"""Frost Bamboo Pudding - the trip.  Original sets, props and POV hands for this short.

Story (no voice): you find the frost bamboo on your map at home, walk out through the snowy village,
cross a frozen river, follow glowing drips through the woods, tick the map, push through an icicle
curtain into the ice cave, rub the frost off the wall, crack the ice, snap the bamboo and eat the
pudding inside. Every scene reads its event times from scene["ev"] (written by make_project.py), so the
pictures and the sounds share one clock.
"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paperkit
from paperkit import Layer, ellipse_pts

W, H = 1080, 1920
FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(paperkit.__file__))), 'assets', 'Fraunces-Black.woff')
_C = {}

# palette
SNOW, SNOW2, SNOW3 = '#EEF2F8', '#D3DCEC', '#AEBBD6'
PINE, PINE2, PINE3 = '#3C6E6B', '#2E5958', '#4F8780'
ICE, ICE2, ICE3, ICE4 = '#A9D7EA', '#CBEAF5', '#7FB6D3', '#4E80AA'
JADE, JADE2, JADE3 = '#8FDCB2', '#5FBF92', '#3F9A75'
CREAM, KNIT_RED, SLEEVE = '#F2E6D2', '#C94A3E', '#2F6F78'
INK, RED = '#4E3628', '#C43A2E'
CYAN = '#8FF3FF'


def sm(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def cache(key, fn):
    k = (key, paperkit.K)
    if k not in _C:
        if len(_C) > 700:
            _C.clear()
        _C[k] = fn()
    return _C[k]


# ------------------------------------------------------------------ shape kit (rotatable, scalable props)
def E(cx, cy, rx, ry, color, rot=0.0, **kw):
    return (ellipse_pts(cx, cy, rx, ry, rot), color, kw)


def P(pts, color, **kw):
    return (np.asarray(pts, np.float32), color, kw)


def build(shapes, ang=0.0, s=1.0, seed=5):
    """shapes in local coords (pivot = 0,0) -> (Layer, ox, oy) after rotating by ang degrees and scaling."""
    a = math.radians(ang)
    c, si = math.cos(a), math.sin(a)
    tp = []
    for pts, col, kw in shapes:
        q = np.asarray(pts, np.float32) * s
        q = np.stack([c * q[:, 0] - si * q[:, 1], si * q[:, 0] + c * q[:, 1]], 1)
        tp.append((q, col, kw))
    allp = np.concatenate([q for q, _, _ in tp])
    x0, y0 = allp.min(0) - 24
    x1, y1 = allp.max(0) + 24
    L = Layer(int(x1 - x0) + 1, int(y1 - y0) + 1, seed=seed)
    for q, col, kw in tp:
        L.poly(q - [x0, y0], col, **kw)
    return L, float(x0), float(y0)


def place(S, name, shapes_fn, x, y, z=2.0, ang=0.0, s=1.0, lift=0.6, seed=5):
    ang = round(ang / 2.0) * 2.0
    s = round(s, 2)
    L, ox, oy = cache(('shape', name, ang, s), lambda: build(shapes_fn(), ang, s, seed))
    S.add(L, z, lift, x + ox, y + oy, key=f'{name}|{ang}|{s}|{paperkit.K}')


def ink_text(L, text, x, y, size, color, rot=0.0):
    """Hand-lettered label printed onto a paper layer (centre x, y)."""
    k = paperkit.K
    f = ImageFont.truetype(FONT, max(6, int(size * k)))
    tw = int(f.getlength(text)) + 8
    th = int(size * 1.4 * k) + 8
    im = Image.new('L', (tw, th), 0)
    ImageDraw.Draw(im).text((4, 2), text, font=f, fill=255)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    m = np.asarray(im).astype(np.float32) / 255 * 0.92
    X0, Y0 = int(x * k - m.shape[1] / 2), int(y * k - m.shape[0] / 2)
    hh, ww = m.shape
    X1, Y1 = min(L.pw, X0 + ww), min(L.ph, Y0 + hh)
    m = m[:Y1 - Y0, :X1 - X0]
    col = paperkit.hexc(color)
    Pp = L.P[Y0:Y1, X0:X1]
    L.P[Y0:Y1, X0:X1] = col * m[..., None] + Pp * (1 - m[..., None])
    L.A[Y0:Y1, X0:X1] = m + L.A[Y0:Y1, X0:X1] * (1 - m)


# ------------------------------------------------------------------ the viewer's hands + props
def mitten_shapes(side):
    """Knitted mitten + coat sleeve, fingers pointing up; pivot = middle of the mitten. side 1 = right hand."""
    th = -1 if side == 1 else 1      # thumb on the inner side
    return [
        P([(-95, 150), (95, 150), (120, 520), (-120, 520)], SLEEVE, crease=[((0, 160), (0, 520), 0.12)]),
        P([(-100, 108), (100, 108), (104, 178), (-104, 178)], CREAM, pat='vstripes', pat_period=12),
        P([(-102, 128), (102, 128), (102, 146), (-102, 146)], KNIT_RED),
        E(th * 78, 20, 34, 64, '#E8D8BE', rot=th * 0.45),
        E(0, -10, 90, 128, CREAM, pat='check', pat_period=15),
        P([(0, -40), (24, -12), (0, 16), (-24, -12)], KNIT_RED, paint=True),
        P([(-50, 62), (50, 62), (46, 74), (-46, 74)], '#D9C8AC', paint=True),
    ]


def put_hand(S, side, x, y, ang=0.0, z=2.0, s=1.0):
    place(S, f'mitten{side}', lambda: mitten_shapes(side), x, y, z, ang, s, lift=0.9, seed=60 + side)


def spoon_shapes():
    """Spoon, tip of the bowl at (0, 0), handle going down."""
    return [P([(-9, 120), (9, 120), (14, 430), (-14, 430)], '#C5CFDA', crease=[((0, 120), (0, 430), 0.15)]),
            E(0, 70, 50, 74, '#DDE5EE'),
            E(0, 76, 36, 56, '#AFBBCB', shade=1.0),
            E(-12, 54, 10, 18, '#FFFFFF', paint=True, alpha=0.7)]


def spoon_full_shapes():
    return spoon_shapes() + [E(0, 66, 40, 34, '#F6F0DA'), E(6, 58, 16, 10, JADE, paint=True, alpha=0.8),
                             E(-14, 52, 8, 6, '#FFFFFF', paint=True, alpha=0.8)]


def pencil_shapes():
    """Pencil, tip at (0, 0), going down."""
    return [P([(0, 0), (-12, 40), (12, 40)], '#3A2E2A'),
            P([(-12, 40), (12, 40), (16, 70), (-16, 70)], '#E9C79A'),
            P([(-16, 70), (16, 70), (16, 330), (-16, 330)], '#E8B33A', crease=[((0, 70), (0, 330), 0.18)]),
            P([(-16, 330), (16, 330), (16, 352), (-16, 352)], '#B9BFC6'),
            P([(-16, 352), (16, 352), (14, 384), (-14, 384)], '#E88C9A')]


def lantern_shapes():
    """Small paper lantern, hanging point at (0, 0)."""
    return [P([(-3, 0), (3, 0), (3, 40), (-3, 40)], '#5A4A42'),
            P([(-46, 40), (46, 40), (38, 62), (-38, 62)], '#3E3632'),
            P([(-40, 62), (40, 62), (46, 170), (-46, 170)], '#FFCF7A', glow=0.25),
            P([(-40, 62), (-30, 62), (-34, 170), (-46, 170)], '#E59A4A'),
            P([(30, 62), (40, 62), (46, 170), (34, 170)], '#E59A4A'),
            P([(-50, 170), (50, 170), (42, 192), (-42, 192)], '#3E3632'),
            E(0, 120, 14, 22, '#FFF4CC', paint=True, glow=0.4)]


def w2s(x, y, z, cam):
    """World point on a layer at depth z -> screen point (same maths as paperkit.Scene.render)."""
    cx, cy, cz = cam
    par = 2.0 / max(z, 0.25)
    zz = 1 + (cz - 1) * par
    return zz * x + (1 - zz) * 540 - cx * par, zz * y + (1 - zz) * 960 - cy * par


# ------------------------------------------------------------------ scenery helpers
def pine(L, x, base, h, w, col=PINE, snow=SNOW, tiers=4, seed=0):
    L.poly([(x - w * 0.06, base), (x + w * 0.06, base), (x + w * 0.05, base - h * 0.25), (x - w * 0.05, base - h * 0.25)], '#5A4636')
    for i in range(tiers):
        u = i / tiers
        tb = base - h * (0.12 + 0.8 * u)
        tw = w * (1 - 0.72 * u)
        tt = tb - h * 0.34
        L.poly([(x - tw / 2, tb), (x, tt), (x + tw / 2, tb)], col, shade=0.92 + 0.06 * (i % 2),
               crease=[((x, tt), (x, tb), 0.10)])
        # snow resting on each tier
        L.poly([(x - tw * 0.36, tb - h * 0.10), (x, tt + 4), (x + tw * 0.30, tb - h * 0.12),
                (x + tw * 0.14, tb - h * 0.07), (x - tw * 0.06, tb - h * 0.11)], snow, rim=0.8)


def sky(seed, base, bands):
    L = Layer(W, H, seed=seed, grain=0.08)
    L.rect(0, 0, W, H, base, rim=0, shadow=0, rough=0)
    for i, (y, c, a) in enumerate(bands):
        xs = np.arange(-60, W + 70, 10, dtype=np.float32)
        ys = y + a * np.sin(2 * math.pi * xs / (520 + 90 * i) + i * 1.7)
        L.poly(np.concatenate([np.stack([xs, ys], 1), [[W + 60, H], [-60, H]]]), c, grad=0.05)
    return L


def ridge(L, base, height, seed, col, step=16, snowcap=None):
    xs = np.arange(-60, W + 76, step, dtype=np.float32)
    n = paperkit.noise1d(len(xs), seed, 7)
    n = np.convolve(n, np.ones(5) / 5, 'same')
    ys = base - height * (0.5 + 0.5 * n / (np.abs(n).max() + 1e-6))
    L.poly(np.concatenate([np.stack([xs, ys], 1), [[W + 60, H], [-60, H]]]), col)
    if snowcap:
        L.poly(np.concatenate([np.stack([xs, ys], 1), np.stack([xs[::-1], ys[::-1] + 26], 1)]), snowcap, rim=0.6)


def item(layer, z, lift=1.0, x=0, y=0, key=None, move=None):
    return dict(layer=layer, z=z, lift=lift, x=x, y=y, key=key, move=move)


# ================================================================== SET: the paper map
STOPS = {'home': (270, 1330), 'river': (565, 1188), 'woods': (330, 985), 'cave': (590, 820)}
ROUTE = [(270, 1330), (380, 1285), (500, 1230), (565, 1188), (560, 1120), (470, 1060), (330, 985),
         (330, 930), (420, 880), (520, 850), (590, 820)]


def catmull(pts, n=14):
    pts = np.asarray(pts, np.float32)
    P_ = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1])
    return np.array(out)


def map_layer():
    L = Layer(W, H, seed=901, grain=0.09)
    L.poly([(92, 500), (886, 486), (896, 1478), (84, 1462)], '#EFE2C4', grad=0.06,
           crease=[((360, 490), (356, 1470), 0.07), ((622, 488), (628, 1474), 0.07), ((88, 990), (892, 982), 0.06)])
    L.poly([(92, 500), (886, 486), (887, 512), (93, 524)], '#E2D1AE', rim=0)
    # river
    for off, col in ((0, '#5B86B5'), (22, '#5B86B5')):
        xs = np.linspace(110, 870, 60)
        ys = 1175 + off + 16 * np.sin(xs / 55)
        L.stroke(np.stack([xs, ys], 1), col, 7)
    for i in range(5):
        x = 170 + i * 150
        L.stroke([(x, 1188 + 12 * math.sin(x / 55)), (x + 40, 1188 + 12 * math.sin((x + 40) / 55))], '#8FB3D8', 4)
    # home
    hx, hy = STOPS['home']
    L.poly([(hx - 42, hy + 20), (hx + 42, hy + 20), (hx + 42, hy - 26), (hx - 42, hy - 26)], '#E9D7B4', paint=True)
    L.stroke([(hx - 42, hy + 20), (hx + 42, hy + 20), (hx + 42, hy - 26), (hx, hy - 62), (hx - 42, hy - 26), (hx - 42, hy + 20)], INK, 6)
    L.stroke([(hx - 10, hy + 20), (hx - 10, hy - 4), (hx + 10, hy - 4), (hx + 10, hy + 20)], INK, 5)
    L.stroke([(hx + 22, hy - 40), (hx + 22, hy - 62), (hx + 34, hy - 62), (hx + 34, hy - 32)], INK, 5)
    # woods
    for (dx, dy, s) in [(-70, 10, 1.0), (-20, -20, 1.2), (30, 6, 0.9), (75, -16, 1.05), (-110, -26, 0.8)]:
        x, y = STOPS['woods'][0] + dx, STOPS['woods'][1] + dy
        L.poly([(x - 22 * s, y + 20), (x, y - 44 * s), (x + 22 * s, y + 20)], '#6E9A86', paint=True)
        L.stroke([(x - 22 * s, y + 20), (x, y - 44 * s), (x + 22 * s, y + 20), (x - 22 * s, y + 20)], INK, 4)
    # mountain + cave + the frost bamboo drawing
    L.poly([(410, 905), (520, 700), (590, 650), (660, 720), (790, 905)], '#DCD3E6', paint=True)
    L.stroke([(410, 905), (520, 700), (590, 650), (660, 720), (790, 905)], INK, 6)
    L.stroke([(545, 690), (590, 715), (625, 690)], INK, 4)
    L.poly(ellipse_pts(590, 862, 66, 92, 0, a0=math.pi, a1=2 * math.pi), '#3D3550', paint=True)
    L.poly([(524, 860), (656, 860), (656, 880), (524, 880)], '#3D3550', paint=True)
    for dx in (-30, 0, 30):
        tp = 760 - (14 if dx == 0 else 0)
        L.poly([(590 + dx - 10, 872), (590 + dx + 10, 872), (590 + dx + 9, tp), (590 + dx - 9, tp)], '#6FE3B4', paint=True, glow=0.3)
        for ny in (830, 795):
            L.stroke([(590 + dx - 11, ny), (590 + dx + 11, ny)], '#2E7E5E', 4)
    # route (red dashes)
    path = catmull(ROUTE)
    seg = np.cumsum(np.r_[0, np.linalg.norm(np.diff(path, axis=0), axis=1)])
    d = 0.0
    while d < seg[-1] - 10:
        i0 = np.searchsorted(seg, d)
        i1 = np.searchsorted(seg, min(seg[-1], d + 18))
        if i1 > i0:
            L.stroke(path[i0:i1 + 1], RED, 6)
        d += 34
    # labels
    ink_text(L, '~ Frost Bamboo ~', 470, 572, 50, RED, rot=1.5)
    ink_text(L, 'home', 250, 1408, 40, INK)
    ink_text(L, 'river', 770, 1240, 40, '#3E6A98')
    ink_text(L, 'woods', 520, 1010, 40, INK)
    ink_text(L, 'cave', 750, 860, 40, INK)
    # a tiny compass rose
    L.stroke([(800, 600), (800, 700)], INK, 4)
    L.stroke([(750, 650), (850, 650)], INK, 4)
    L.poly([(800, 588), (812, 622), (788, 622)], RED, paint=True)
    return L


def build_map(variant='home'):
    its = []
    if variant == 'home':
        bg = Layer(W, H, seed=910)
        bg.rect(0, 0, W, H, '#5E4033', pat='planks', pat_period=135, rim=0, shadow=0, rough=0)
        bg.rect(40, 110, 560, 820, '#3A2A22')
        bg.rect(70, 140, 530, 790, '#5A6FA8', grad=0.25)
        bg.poly([(70, 600), (170, 520), (270, 600), (330, 560), (530, 640), (530, 790), (70, 790)], SNOW2)
        bg.rect(70, 650, 530, 790, SNOW)
        bg.rect(292, 140, 308, 790, '#3A2A22')
        bg.rect(70, 456, 530, 472, '#3A2A22')
        bg.rect(660, 820, 1080, 850, '#3A2A22')
        bg.poly([(840, 820), (880, 700), (930, 700), (960, 820)], '#C98A4A')
        bg.ellipse(900, 650, 70, 58, '#FFD98A', glow=0.3)
        its.append(item(bg, 8, 0.6, key='mapbg-home'))
        g0 = [(300, 470, 300, '#9FB9FF', 0.12), (900, 650, 260, '#FFC060', 0.30)]
    elif variant == 'woods':
        bg = sky(911, '#AFC2DC', [(700, '#C2D1E6', 24), (900, '#D6E1EF', 18)])
        ridge(bg, 1000, 200, 3, '#9AA6C8', snowcap=SNOW)
        for i in range(8):
            pine(bg, 40 + i * 145, 1500 + 40 * (i % 2), 700 + 80 * (i % 3), 300, PINE2 if i % 2 else PINE)
        bg.rect(0, 1450, W, H, SNOW)
        its.append(item(bg, 8, 0.6, key='mapbg-woods'))
        g0 = [(540, 500, 600, '#FFFFFF', 0.08)]
    else:  # cave
        bg = Layer(W, H, seed=912)
        bg.rect(0, 0, W, H, '#25335C', rim=0, shadow=0, rough=0)
        r = np.random.default_rng(4)
        for _ in range(60):
            x, y = r.uniform(-60, W + 60), r.uniform(-60, H + 60)
            pts = [(x + r.uniform(-140, 140), y + r.uniform(-160, 160)) for _ in range(4)]
            bg.poly(pts, [ICE3, ICE4, '#5F92BC', '#3E6896'][r.integers(4)], shade=0.8 + 0.3 * r.random())
        its.append(item(bg, 8, 0.6, key='mapbg-cave'))
        g0 = [(540, 900, 700, '#7FD8FF', 0.14), (540, 1000, 300, '#FFD890', 0.10)]
    its.append(item(cache('map-paper', map_layer), 2.2, 0.9, key='map-paper'))

    def glows(t):
        p = 0.5 + 0.5 * math.sin(t * 3.1)
        return g0 + [(590, 820, 70 + 14 * p, '#7FFFD0', 0.40 + 0.25 * p), (590, 820, 190, CYAN, 0.10 + 0.06 * p)]
    return dict(items=its, glows=glows, floor=1700, focus=2.2, light='warm' if variant == 'home' else ('snow' if variant == 'woods' else 'ice'),
                marks={'C': 540})


def check_pts(stop):
    x, y = STOPS[stop]
    x += 58
    y -= 14
    return np.array([(x - 22, y), (x - 6, y + 20), (x + 30, y - 30)], np.float32)


def partial(pts, frac):
    pts = np.asarray(pts, np.float32)
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    tot = seg[-1] * min(1.0, max(0.0, frac))
    out = [pts[0]]
    for i in range(1, len(pts)):
        if seg[i] <= tot:
            out.append(pts[i])
        else:
            u = (tot - seg[i - 1]) / max(1e-6, seg[i] - seg[i - 1])
            out.append(pts[i - 1] + (pts[i] - pts[i - 1]) * u)
            break
    return np.array(out)


def draw_map(sc, S, t, ev):
    # ticks on the map (persisting ones + animated ones)
    for stop, ts in ev.get('checks', []):
        if t < ts:
            continue
        frac = sm((t - ts) / 0.32)
        q = partial(check_pts(stop), frac)
        if len(q) >= 2:
            def shp(q=q):
                return [P(np.vstack([q + [0, 4], q[::-1] + [0, -4]]), RED, paint=True)]
            key = f'check-{stop}-{round(frac, 2)}'
            L, ox, oy = cache(('chk', key), lambda: build_line(q, RED, 11))
            S.add(L, 2.19, 0.0, ox, oy, key=key + str(paperkit.K))
    # steam curling off the bamboo drawing
    for i in range(3):
        ph = ((t * 0.55 + i / 3) % 1.0)
        x = 590 + 14 * math.sin(ph * 6 + i * 2)
        y = 790 - 120 * ph
        s = 0.5 + 0.9 * ph
        place(S, 'mapsteam', lambda: [E(0, 0, 22, 14, '#F7FAFF', alpha=0.85)], x, y, 2.18, 0, round(s * 5) / 5, lift=0.2)


def build_line(q, col, wdt):
    q = np.asarray(q, np.float32)
    x0, y0 = q.min(0) - 30
    x1, y1 = q.max(0) + 30
    L = Layer(int(x1 - x0) + 1, int(y1 - y0) + 1, seed=77)
    if len(q) == 2:
        mid = (q[0] + q[1]) / 2
        q = np.vstack([q[0], mid, q[1]])
    L.stroke(q - [x0, y0], col, wdt)
    return L, float(x0), float(y0)


def pov_map(sc, S, t, ev, cam):
    """Both mittens hold the map; the right one taps the bamboo / ticks with the pencil."""
    lift = 6 * math.sin(t * 1.3)
    lx, ly = w2s(110, 1330, 2.2, cam)
    put_hand(S, -1, lx - 20, ly + 140 + lift, ang=12)
    pen = ev.get('pencil')
    tap = ev.get('tap')
    rx, ry = w2s(868, 1330, 2.2, cam)
    hand = (rx + 20, ry + 140 + lift, -12)
    if tap and tap - 0.45 < t < tap + 0.9:
        bx, by = w2s(*STOPS['cave'], 2.2, cam)
        u = sm((t - (tap - 0.45)) / 0.4) if t < tap else 1 - sm((t - tap - 0.25) / 0.6)
        press = 10 * math.exp(-((t - tap) / 0.06) ** 2)
        hand = (lerp(hand[0], bx + 40, u), lerp(hand[1], by + 150 + press, u), lerp(-12, -22, u))
    if pen:
        p0, p1 = pen
        if p0 - 0.4 < t < p1 + 0.5:
            u = sm((t - (p0 - 0.4)) / 0.4) if t < p1 else 1 - sm((t - p1) / 0.5)
            tip = None
            for stop, ts in ev.get('checks', []):
                if ts - 0.25 <= t <= ts + 0.45:
                    q = partial(check_pts(stop), sm((t - ts) / 0.32))
                    tip = q[-1]
            if tip is None:
                nxt = [c for c in ev.get('checks', []) if c[1] >= t - 0.5]
                tip = check_pts((nxt[0] if nxt else ev['checks'][-1])[0])[0]
            tx, ty = w2s(tip[0], tip[1], 2.2, cam)
            ang = 28
            a = math.radians(ang)
            hx = lerp(hand[0], tx - math.sin(a) * -1 * 0 + 300 * math.sin(a) + 40, u)
            hy = lerp(hand[1], ty + 300 * math.cos(a) + 60, u)
            if u > 0.05:
                px = lerp(hx + 200, tx, u)
                py = lerp(hy + 200, ty, u)
                place(S, 'pencil', pencil_shapes, px, py, 2.0, -ang, 1.0, lift=1.0, seed=71)
            hand = (hx, hy, lerp(-12, -24, u))
    put_hand(S, 1, hand[0], hand[1], ang=hand[2])


# ================================================================== SET: snowy village at dawn
def cottage(L, x, base, w, h, wall, seed=0, lit=True):
    L.rect(x, base - h, x + w, base, wall, pat='hplanks', pat_period=26)
    L.poly([(x - 30, base - h + 10), (x + w / 2, base - h - h * 0.75), (x + w + 30, base - h + 10)], '#6B4A44',
           crease=[((x + w / 2, base - h - h * 0.75), (x + w / 2, base - h), 0.12)])
    # thick snow on the roof with drips
    pts = [(x - 40, base - h + 4), (x + w / 2, base - h - h * 0.80), (x + w + 40, base - h + 4)]
    drip = [(x + w + 40 - i * (w + 80) / 8, base - h + 4 + (18 if i % 2 else 34)) for i in range(9)]
    L.poly(pts + drip, SNOW, crease=[((x + w / 2, base - h - h * 0.8), (x + w / 2, base - h + 10), 0.08)])
    L.rect(x + w * 0.62, base - h - h * 0.62, x + w * 0.76, base - h - h * 0.25, '#5A403C')
    L.rect(x + w * 0.60, base - h - h * 0.66, x + w * 0.78, base - h - h * 0.60, SNOW)
    if lit:
        L.rect(x + w * 0.18, base - h * 0.62, x + w * 0.42, base - h * 0.30, '#FFC56E', glow=0.25)
        L.rect(x + w * 0.29, base - h * 0.62, x + w * 0.31, base - h * 0.30, '#5A403C')
    L.rect(x + w * 0.58, base - h * 0.55, x + w * 0.80, base, '#4A3430')
    L.poly([(x - 20, base), (x + w + 20, base), (x + w + 30, base + 26), (x - 30, base + 26)], SNOW, rim=0.6)


HOUSES = [(-90, 1300, 300, 220, '#9C5B4A', 0), (300, 1215, 150, 110, '#7D5A80', 1), (690, 1215, 150, 110, '#8A6A5A', 2),
          (860, 1300, 300, 220, '#6E7FA0', 3)]


def build_village(variant='dawn'):
    its = []
    its.append(item(sky(920, '#3A3F74', [(420, '#5E5590', 30), (700, '#B97A9A', 24), (900, '#EBA58C', 18), (1040, '#F7CFA0', 12)]),
                    10, 0, key='vil-sky'))
    far = Layer(W, H, seed=921)
    far.poly([(-60, 1180), (160, 960), (330, 1090), (560, 820), (700, 960), (820, 900), (1140, 1180), (1140, H), (-60, H)], '#8E8CB8',
             crease=[((560, 820), (600, 1180), 0.12)])
    far.poly([(510, 870), (560, 820), (610, 868), (585, 880), (560, 862), (535, 885)], SNOW)
    far.poly([(120, 1000), (160, 960), (200, 996), (165, 990)], SNOW)
    far.ellipse(560, 960, 26, 20, '#2A2E55')
    its.append(item(far, 8.5, 0.8, key='vil-far'))
    mid = Layer(W, H, seed=922)
    ridge(mid, 1240, 70, 9, '#C9CFE6')
    for i in range(9):
        pine(mid, 30 + i * 130, 1250, 170 + 30 * (i % 3), 90, '#5C7A8E', '#E4EAF4', 3)
    its.append(item(mid, 6.5, 0.8, key='vil-mid'))
    for k, (x, b, w_, h_, col, s) in enumerate(HOUSES):
        L = Layer(W, H, seed=930 + k)
        cottage(L, x, b, w_, h_, col, s)
        z = 4.2 if w_ > 200 else 5.4
        its.append(item(L, z, 1.0, key=f'vil-house{k}'))
    gnd = Layer(W, H, seed=940)
    gnd.poly([(-60, 1230), (1140, 1230), (1140, H + 20), (-60, H + 20)], SNOW2)
    gnd.poly([(470, 1230), (610, 1230), (1000, H + 20), (80, H + 20)], SNOW, grad=0.12)
    for xo in (-1, 1):
        gnd.stroke([(540 + xo * 26, 1235), (540 + xo * 150, 1600), (540 + xo * 300, H + 20)], SNOW3, 10, alpha=0.6)
    for i in range(6):
        gnd.rect(30 + i * 60, 1420 - 10 * i, 44 + i * 60, 1560 - 10 * i, '#6B4A3A')
        gnd.rect(24 + i * 60, 1408 - 10 * i, 50 + i * 60, 1426 - 10 * i, SNOW)
    its.append(item(gnd, 2.4, 0.4, key='vil-ground'))
    r = np.random.default_rng(7)
    flakes = [(r.uniform(0, W), r.uniform(0, H), r.uniform(0.3, 1.0), r.uniform(0, 6)) for _ in range(30)]

    def glows(t):
        g = [(560, 1060, 520, '#FFC98A', 0.22), (560, 960, 34, CYAN, 0.35 + 0.15 * math.sin(t * 3)),
             (110, 1180, 90, '#FFB060', 0.18), (950, 1180, 90, '#FFB060', 0.18)]
        for (x, y, sp, ph) in flakes:
            yy = (y + 70 * sp * t) % H
            g.append((x + 24 * math.sin(t * sp + ph), yy, 5 * sp + 2, '#FFFFFF', 0.55))
        return g
    return dict(items=its, glows=glows, floor=1700, focus=2.4, light='dawn', marks={'C': 540})


def draw_village(sc, S, t, ev):
    for k, (x, b, w_, h_, col, s) in enumerate(HOUSES):
        cx, cy = x + w_ * 0.69, b - h_ - h_ * 0.66
        z = 4.2 if w_ > 200 else 5.4
        for i in range(4):
            ph = (t * 0.35 + i / 4 + k * 0.3) % 1.0
            place(S, 'smoke', lambda: [E(0, 0, 30, 22, '#E7E2EC', alpha=0.85)], cx + 30 * ph + 8 * math.sin(ph * 7),
                  cy - 200 * ph, z - 0.05, 0, round((0.5 + 1.2 * ph) * 5) / 5, lift=0.1)


def pov_village(sc, S, t, ev, cam):
    d0, d1 = ev['door']
    u = sm((t - d0) / (d1 - d0))
    if u < 1:
        def panel(side):
            sh = [P([(0, 0), (560, 0), (560, 1920), (0, 1920)], '#6E4B36', pat='planks', pat_period=92)]
            sh += [P([(40, 160), (520, 160), (520, 820), (40, 820)], '#7A5640', pat='planks', pat_period=92),
                   P([(40, 1000), (520, 1000), (520, 1760), (40, 1760)], '#7A5640', pat='planks', pat_period=92)]
            hx = 470 if side < 0 else 90
            sh += [E(hx, 960, 22, 22, '#3A3A40'), P([(hx - 8, 960), (hx + 8, 960), (hx + 8, 1060), (hx - 8, 1060)], '#2E2E34')]
            return sh
        off = 620 * u
        place(S, 'doorL', lambda: panel(-1), -20 - off, 0, 2.0, 0, 1.0, lift=1.2, seed=81)
        place(S, 'doorR', lambda: panel(1), 540 + off, 0, 2.0, 0, 1.0, lift=1.2, seed=82)
        # both hands push the doors open
        hu = sm((t - (d0 - 0.4)) / 0.4)
        put_hand(S, -1, 380 - off * 0.8, 1250 + 400 * (1 - hu) + 60 * u, ang=8)
        put_hand(S, 1, 700 + off * 0.8, 1250 + 400 * (1 - hu) + 60 * u, ang=-8)
    pov_breath(S, t, ev)


def pov_breath(S, t, ev):
    for b in ev.get('breath', []):
        if b <= t < b + 1.4:
            u = (t - b) / 1.4
            for i in range(5):
                v = max(0.0, u - i * 0.05)
                x = 540 + (i - 2) * 30 * v + 16 * math.sin(i + v * 5)
                y = 1760 - 520 * v - i * 20
                a = (1 - v) ** 1.5 * sm(v / 0.1)
                if a > 0.03:
                    place(S, f'breath{int(a * 8)}', lambda a=a: [E(0, 0, 60, 40, '#F4F8FF', alpha=round(a * 8) / 8 * 0.8)],
                          x, y, 2.0, 0, round((0.7 + 2.2 * v) * 5) / 5, lift=0.0)


# ================================================================== SET: frozen river
def build_river(variant='day'):
    its = []
    its.append(item(sky(950, '#8FAAD6', [(520, '#A7BEE0', 26), (700, '#C6D6EC', 18), (840, '#E6EEF6', 10)]), 10, 0, key='riv-sky'))
    far = Layer(W, H, seed=951)
    ridge(far, 940, 170, 11, '#B7C4E0', snowcap=SNOW)
    its.append(item(far, 8.0, 0.8, key='riv-far'))
    fb = Layer(W, H, seed=954)
    fb.poly([(-60, 1070), (300, 1050), (700, 1075), (1140, 1050), (1140, 1210), (-60, 1210)], SNOW, grad=0.1)
    for i in range(11):
        pine(fb, -10 + i * 110, 1110 + 14 * (i % 2), 230 + 60 * (i % 3), 120, PINE2 if i % 2 else PINE)
    its.append(item(fb, 3.6, 0.8, key='riv-farbank'))
    ice = Layer(W, H, seed=952)
    xs = np.arange(-60, W + 70, 20, dtype=np.float32)
    top = 1170 + 10 * np.sin(xs / 90)
    bot = 1700 + 16 * np.sin(xs / 130 + 1)
    ice.poly(np.concatenate([np.stack([xs, top], 1), np.stack([xs[::-1], bot[::-1]], 1)]), ICE, grad=0.18)
    r = np.random.default_rng(5)
    for _ in range(30):
        y = r.uniform(1190, 1680)
        x = r.uniform(-20, W + 20)
        ln = 40 + (y - 1170) * 0.4
        ice.stroke([(x - ln, y), (x + ln, y + r.uniform(-5, 5))], ICE2, 3 + (y - 1170) / 80, alpha=0.8)
    for _ in range(18):
        y = r.uniform(1200, 1670)
        ice.ellipse(r.uniform(0, W), y, 6 + (y - 1170) / 30, 3 + (y - 1170) / 80, '#E9F7FC', paint=True, alpha=0.7)
    its.append(item(ice, 2.6, 0.2, key='riv-ice'))
    nb = Layer(W, H, seed=953)
    nb.poly([(-60, 1690), (200, 1660), (480, 1700), (760, 1670), (1140, 1700), (1140, H + 40), (-60, H + 40)], SNOW, grad=0.1)
    for i in range(6):
        nb.ellipse(90 + i * 180, 1760 + 30 * (i % 2), 70, 16, SNOW3, paint=True, alpha=0.4)
    its.append(item(nb, 2.2, 0.5, key='riv-nearbank'))

    def glows(t):
        return [(540, 720, 600, '#FFFFFF', 0.10), (300, 1450, 40, '#FFFFFF', 0.35 + 0.2 * math.sin(t * 2)),
                (760, 1330, 30, '#FFFFFF', 0.30 + 0.2 * math.sin(t * 2.6 + 1))]
    return dict(items=its, glows=glows, floor=1700, focus=2.6, light='snow', marks={'C': 540})


CRACK = [(120, 1650), (260, 1580), (380, 1530), (520, 1450), (640, 1400), (760, 1300), (900, 1230)]
BRANCH = [[(260, 1580), (200, 1490), (230, 1400)], [(520, 1450), (600, 1560), (720, 1600)], [(640, 1400), (560, 1300)]]


def draw_river(sc, S, t, ev):
    c0, c1 = ev['crack']
    if t >= c0:
        u = sm((t - c0) / (c1 - c0))
        key = round(u, 2)

        def mk():
            L = Layer(W, H, seed=960)
            q = partial(CRACK, u)
            if len(q) >= 2:
                L.stroke(q + [3, 3], ICE4, 9, alpha=0.8)
                L.stroke(q, '#F6FDFF', 6)
            for b in BRANCH:
                bu = max(0.0, u * 1.6 - 0.5)
                qb = partial(b, bu)
                if len(qb) >= 2 and bu > 0:
                    L.stroke(qb + [2, 2], ICE4, 6, alpha=0.8)
                    L.stroke(qb, '#F6FDFF', 4)
            return L
        S.add(cache(('crack', key), mk), 2.55, 0.0, 0, 0, key=f'crack{key}{paperkit.K}')


# ================================================================== SET: snowy woods with glowing drips
DRIPS = [(565, 1760), (520, 1610), (555, 1480), (528, 1370), (548, 1280), (536, 1205), (545, 1150)]


def build_woods(variant='day'):
    its = []
    its.append(item(sky(970, '#A9BCDA', [(620, '#BCCBE3', 20), (820, '#D2DDEC', 14)]), 10, 0, key='wd-sky'))
    far = Layer(W, H, seed=971)
    far.poly([(-60, 1150), (100, 900), (260, 980), (420, 720), (540, 560), (680, 740), (820, 860), (980, 780), (1140, 1150)], '#9EA3C8',
             crease=[((540, 560), (560, 1150), 0.12), ((420, 720), (440, 1150), 0.10)])
    far.poly([(450, 650), (540, 560), (625, 650), (590, 680), (545, 640), (500, 690)], SNOW)
    far.poly([(940, 820), (980, 780), (1020, 820)], SNOW)
    far.poly([(70, 940), (100, 900), (130, 930)], SNOW)
    far.poly(ellipse_pts(545, 1040, 52, 60, 0, a0=math.pi, a1=2 * math.pi), '#252A50')
    far.rect(493, 1040, 597, 1080, '#252A50')
    its.append(item(far, 9.0, 0.6, key='wd-far'))
    for k, (z, n, base, hh, col, seed) in enumerate([(7.0, 9, 1180, 330, '#6F96A0', 3), (5.0, 7, 1260, 520, PINE3, 4),
                                                     (3.4, 5, 1380, 820, PINE, 5)]):
        L = Layer(W, H, seed=972 + k)
        r = np.random.default_rng(seed)
        xs = np.linspace(-40, W + 40, n) + r.uniform(-40, 40, n)
        for x in xs:
            if abs(x - 545) < 120 + 60 * k:
                continue
            pine(L, x, base + r.uniform(-20, 20), hh * r.uniform(0.85, 1.1), hh * 0.5, col)
        its.append(item(L, z, 1.0, key=f'wd-pines{k}'))
    gnd = Layer(W, H, seed=980)
    gnd.poly([(-60, 1150), (1140, 1150), (1140, H + 20), (-60, H + 20)], SNOW)
    gnd.poly([(500, 1150), (590, 1150), (820, H + 20), (300, H + 20)], SNOW2, alpha=0.85)
    for (x, y) in DRIPS:
        sc_ = 0.4 + (y - 1100) / 700
        gnd.ellipse(x, y, 16 * sc_, 7 * sc_, '#B7F6FF', glow=0.35)
    its.append(item(gnd, 2.4, 0.3, key='wd-ground'))
    fg = Layer(W, H, seed=981)
    fg.poly([(-80, H + 20), (-80, -40), (70, -40), (110, H + 20)], '#3A3040', pat='vstripes', pat_period=22)
    fg.poly([(1000, -40), (1160, -40), (1160, H + 20), (960, H + 20)], '#3A3040', pat='vstripes', pat_period=22)
    its.append(item(fg, 1.1, 1.0, key='wd-fg'))

    def glows(t):
        g = [(545, 1050, 90, CYAN, 0.30 + 0.1 * math.sin(t * 2))]
        for i, (x, y) in enumerate(DRIPS):
            p = 0.5 + 0.5 * math.sin(t * 2.4 - i * 0.9)
            g.append((x, y, 30 + 30 * (y - 1100) / 700, CYAN, 0.30 + 0.35 * p))
        return g
    return dict(items=its, glows=glows, floor=1700, focus=2.4, light='snow', marks={'C': 540})


def bough_shapes():
    sh = [P([(-200, 20), (420, -30), (430, 10), (-200, 70)], '#4A3A34')]
    for i in range(9):
        x = -120 + i * 62
        sh.append(P([(x - 70, 30 + i * -5), (x, 160 - i * 4), (x + 70, 26 - i * 5)], PINE2 if i % 2 else PINE))
    sh.append(P([(-160, 0), (0, -50), (200, -60), (380, -80), (420, -30), (200, 10), (0, 30)], SNOW))
    return sh


def clump_shapes():
    return [E(0, 0, 130, 70, SNOW), E(-60, -20, 70, 50, SNOW), E(70, -14, 80, 52, '#F7FAFF')]


def draw_woods(sc, S, t, ev):
    f0 = ev['fall']
    place(S, 'bough', bough_shapes, 260, -40, 1.3, 0, 1.0, lift=1.4, seed=91)
    if t < f0 + 0.4:
        u = max(0.0, (t - f0) / 0.4)
        place(S, 'clump', clump_shapes, 380, 10 + 1200 * u * u, 1.2, 0, 1.0, lift=1.6, seed=92)


def pov_woods(sc, S, t, ev, cam):
    s0 = ev['splat']
    if s0 <= t < s0 + 1.2:
        u = (t - s0) / 1.2
        y = -400 + 2300 * sm((u - 0.3) / 0.7) ** 1.4
        def splat():
            r = np.random.default_rng(3)
            sh = [P([(-40, -40), (1120, -40), (1120, 1900), (-40, 1960)], SNOW)]
            for i in range(16):
                sh.append(E(r.uniform(0, 1080), 1900 + r.uniform(-60, 80), r.uniform(60, 130), r.uniform(50, 100), SNOW if i % 2 else '#F7FAFF'))
            for i in range(40):
                sh.append(E(r.uniform(0, 1080), r.uniform(0, 1850), r.uniform(30, 90), r.uniform(20, 60), [SNOW2, '#F9FBFF', '#E2E9F4'][i % 3]))
            return sh
        place(S, 'splat', splat, 0, y, 2.0, 0, 1.0, lift=1.0, seed=93)
    sw = ev['swipe']
    if sw - 0.3 <= t < sw + 0.6:
        u = sm((t - sw + 0.3) / 0.9)
        put_hand(S, 1, lerp(1100, -80, u), 700 + 300 * math.sin(u * math.pi) * 0.3, ang=-70)
    pov_breath(S, t, ev)


# ================================================================== SET: cave mouth behind an icicle curtain
ICICLES = [(x, 560 + 40 * math.sin(x * 0.07), 220 + 300 * abs(math.sin(x * 0.031)) + 80 * (i % 3)) for i, x in enumerate(range(150, 950, 46))]


def build_cave_mouth(variant='day'):
    its = []
    its.append(item(sky(990, '#9DB4DA', [(500, '#B5C8E4', 18)]), 10, 0, key='cm-sky'))
    rock = Layer(W, H, seed=991)
    r = np.random.default_rng(8)
    rock.poly([(-40, 420), (120, 300), (260, 360), (420, 160), (560, 60), (700, 200), (860, 120), (1120, 330), (1120, 1500), (-40, 1500)], '#6E7198')
    for _ in range(70):
        x, y = r.uniform(-60, W + 60), r.uniform(180, 1500)
        pts = [(x + r.uniform(-130, 130), y + r.uniform(-110, 110)) for _ in range(4)]
        rock.poly(pts, ['#7C7FA6', '#6A6D94', '#8E91B6', '#5E6188'][r.integers(4)])
    rock.poly([(420, 160), (560, 60), (700, 200), (650, 190), (560, 120), (480, 200)], SNOW)
    rock.poly([(-40, 420), (120, 300), (260, 360), (200, 380), (120, 340), (20, 430)], SNOW)
    rock.poly(ellipse_pts(540, 1060, 290, 480, 0, a0=math.pi, a1=2 * math.pi), '#1C2240')
    rock.rect(250, 1060, 830, 1460, '#1C2240')
    rock.poly(ellipse_pts(540, 1080, 190, 330, 0, a0=math.pi, a1=2 * math.pi), '#2B3A6A', alpha=0.8)
    rock.rect(350, 1080, 730, 1460, '#2B3A6A', alpha=0.8)
    its.append(item(rock, 4.0, 1.0, key='cm-rock'))
    gnd = Layer(W, H, seed=992)
    gnd.poly([(-60, 1400), (300, 1380), (540, 1420), (800, 1370), (1140, 1400), (1140, H + 20), (-60, H + 20)], SNOW, grad=0.1)
    gnd.poly([(380, 1420), (700, 1420), (900, H + 20), (180, H + 20)], SNOW2, alpha=0.7)
    its.append(item(gnd, 2.4, 0.4, key='cm-ground'))

    def glows(t):
        return [(540, 1150, 260, CYAN, 0.30 + 0.08 * math.sin(t * 2.2)), (540, 1180, 90, '#BFFFE6', 0.25)]
    return dict(items=its, glows=glows, floor=1700, focus=2.4, light='snow', marks={'C': 540})


def icicle_shapes(ln):
    return [P([(-16, 0), (16, 0), (0, ln)], ICE2, glow=0.08, crease=[((0, 0), (0, ln), 0.18)]),
            P([(-6, 10), (2, 10), (-2, ln * 0.7)], '#FFFFFF', paint=True, alpha=0.6)]


def draw_cave_mouth(sc, S, t, ev):
    p0, p1 = ev['push']
    for i, (x, y, ln) in enumerate(ICICLES):
        dx = 0.0
        if t >= p0:
            u = (t - p0) / (p1 - p0)
            side = -1 if x < 540 else 1
            reach = max(0.0, 1 - abs(x - 540) / 380)
            push = 260 * reach * sm(u / 0.5)
            wob = 22 * reach * math.exp(-max(0.0, t - p0 - 0.3) * 3) * math.sin((t - p0) * 18 + i)
            dx = side * push + wob
        ln_q = int(ln // 20 * 20)
        place(S, f'icicle{ln_q}', lambda ln_q=ln_q: icicle_shapes(ln_q), x + dx, y, 1.9, dx * 0.04, 1.0, lift=0.8, seed=100 + ln_q)
    rod = cache('cm-rod', lambda: _rod())
    S.add(rod, 1.9, 0.6, 0, 450, key='cm-rod' + str(paperkit.K))


def _rod():
    L = Layer(W, 200, seed=995)
    L.poly([(-40, 70), (160, 40), (380, 80), (560, 50), (760, 86), (980, 46), (W + 40, 70), (W + 40, 120), (820, 132), (540, 112), (240, 130), (-40, 118)], '#5A5D86')
    L.poly([(-40, 50), (180, 24), (400, 58), (600, 30), (800, 64), (1000, 28), (W + 40, 50), (W + 40, 84), (700, 92), (300, 88), (-40, 86)], SNOW)
    return L


def pov_lantern(S, t, l0, x=210, y=1250):
    if t < l0 - 0.5:
        return []
    u = sm((t - (l0 - 0.5)) / 0.5)
    sway = 10 * math.sin(t * 2.3)
    lx, ly = x + sway, y + 500 * (1 - u)
    place(S, 'lantern', lantern_shapes, lx, ly, 2.0, sway * 0.4, 1.0, lift=1.0, seed=111)
    put_hand(S, -1, lx, ly + 60, ang=6)
    on = sm((t - l0) / 0.12)
    if on <= 0:
        return []
    fl = 0.9 + 0.1 * math.sin(t * 17) * math.sin(t * 5.3)
    return [(lx, ly + 120, 120, '#FFD27A', 0.55 * on * fl), (lx, ly + 120, 520, '#FFB050', 0.20 * on * fl)]


def pov_cave_mouth(sc, S, t, ev, cam):
    p0, p1 = ev['push']
    g = []
    if p0 - 0.5 < t < p1 + 0.3:
        u = sm((t - (p0 - 0.5)) / 0.5) if t < p0 + 0.6 else 1 - sm((t - p0 - 0.6) / (p1 - p0 - 0.3))
        put_hand(S, 1, 560 + 120 * sm((t - p0) / 0.6), 1500 - 520 * u, ang=-6)
    g += pov_lantern(S, t, ev['lantern'])
    return g


# ================================================================== SET: the ice wall (bamboo frozen inside)
def build_ice_wall(variant='day'):
    its = []
    back = Layer(W, H, seed=1001)
    back.rect(-40, -40, W + 40, H + 40, '#1E2A52', rim=0, shadow=0)
    r = np.random.default_rng(12)
    for _ in range(40):
        x, y = r.uniform(-60, W + 60), r.uniform(-60, H + 60)
        back.poly([(x + r.uniform(-160, 160), y + r.uniform(-200, 200)) for _ in range(4)], ['#25356A', '#2C4078', '#1A254A'][r.integers(3)])
    its.append(item(back, 4.0, 0.6, key='iw-back'))
    bam = Layer(W, H, seed=1002)
    for (x, top, w_, sh) in [(380, 620, 64, 0.85), (700, 700, 60, 0.85), (540, 480, 96, 1.0)]:
        bam.poly([(x - w_ / 2, 1700), (x - w_ / 2, top), (x + w_ / 2, top), (x + w_ / 2, 1700)], JADE, shade=sh, glow=0.12,
                 crease=[((x, top), (x, 1700), 0.16)])
        for ny in range(top + 160, 1700, 260):
            bam.rect(x - w_ / 2 - 6, ny, x + w_ / 2 + 6, ny + 16, JADE3, shade=sh)
        bam.ellipse(x, top, w_ / 2, 12, JADE2, shade=sh)
        bam.poly([(x + w_ / 2, top + 300), (x + w_ / 2 + 90, top + 230), (x + w_ / 2 + 60, top + 270)], JADE2)
    its.append(item(bam, 3.0, 0.6, key='iw-bamboo'))
    ice = Layer(W, H, seed=1003)
    for _ in range(46):
        x, y = r.uniform(-60, W + 60), r.uniform(-60, H + 60)
        ice.poly([(x + r.uniform(-170, 170), y + r.uniform(-220, 220)) for _ in range(4)],
                 [ICE, ICE2, ICE3][r.integers(3)], alpha=0.36, rim=0.6)
    its.append(item(ice, 2.2, 0.3, key='iw-ice'))

    def glows(t):
        p = 0.5 + 0.5 * math.sin(t * 2.0)
        return [(540, 900, 320, '#9FFFD6', 0.26 + 0.1 * p), (540, 700, 140, '#DFFFF0', 0.2), (380, 1000, 120, '#9FFFD6', 0.14),
                (700, 1050, 120, '#9FFFD6', 0.14)]
    return dict(items=its, glows=glows, floor=1700, focus=2.2, light='ice', marks={'C': 540})


FROST = None


def frost_specks():
    r = np.random.default_rng(21)
    return [(r.uniform(-40, W + 40), r.uniform(-40, H + 40), r.uniform(50, 120), r.uniform(10, 30), r.uniform(0, 3.1)) for _ in range(520)]


def draw_ice_wall(sc, S, t, ev):
    r0, r1 = ev['rub']
    rad = 0 if t < r0 else 470 * sm((t - r0) / (r1 - r0)) ** 0.8
    key = int(rad // 12)

    def mk():
        L = Layer(W, H, seed=1010, grain=0.12)
        for (x, y, a, b, rot) in cache('frost-specks', frost_specks):
            d = math.hypot(x - 540, (y - 980) * 0.8)
            if d < key * 12 - 40:
                continue
            al = 0.62 if d > key * 12 + 60 else 0.35
            c_, s_ = math.cos(rot), math.sin(rot)
            L.poly([(x - a * c_, y - a * s_), (x - b * s_, y + b * c_), (x + a * c_, y + a * s_), (x + b * s_, y - b * c_)],
                   ['#E6F2FA', '#F5FAFF', '#D2E6F4'][int(a) % 3], alpha=al, rim=0.4, shadow=0.2)
        return L
    S.add(cache(('frost', key), mk), 2.0, 0.2, 0, 0, key=f'frost{key}{paperkit.K}')
    for i in range(4):  # steam rising inside the ice from the bamboo top
        ph = (t * 0.4 + i / 4) % 1.0
        al = round((1 - ph) * sm(ph / 0.15) * 5) / 5
        place(S, f'iwsteam{al}', lambda al=al: [E(0, 0, 16, 54, '#E9FFF6', alpha=0.6 * al)], 540 + 30 * math.sin(ph * 6 + i), 470 - 280 * ph, 2.6,
              20 * math.sin(ph * 5 + i), round((0.7 + 1.0 * ph) * 5) / 5, lift=0.0)


def pov_ice_wall(sc, S, t, ev, cam):
    g = pov_lantern(S, t, ev['lantern'], x=170, y=1270)
    r0, r1 = ev['rub']
    if r0 - 0.4 < t < r1 + 0.4:
        u = sm((t - (r0 - 0.4)) / 0.4) if t < r1 else 1 - sm((t - r1) / 0.4)
        k = (t - r0) * 2 * math.pi * 1.6
        rr = 60 + 160 * sm((t - r0) / (r1 - r0))
        hx = 560 + rr * math.cos(k)
        hy = 1030 + rr * 0.6 * math.sin(k) + 700 * (1 - u)
        put_hand(S, 1, hx, hy + 120, ang=-10 + 8 * math.sin(k))
    return g


# ================================================================== SET: close-up of the bamboo (payoff)
def build_bamboo(variant='day'):
    its = []
    back = Layer(W, H, seed=1101)
    back.rect(-40, -40, W + 40, H + 40, '#22305C', rim=0, shadow=0)
    r = np.random.default_rng(14)
    for _ in range(40):
        x, y = r.uniform(-60, W + 60), r.uniform(-60, H + 60)
        back.poly([(x + r.uniform(-200, 200), y + r.uniform(-220, 220)) for _ in range(4)], ['#2A3C70', '#33498A', '#1D2A52'][r.integers(3)])
    its.append(item(back, 5.0, 0.6, key='bc-back'))
    stalk = Layer(W, H, seed=1102)
    stalk.poly([(400, H + 40), (400, 980), (680, 980), (680, H + 40)], JADE, glow=0.10, crease=[((540, 980), (540, H), 0.16)],
               pat='vstripes', pat_period=46)
    stalk.rect(388, 1300, 692, 1340, JADE3)
    stalk.rect(388, 960, 692, 1000, JADE3)
    stalk.ellipse(540, 980, 152, 34, JADE3)       # rim of the opened cup (hidden under the cap until the snap)
    stalk.ellipse(540, 984, 132, 26, '#F6F0DA', glow=0.12)
    stalk.ellipse(520, 980, 50, 10, '#FFFFFF', paint=True, alpha=0.6)
    stalk.ellipse(570, 986, 40, 8, JADE, paint=True, alpha=0.6)
    its.append(item(stalk, 2.3, 0.8, key='bc-stalk'))
    gnd = Layer(W, H, seed=1103)
    gnd.poly([(-60, 1560), (1140, 1540), (1140, H + 20), (-60, H + 20)], '#C7DDF0', grad=0.1)
    its.append(item(gnd, 2.6, 0.3, key='bc-ground'))

    def glows(t):
        return [(540, 980, 260, '#AFFFE0', 0.24), (540, 700, 420, '#7FD8FF', 0.10)]
    return dict(items=its, glows=glows, floor=1700, focus=2.3, light='ice', marks={'C': 540})


def cap_shapes():
    """The bamboo segment above the cup (it snaps off)."""
    return [P([(-140, 0), (140, 0), (140, -700), (-140, -700)], JADE, glow=0.10, crease=[((0, 0), (0, -700), 0.16)], pat='vstripes', pat_period=46),
            P([(-152, -360), (152, -360), (152, -320), (-152, -320)], JADE3),
            P([(-150, -20), (150, -20), (150, 20), (-150, 20)], JADE3)]


SHARDS = None


def shard_list():
    r = np.random.default_rng(31)
    out = []
    for i in range(26):
        x, y = r.uniform(330, 750), r.uniform(420, 1520)
        pts = [(r.uniform(-90, 90), r.uniform(-110, 110)) for _ in range(4)]
        vx = (x - 540) * r.uniform(2.5, 5.0) + r.uniform(-200, 200)
        vy = r.uniform(-700, -150)
        out.append((x, y, pts, vx, vy, r.uniform(-300, 300), i))
    return out


def draw_bamboo(sc, S, t, ev):
    taps, shat = ev['taps'], ev['shatter']
    s0 = ev['snap']
    # cap: sits on the cup until the snap, then flies up-right
    u = sm((t - s0) / 0.6) if t >= s0 else 0.0
    if u < 1:
        place(S, 'cap', cap_shapes, 540 + 700 * u * u, 990 - 300 * u + 900 * u * u * u, 2.25, 40 * u, 1.0, lift=1.0, seed=121)
    # wobbling pudding surface after the snap
    if t >= s0 + 0.1:
        w = math.exp(-max(0.0, t - s0 - 0.2) * 2.6) * math.sin((t - s0) * 22)
        dome = 1.0 + 0.30 * w
        scoop = ev['scoop']
        gone = t >= scoop + 0.15
        def pud(dome=round(dome, 2), gone=gone):
            sh = [E(0, 0, 132, 26 + 22 * dome, '#F6F0DA', glow=0.12), E(-30, -10 * dome, 46, 10, '#FFFFFF', paint=True, alpha=0.7),
                  E(36, 4, 36, 8, JADE, paint=True, alpha=0.7)]
            if gone:
                sh.append(E(20, 2, 46, 16, '#D9CDA8'))
            return sh
        place(S, f'pud{int(gone)}_{round(dome, 2)}', pud, 540, 982 - 10 * dome, 2.29, 0, 1.0, lift=0.2, seed=122)
    # ice shell around the stalk: whole -> cracked -> shattered
    if t < shat:
        nc = sum(1 for x in taps if t >= x)
        L = cache(('shell', nc), lambda: _shell(nc))
        S.add(L, 2.1, 0.4, 0, 0, key=f'shell{nc}{paperkit.K}')
    elif t < shat + 1.2:
        dt = t - shat
        for (x, y, pts, vx, vy, vr, i) in cache('shards', shard_list):
            px, py = x + vx * dt, y + vy * dt + 1600 * dt * dt
            place(S, f'shard{i}', lambda pts=pts: [P(pts, ICE2, alpha=0.8, glow=0.1)], px, py, 2.0, vr * dt, 1.0, lift=0.8, seed=130 + i)
    # steam burst when the ice breaks and when the cap comes off
    for b0, n, y0 in ((shat, 6, 560), (s0, 8, 900)):
        if b0 <= t < b0 + 2.4:
            for i in range(n):
                ph = (t - b0) / 2.4 + i * 0.04
                if ph > 1:
                    continue
                al = round((1 - ph) * sm(ph / 0.1) * 6) / 6
                if al <= 0:
                    continue
                place(S, f'steam{al}', lambda al=al: [E(0, 0, 18, 60, '#F2FFFA', alpha=0.55 * al), E(14, -50, 12, 40, '#F2FFFA', alpha=0.4 * al)],
                      540 + (i - n / 2) * 22 + 50 * math.sin(ph * 5 + i), y0 - 420 * ph, 1.8, 25 * math.sin(ph * 4 + i), round((0.7 + 1.2 * ph) * 5) / 5, lift=0.0)


def _shell(nc):
    L = Layer(W, H, seed=1110 + nc)
    r = np.random.default_rng(40)
    for _ in range(34):
        x, y = r.uniform(300, 780), r.uniform(380, 1560)
        L.poly([(x + r.uniform(-120, 120), y + r.uniform(-140, 140)) for _ in range(4)], [ICE, ICE2, ICE3][r.integers(3)], alpha=0.42, rim=0.6)
    cracks = [[(610, 960), (660, 860), (640, 760), (700, 650)], [(610, 960), (520, 900), (470, 780)], [(610, 960), (700, 1080), (760, 1180)],
              [(610, 960), (560, 1100), (600, 1260)], [(470, 780), (400, 700)], [(700, 650), (760, 560)]]
    for c in cracks[:2 + 2 * nc] if nc else []:
        L.stroke(np.array(c, np.float32) + [2, 2], ICE4, 7, alpha=0.8)
        L.stroke(c, '#F8FEFF', 5)
    return L


def pov_bamboo(sc, S, t, ev, cam):
    g = []
    taps, shat, s0, scoop, bite = ev['taps'], ev['shatter'], ev['snap'], ev['scoop'], ev['bite']
    # spoon taps the ice (tip lands on the crack point)
    if taps[0] - 0.6 < t < shat + 0.4:
        u = sm((t - (taps[0] - 0.6)) / 0.5) if t < shat else 1 - sm((t - shat) / 0.4)
        back = min([abs(t - x) for x in taps + [shat]])
        pull = 120 * (1 - math.exp(-(back / 0.12) ** 2))
        tx, ty = 610 + pull * 0.6, 960 + pull
        place(S, 'spoon', spoon_shapes, tx, ty + 700 * (1 - u), 2.0, -26, 1.0, lift=1.0, seed=141)
        put_hand(S, 1, tx + 190, ty + 470 + 700 * (1 - u), ang=-26)
    # left hand snaps the cap off
    if s0 - 0.6 < t < s0 + 0.5:
        u = sm((t - (s0 - 0.6)) / 0.5) if t < s0 else 1 - sm((t - s0) / 0.5)
        put_hand(S, -1, 380 + 20 * u, 900 + 900 * (1 - u), ang=24)
    # scoop, then the spoon comes to you
    if scoop - 0.6 < t < bite + 0.15:
        if t < scoop:
            u = sm((t - (scoop - 0.6)) / 0.6)
            x, y, s = 560, 960 + 800 * (1 - u), 1.0
            full = False
        else:
            v = sm((t - scoop - 0.25) / (bite - scoop - 0.25))
            x = lerp(560, 540, v)
            y = lerp(960, 1300, v ** 1.6) - 40 * math.sin(min(1.0, (t - scoop) / 0.25) * math.pi)
            s = lerp(1.0, 2.6, v ** 2)
            full = True
        place(S, 'spoonF' if full else 'spoon', spoon_full_shapes if full else spoon_shapes, x, y, 2.0, -8 if full else -20, round(s * 10) / 10, lift=1.0, seed=142)
        put_hand(S, 1, x + 120 * s, y + 470 * s, ang=-14, s=round(s * 10) / 10)
    if t >= bite:
        v = (t - bite)
        r = np.random.default_rng(5)
        for i in range(18):
            ph = v * 0.6 + r.random()
            g.append((r.uniform(120, 960), 1700 - 900 * (ph % 1.0), 10, '#FFE9A8', 0.9 * math.exp(-v * 0.6) * (0.5 + 0.5 * math.sin(v * 6 + i))))
        g.append((540, 1100, 900, '#FFD58A', 0.35 * math.exp(-v * 0.9)))
    return g


# ================================================================== wiring
def register(CAST, rigs, POSES, SETS):
    for name, fn, variants in [('trip_map', build_map, ['home', 'woods', 'cave']), ('snow_village', build_village, ['dawn']),
                               ('ice_river', build_river, ['day']), ('snow_woods', build_woods, ['day']),
                               ('cave_mouth', build_cave_mouth, ['day']), ('ice_wall', build_ice_wall, ['day']),
                               ('bamboo_close', build_bamboo, ['day'])]:
        if isinstance(SETS, dict):   # lint.py passes the sets table itself
            SETS[name] = fn
        else:                        # director passes the sets module
            SETS.SETS[name] = fn
            SETS.VARIANTS[name] = variants


DRAW = {'trip_map': draw_map, 'snow_village': draw_village, 'ice_river': draw_river, 'snow_woods': draw_woods,
        'cave_mouth': draw_cave_mouth, 'ice_wall': draw_ice_wall, 'bamboo_close': draw_bamboo}
POV = {'trip_map': pov_map, 'snow_village': pov_village, 'snow_woods': pov_woods, 'cave_mouth': pov_cave_mouth,
       'ice_wall': pov_ice_wall, 'bamboo_close': pov_bamboo}


def draw(scene, S, t, ctx):
    f = DRAW.get(scene['set'])
    if f:
        return f(scene, S, t, scene.get('ev', {}))


def pov(scene, S, t, ctx):
    f = POV.get(scene['set'])
    if f:
        return f(scene, S, t, scene.get('ev', {}), ctx['cam'])
    return pov_breath(S, t, scene.get('ev', {}))
