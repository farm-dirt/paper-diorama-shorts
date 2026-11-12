"""director - turns project.json + timing.json into frames.  frame(t) -> RGB uint8.

Character motion is stepped "on twos" (a new pose 12 times a second, like hand-made
stop-motion); camera, waves and lights stay smooth at 24 fps.
"""
import importlib.util
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import paperkit
from paperkit import Scene, Layer, grade
from cast import CAST, _apply
import sets as SETS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'assets', 'Fraunces-Black.woff')
STEP = 24.0  # pose updates per second; project "steps": 12 gives a choppier stop-motion feel (never for walks)
LEG = {'ilaw': 205, 'mang_oso': 290, 'kupas': 105}

# ------------------------------------------------------------ pose library
HUMAN = {  # Ilaw + Mang Oso (bones: root torso head armR armL); arms: armR + = outward, armL - = outward
    'idle': {},
    'wave': {'armL': -150, 'head': -4},
    'point': {'armL': -95, 'head': -3},
    'point_up': {'armL': -165, 'head': -14},
    'shock': {'armR': 40, 'armL': -40, 'eyes': 1.5, 'mouth': 0.7, 'torso': -2, 'bob': -10},
    'scared': {'armR': -20, 'armL': 20, 'eyes': 1.45, 'brow': -1, 'mouth': 0.3, 'torso': 4, 'bob': 6},
    'sad': {'head': 10, 'armR': 4, 'armL': -4, 'brow': -1, 'look': 0, 'eyes': 0.85},
    'happy': {'armR': 22, 'armL': -22, 'head': -6, 'eyes': 1.1, 'mouth': 0.35},
    'cheer': {'armR': 150, 'armL': -150, 'head': -10, 'eyes': 1.15, 'mouth': 0.8, 'bob': -14},
    'think': {'armL': -150, 'head': 8, 'look': 0.8, 'brow': 0.4},
    'angry': {'armR': 18, 'armL': -18, 'brow': 1, 'eyes': 0.9, 'torso': -4},
    'look_up': {'head': -16, 'look': 0.2, 'eyes': 1.15},
    'look_back': {'head': 6, 'look': -1, 'face_flip': True},
    'cower': {'armR': -40, 'armL': 40, 'head': 14, 'torso': 8, 'eyes': 1.3, 'brow': -1, 'bob': 20},
    'shrug': {'armR': 55, 'armL': -55, 'head': 8, 'brow': -0.6, 'mouth': 0.15},
}
DOG = {
    'idle': {}, 'wag': {'tail': 30}, 'alert': {'head': -14, 'tail': 35, 'eyes': 1.3},
    'bark': {'head': -10, 'mouth': 1.0, 'tail': 20}, 'sad': {'head': 16, 'tail': -30, 'eyes': 0.8},
    'scared': {'head': 10, 'tail': -40, 'eyes': 1.5, 'bob': 10}, 'happy': {'tail': 40, 'mouth': 0.6, 'head': -6},
}
POSES = {'ilaw': HUMAN, 'mang_oso': HUMAN, 'kupas': DOG}
DEFAULT_SCALE = {'ilaw': 0.86, 'mang_oso': 0.82, 'kupas': 0.72}
NUMERIC_DEFAULTS = {'blink': 0.0, 'mouth': 0.0, 'look': 0.0, 'eyes': 1.0, 'brow': 0.0, 'bob': 0.0}


def ease(u, kind='inOut'):
    u = min(1.0, max(0.0, u))
    if kind == 'linear':
        return u
    if kind == 'in':
        return u * u
    if kind == 'out':
        return 1 - (1 - u) ** 2
    if kind == 'back':  # overshoot then settle (snappy cartoon pose)
        c = 1.70158
        return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


class Director:
    def __init__(self, pdir):
        self.pdir = pdir
        pf = os.path.join(pdir, 'project-files')
        self.proj = json.load(open(os.path.join(pf, 'project.json')))
        tp = os.path.join(pf, 'timing.json')
        self.tim = json.load(open(tp)) if os.path.exists(tp) else {'dur': self.proj['scenes'][-1]['end'], 'env': [], 'envFps': 30, 'speech': []}
        self.fps = self.proj.get('fps', 24)
        self.dur = self.tim['dur']
        self.rigs = {k: f() for k, f in CAST.items()}
        self.custom = None
        cp = os.path.join(pf, 'custom.py')
        if os.path.exists(cp):
            spec = importlib.util.spec_from_file_location('custom', cp)
            self.custom = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.custom)
            if hasattr(self.custom, 'register'):
                self.custom.register(CAST, self.rigs, POSES, SETS)
        self.life = True  # False = no auto blink (thumbnails, model sheets)
        self._font_cache = {}
        self._cap_cache = {}

    # -------------------------------------------------------- helpers
    def scene_at(self, t):
        for i, s in enumerate(self.proj['scenes']):
            if s['start'] <= t < s['end']:
                return i, s
        return len(self.proj['scenes']) - 1, self.proj['scenes'][-1]

    def env(self, t):
        e = self.tim.get('env') or []
        if not e:
            return 0.0
        i = int(t * self.tim.get('envFps', 30))
        return float(e[min(max(i, 0), len(e) - 1)])

    def font(self, size):
        if size not in self._font_cache:
            self._font_cache[size] = ImageFont.truetype(FONT, size)
        return self._font_cache[size]

    def pose_of(self, who, p):
        if isinstance(p, str):
            return dict(POSES.get(who, HUMAN).get(p, {}))
        return dict(p or {})

    def actor_pose(self, a, t, sc, ta):
        """Blend base pose -> keyed poses (absolute times), add life (breath, blink, talk)."""
        who = a['who']
        rig = self.rigs[who]
        base = self.pose_of(who, a.get('pose', 'idle'))

        def full(d):
            out = {}
            for k in set(d) | set(base):
                out[k] = d.get(k, base.get(k))
            return out
        cur = dict(base)
        for k in sorted(a.get('keys', []), key=lambda k_: k_['t']):
            if ta < k['t']:
                break
            target = self.pose_of(who, k['pose'])
            u = ease((ta - k['t']) / max(0.01, k.get('dur', 0.25)), k.get('ease', 'back'))
            nxt = {}
            for name in set(cur) | set(target):
                if name == 'face_flip' or name == 'prop':
                    nxt[name] = target.get(name, cur.get(name)) if u > 0.5 else cur.get(name, target.get(name))
                    continue
                rest = rig.bones[name].get('rest', 0.0) if name in rig.bones else NUMERIC_DEFAULTS.get(name, 0.0)
                va, vb = cur.get(name, rest), target.get(name, rest)
                if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                    nxt[name] = lerp(va, vb, u)
            cur = nxt
        pose = cur
        seed = sum(map(ord, who)) * 7
        # life: breathing + tiny head drift (never fully still)
        pose['bob'] = pose.get('bob', 0) + 2.0 * math.sin(2 * math.pi * ta / 3.1 + seed)
        if 'head' in rig.bones:
            pose['head'] = pose.get('head', rig.bones['head'].get('rest', 0)) + 1.6 * math.sin(2 * math.pi * ta / 4.3 + seed)
        if who == 'kupas':
            pose['tail'] = pose.get('tail', 0) + 14 * math.sin(2 * math.pi * ta * 1.6)
        # blink every ~3.4 s (+ per-character offset), 2 steps long
        ph = (ta + seed % 5) % 3.4
        if self.life and ph < 0.13 and pose.get('blink', 0) < 0.5:
            pose['blink'] = 1.0
        # talking: mouth follows the voice loudness during this actor's talk windows
        talk = a.get('talk')
        if talk:
            wins = [[sc['start'], sc['end']]] if talk is True else talk
            if any(w0 <= ta < w1 for w0, w1 in wins):
                pose['mouth'] = max(pose.get('mouth', 0), min(1.0, self.env(ta) * 1.1))
        # walking (always smooth, steps timed to the distance covered so feet don't skate)
        wk = a.get('walk')
        if wk:
            dist, moving = self.walk_dist(a, t)
            if moving:
                scale = a.get('scale', DEFAULT_SCALE.get(who, 0.8))
                if who == 'kupas':
                    stride = 2 * LEG[who] * scale * math.sin(math.radians(24)) * 1.4
                    ph = math.pi * dist / max(1.0, stride)
                    sw = math.sin(ph)
                    for b_, sgn in (('legFL', 1), ('legBR', 1), ('legFR', -1), ('legBL', -1)):
                        pose[b_] = 24 * sw * sgn
                    pose['bob'] = pose.get('bob', 0) - 4 * abs(math.sin(ph))
                    pose['head'] = pose.get('head', 0) + 3 * math.sin(2 * ph)
                else:
                    stride = 0.55 * LEG[who] * scale  # one step (front-on puppet walk)
                    ph = math.pi * dist / max(1.0, stride)
                    sw = math.sin(ph)
                    lift = 0.07 * LEG[who]
                    pose['legL_dy'] = -lift * max(0.0, sw)
                    pose['legR_dy'] = -lift * max(0.0, -sw)
                    pose['legL'] = pose.get('legL', 0) + 5 * max(0.0, sw)
                    pose['legR'] = pose.get('legR', 0) - 5 * max(0.0, -sw)
                    pose['armR'] = pose.get('armR', rig.bones['armR'].get('rest', 0)) + 9 * sw
                    pose['armL'] = pose.get('armL', rig.bones['armL'].get('rest', 0)) + 9 * sw
                    pose['torso'] = pose.get('torso', 0) + 2.5 * sw
                    pose['head'] = pose.get('head', rig.bones['head'].get('rest', 0)) - 1.5 * sw
                    pose['bob'] = pose.get('bob', 0) - 0.03 * LEG[who] * abs(sw)
        return pose

    def walk_x(self, a, t):
        set_ = self._set
        def xof(v):
            return set_['marks'][v] if isinstance(v, str) else v
        x0 = xof(a.get('mark', a.get('x', 'C')))
        wk = a.get('walk')
        if not wk:
            return x0, x0, x0
        x1 = xof(wk['to'])
        u = ease((t - wk['s']) / max(0.01, wk['e'] - wk['s']), wk.get('ease', 'inOut'))
        return x0, x1, lerp(x0, x1, u) if t >= wk['s'] else x0

    def walk_dist(self, a, t):
        wk = a['walk']
        x0, x1, x = self.walk_x(a, t)
        return abs(x - x0), wk['s'] <= t < wk['e']

    def actor_x(self, a, set_, t):
        x0, x1, x = self.walk_x(a, t)
        face = a.get('face', 1)
        wk = a.get('walk')
        if wk and wk['s'] <= t < wk['e'] and 'face' not in a and a['who'] == 'kupas':
            face = 1 if x1 >= x0 else -1
        return x, face

    # -------------------------------------------------------- frame
    def frame(self, t, fi=0):
        si, sc = self.scene_at(t)
        set_ = SETS.get_set(sc['set'], sc.get('variant'))
        S = Scene(1080, 1920)
        for it in set_['items']:
            dx, dy = it['move'](t) if it['move'] else (0, 0)
            S.add(it['layer'], it['z'], it['lift'], it['x'], it['y'], dx, dy, key=it['key'])
        step = float(self.proj.get('steps', STEP))
        ta = math.floor(t * step + 1e-6) / step
        self._set = set_
        glows = list(set_['glows'](t))
        locs = {}
        for a in sc.get('actors', []):
            rig = self.rigs[a['who']]
            pose = self.actor_pose(a, t, sc, ta)
            x, face = self.actor_x(a, set_, t)
            if pose.pop('face_flip', False):
                face = -face
            pose['face'] = face
            scale = a.get('scale', DEFAULT_SCALE.get(a['who'], 0.8))
            L, fx, fy = rig.render(pose=pose, scale=scale, seed=31 + len(a['who']))
            fy_ = a.get('y', set_['floor'])
            ox, oy = x - fx, fy_ - fy
            S.add(L, a.get('z', 2.0), lift=a.get('lift', 0.8), x=ox, y=oy)
            W_ = rig.world
            locs[a['who']] = {b: tuple(_apply(W_[b], [(0, 0)])[0] + [ox, oy]) for b in W_}
            if a['who'] == 'ilaw' and pose.get('lantern_on', True):
                lx, ly = _apply(W_['lantern'], [(0, 92)])[0] + [ox, oy]
                glows.append((lx, ly, 150, '#FF8A3D', 0.30))
        if self.custom and hasattr(self.custom, 'draw'):
            more = self.custom.draw(sc, S, t, dict(set=set_, locs=locs, scene_index=si))
            if more:
                glows += more
        # camera
        cam = sc.get('cam', {})
        u = ease((t - sc['start']) / max(0.01, sc['end'] - sc['start']), cam.get('ease', 'inOut'))
        c0 = cam.get('from', [0, 0, 1.0])
        c1 = cam.get('to', c0)
        cx, cy, cz = [lerp(c0[i], c1[i], u) for i in range(3)]
        sh = sc.get('shake')
        if sh and sh['t'] <= t < sh['t'] + sh.get('dur', 0.4):
            k = 1 - (t - sh['t']) / sh.get('dur', 0.4)
            amp = sh.get('amp', 14) * k
            cx += amp * math.sin(t * 91)
            cy += amp * math.cos(t * 73)
        focus = sc.get('focus', set_['focus'])
        rk = sc.get('rack')
        if rk and t >= rk['t']:
            focus = lerp(focus, rk['to'], ease((t - rk['t']) / rk.get('dur', 0.5)))
        img = S.render(focus=focus, dof=sc.get('dof', self.proj.get('dof', 0.3)), cam=(cx, cy, cz))
        fl = 0.0
        f_ = sc.get('flash')
        if f_ and f_['t'] <= t < f_['t'] + f_.get('dur', 0.2):
            fl = 0.7 * (1 - (t - f_['t']) / f_.get('dur', 0.2))
        # glows follow the camera roughly (they belong to near-focus objects)
        par = 1.0
        zz = 1 + (cz - 1) * par
        glows = [(zz * gx + (1 - zz) * 540 - cx * par, zz * gy + (1 - zz) * 960 - cy * par, r * zz, c, a)
                 for (gx, gy, r, c, a) in glows]
        out = grade(img, glows=glows, light=sc.get('light', set_['light']), frame=fi,
                    flash=fl, flash_color=(f_ or {}).get('color', '#FFFFFF'),
                    letterbox=sc.get('letterbox', 0))
        out = self.overlay(out, t)
        return out

    # -------------------------------------------------------- captions, hook, CTA
    def caption_img(self, text, size, maxw=900):
        key = (text, size, paperkit.K)
        if key in self._cap_cache:
            return self._cap_cache[key]
        k = paperkit.K
        f = self.font(int(size * k))
        words = []
        for w in text.split():
            hl = w.startswith('*') and w.endswith('*') or w.startswith('*')
            words.append((w.strip('*'), hl or (w.endswith('*') and not w.startswith('*'))))
        # simple greedy wrap
        lines, cur = [], []
        for w in words:
            trial = ' '.join(x[0] for x in cur + [w])
            if cur and f.getlength(trial) > maxw * k:
                lines.append(cur)
                cur = [w]
            else:
                cur.append(w)
        lines.append(cur)
        lh = int(size * 1.12 * k)
        tw = max(f.getlength(' '.join(x[0] for x in ln)) for ln in lines)
        pad_x, pad_y = int(34 * k), int(18 * k)
        Wd, Hd = int(tw + 2 * pad_x + 30 * k), int(lh * len(lines) + 2 * pad_y + 30 * k)
        img = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        r = np.random.default_rng(abs(hash(text)) % 99991)
        x0, y0, x1, y1 = 10 * k, 8 * k, Wd - 20 * k, Hd - 22 * k
        edge = []
        for i in range(24):
            edge.append((x0 + (x1 - x0) * i / 23, y0 + r.uniform(-3, 3) * k))
        for i in range(24):
            edge.append((x1 - (x1 - x0) * i / 23, y1 + r.uniform(-3, 3) * k))
        sh = [(x + 7 * k, y + 9 * k) for x, y in edge]
        shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(shadow).polygon(sh, fill=(20, 12, 10, 120))
        from PIL import ImageFilter
        shadow = shadow.filter(ImageFilter.GaussianBlur(6 * k))
        img = Image.alpha_composite(img, shadow)
        d = ImageDraw.Draw(img)
        d.polygon(edge, fill=(244, 236, 220, 255))
        y = y0 + pad_y - 4 * k
        for ln in lines:
            s = ' '.join(x[0] for x in ln)
            x = x0 + (x1 - x0 - f.getlength(s)) / 2
            for w, hl in ln:
                d.text((x, y), w, font=f, fill=(196, 58, 46) if hl else (40, 30, 30))
                x += f.getlength(w + ' ')
            y += lh
        arr = np.asarray(img).astype(np.float32) / 255
        self._cap_cache[key] = arr
        return arr

    def paste(self, out, rgba, cx, cy, scale=1.0, rot=0.0):
        if scale != 1.0:
            import cv2
            rgba = cv2.resize(rgba, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        if rot:
            import cv2
            h, w = rgba.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, 1.0)
            rgba = cv2.warpAffine(rgba, M, (w, h))
        h, w = rgba.shape[:2]
        k = paperkit.K
        x0, y0 = int(cx * k - w / 2), int(cy * k - h / 2)
        H_, W_ = out.shape[:2]
        sx0, sy0 = max(0, -x0), max(0, -y0)
        dx0, dy0 = max(0, x0), max(0, y0)
        ww, hh = min(w - sx0, W_ - dx0), min(h - sy0, H_ - dy0)
        if ww <= 0 or hh <= 0:
            return
        src = rgba[sy0:sy0 + hh, sx0:sx0 + ww]
        dst = out[dy0:dy0 + hh, dx0:dx0 + ww].astype(np.float32) / 255
        a = src[..., 3:4]
        dst = src[..., :3] * a + dst * (1 - a)
        out[dy0:dy0 + hh, dx0:dx0 + ww] = (dst * 255 + 0.5).astype(np.uint8)

    def overlay(self, out, t):
        P = self.proj
        out = out.copy()
        hook = P.get('hook')
        if hook and hook.get('s', 0) <= t < hook.get('e', 2.0):
            u = (t - hook.get('s', 0)) / 0.18
            sc = 0.6 + 0.4 * ease(u, 'back') if u < 1 else 1.0
            self.paste(out, self.caption_img(hook['text'], 96, 860), 540, hook.get('y', 330), sc, rot=-3)
        for c in P.get('captions', []):
            if c['s'] <= t < c['e']:
                u = (t - c['s']) / 0.12
                dy = 16 * (1 - ease(u, 'out')) if u < 1 else 0
                self.paste(out, self.caption_img(c['text'], 66), 540, P.get('captionY', 420) + dy)
        for o in (P.get('overlays') or []) if hook is not None else []:  # silent tags (none on thumbnails)
            if o['s'] <= t < o['e']:
                u = (t - o['s']) / 0.16
                sc_ = 0.6 + 0.4 * ease(u, 'back') if u < 1 else 1.0
                self.paste(out, self.caption_img(o['text'], o.get('size', 72), o.get('maxw', 860)), o['x'], o['y'], sc_, rot=o.get('rot', 0))
        cta = P.get('cta')
        if cta and cta['s'] <= t < cta['e']:
            self.draw_cta(out, t, cta)
        return out

    def draw_cta(self, out, t, cta):
        k = paperkit.K
        u = t - cta['s']
        done = u >= cta.get('tap', 0.95)
        label = 'SUBSCRIBED' if done else 'SUBSCRIBE'
        key = ('cta', label, k)
        if key not in self._cap_cache:
            f = self.font(int(48 * k))
            w = int(f.getlength(label) + 90 * k)
            h = int(96 * k)
            img = Image.new('RGBA', (w + int(20 * k), h + int(20 * k)), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.rounded_rectangle([8 * k, 10 * k, w + 8 * k, h + 10 * k], 18 * k, fill=(20, 12, 10, 110))
            col = (150, 140, 130, 255) if done else (210, 69, 58, 255)
            d.rounded_rectangle([0, 0, w, h], 18 * k, fill=col)
            d.text((45 * k, 18 * k), label, font=f, fill=(244, 236, 220))
            self._cap_cache[key] = np.asarray(img).astype(np.float32) / 255
        tag = self._cap_cache[key]
        slide = 1 - ease(u / 0.3, 'back') if u < 0.3 else 0
        out_ = 1 - ease((cta['e'] - t) / 0.3, 'in') if cta['e'] - t < 0.3 else 0
        x = 540 + 700 * slide + 700 * out_
        y = cta.get('y', 1440)
        pop = 1.0 + (0.12 * math.sin(min(1, (u - cta.get('tap', .95)) / 0.2) * math.pi) if done and u - cta.get('tap', .95) < 0.2 else 0)
        self.paste(out, tag, x, y, pop)
        # paper hand that taps
        tp = cta.get('tap', 0.95)
        if 0.35 < u < tp + 0.5:
            hu = min(1.0, (u - 0.35) / max(0.05, tp - 0.35))
            hx = x + 120
            hy = y + 150 - 110 * ease(hu, 'inOut') + (14 if abs(u - tp) < 0.08 else 0)
            hand = self._hand()
            self.paste(out, hand, hx, hy)

    def _hand(self):
        key = ('hand', paperkit.K)
        if key not in self._cap_cache:
            L = Layer(200, 260, seed=77)
            L.ellipse(100, 170, 58, 64, '#EBC39C', n=14)
            L.poly([(76, 40), (110, 40), (112, 150), (74, 150)], '#EBC39C')
            L.poly([(58, 210), (142, 210), (150, 260), (50, 260)], '#E0A33A')
            P_, A_ = L.P, L.A
            rgb = np.where(A_[..., None] > 0, P_ / np.maximum(A_[..., None], 1e-4), 0)
            self._cap_cache[key] = np.dstack([np.clip(rgb, 0, 1), A_])
        return self._cap_cache[key]

