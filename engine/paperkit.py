"""paperkit - 2.5D cut-paper diorama renderer (numpy + OpenCV). Original code.

Everything is written in LOGICAL coordinates (1080 x 1920 frame). set_res(k)
renders at k x that size (k=0.5 for fast previews) without changing any numbers.

Paper look, per piece (Layer.poly):
  rough cut edges · paper grain + fibres · light "cut edge" on the lit side ·
  darker edge on the shadow side · soft drop shadow onto paper below ·
  fold creases · printed patterns (stripes, newsprint, planks).
Diorama look, per layer (Scene):
  each layer floats at depth z; casts a soft shadow on layers behind it
  (lift = how high it floats); depth-of-field blur grows with distance from
  the focus plane; camera pan/zoom moves near layers more (parallax).
Images are float32 premultiplied RGBA.
"""
import math
import numpy as np
import cv2

K = 1.0                                   # render scale (1 = 1080x1920)
LIGHT = np.array([0.55, 0.835], np.float32)  # direction light travels (to lower-right)


def set_res(k):
    global K
    K = float(k)
    _GRAIN.clear()
    _PREP.clear()


def set_light(dx, dy):
    global LIGHT
    v = np.array([dx, dy], np.float32)
    LIGHT = v / (np.linalg.norm(v) + 1e-6)


def hexc(h):
    if not isinstance(h, str):
        return np.asarray(h, np.float32)
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


def mix(a, b, t):
    return hexc(a) * (1 - t) + hexc(b) * t


# ------------------------------------------------------------ textures
_GRAIN = {}


def _grain_tile(strength):
    key = round(strength, 3)
    if key not in _GRAIN:
        n = 2048
        r = np.random.default_rng(1234)
        fine = cv2.GaussianBlur(r.standard_normal((n, n)).astype(np.float32), (0, 0), 0.7 * max(K, .5))
        blot = cv2.resize(r.standard_normal((n // 24 + 2, n // 24 + 2)).astype(np.float32), (n, n),
                          interpolation=cv2.INTER_CUBIC)
        fib = cv2.GaussianBlur(r.standard_normal((n, n)).astype(np.float32), (0, 0),
                               sigmaX=7 * K, sigmaY=0.6 * K)
        g = 0.45 * fine / fine.std() + 0.7 * blot / blot.std() + 0.8 * fib / fib.std()
        _GRAIN[key] = (1 + strength * g / 3).astype(np.float32)
    return _GRAIN[key]


def paper_grain(h, w, seed=0, strength=0.07):
    t = _grain_tile(strength)
    n = t.shape[0]
    if h > n or w > n:
        t = np.tile(t, (h // n + 1, w // n + 1))
    r = np.random.default_rng(seed)
    oy = int(r.integers(0, t.shape[0] - h + 1))
    ox = int(r.integers(0, t.shape[1] - w + 1))
    return t[oy:oy + h, ox:ox + w]


def pattern(kind, X, Y, period=20, seed=0):
    """Printed patterns (X, Y in pixels). Returns a multiplier field."""
    if kind == 'stripes':
        return np.where((Y // period) % 2 == 0, 1.0, 0.86).astype(np.float32)
    if kind == 'vstripes':
        return np.where((X // period) % 2 == 0, 1.0, 0.86).astype(np.float32)
    if kind == 'check':
        a = (X // period) % 2
        b = (Y // period) % 2
        return (1.0 - 0.08 * a - 0.08 * b).astype(np.float32)
    if kind == 'dots':
        u = (X % period) - period / 2
        v = (Y % period) - period / 2
        return np.where(u * u + v * v < (period * 0.22) ** 2, 0.82, 1.0).astype(np.float32)
    if kind == 'news':
        p = max(4, period * 0.5)
        r = np.random.default_rng(seed)
        row = (Y // p).astype(int)
        blocks = r.random((int(Y.max() // p) + 2, int(X.max() // (p * 2.2)) + 2)) > 0.35
        on = blocks[row, (X // (p * 2.2)).astype(int)]
        return np.where(((Y % p) < max(1, p * 0.16)) & on, 0.86, 1.0).astype(np.float32)
    if kind == 'planks':
        return np.where((X % period) < max(1.5, period * 0.03), 0.78, 1.0).astype(np.float32)
    if kind == 'hplanks':
        return np.where((Y % period) < max(1.5, period * 0.03), 0.78, 1.0).astype(np.float32)
    return np.ones_like(X, np.float32)


# ------------------------------------------------------------ geometry
def ellipse_pts(cx, cy, rx, ry, rot=0.0, n=None, a0=0.0, a1=2 * math.pi):
    n = n or max(24, int((rx + ry) * 0.6))
    full = abs(a1 - a0) >= 2 * math.pi - 1e-6
    t = np.linspace(a0, a1, n, endpoint=not full)
    c, s = math.cos(rot), math.sin(rot)
    x, y = rx * np.cos(t), ry * np.sin(t)
    return np.stack([cx + c * x - s * y, cy + s * x + c * y], 1).astype(np.float32)


def chamfer(pts, r):
    """Cut the corners of a polygon (cut-card look)."""
    pts = np.asarray(pts, np.float32)
    out = []
    n = len(pts)
    for i in range(n):
        p, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
        da, db = a - p, b - p
        la, lb = np.linalg.norm(da), np.linalg.norm(db)
        k = min(r, la * 0.45, lb * 0.45)
        out += [p + da / la * k, p + db / lb * k]
    return np.array(out, np.float32)


def noise1d(n, seed, k=4):
    r = np.random.default_rng(seed)
    v = r.standard_normal(n + 2 * k)
    v = np.convolve(v, np.ones(k) / k, 'same')[k:-k]
    return v / (v.std() + 1e-6)


def roughen(pts, seed, amp=0.8, step=5.0):
    pts = np.asarray(pts, np.float32)
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        k = max(1, int(np.linalg.norm(b - a) / step))
        for j in range(k):
            out.append(a + (b - a) * (j / k))
    out = np.array(out, np.float32)
    t = np.roll(out, -1, 0) - np.roll(out, 1, 0)
    nrm = np.stack([t[:, 1], -t[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    return out + nrm * (noise1d(len(out), seed) * amp)[:, None]


def poly_mask(h, w, pts):
    m = np.zeros((h, w), np.uint8)
    p = np.round(np.asarray(pts, np.float64) * 16).astype(np.int32)
    cv2.fillPoly(m, [p], 255, lineType=cv2.LINE_AA, shift=4)
    return m.astype(np.float32) / 255


def shift(img, dx, dy):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))


def blur(img, s):
    if s < 0.35:
        return img
    if s > 6:  # big blurs: do them at lower resolution (same look, much faster)
        f = max(1, int(s / 3))
        h, w = img.shape[:2]
        small = cv2.resize(img, (max(1, w // f), max(1, h // f)), interpolation=cv2.INTER_AREA)
        small = cv2.GaussianBlur(small, (0, 0), s / f)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)
    return cv2.GaussianBlur(img, (0, 0), s)


# ------------------------------------------------------------ layer
class Layer:
    """A sheet you glue paper pieces onto. Logical size w x h."""

    def __init__(self, w, h, seed=0, grain=0.07, scale=1.0):
        self.w, self.h = w, h
        self.pw, self.ph = int(math.ceil(w * K)), int(math.ceil(h * K))
        self.P = np.zeros((self.ph, self.pw, 3), np.float32)
        self.A = np.zeros((self.ph, self.pw), np.float32)
        self.G = paper_grain(self.ph, self.pw, seed, grain)
        self.scale, self.seed, self.n = scale, seed, 0

    def poly(self, pts, color, shade=1.0, crease=None, rim=1.0, shadow=1.0,
             rough=1.0, grad=0.10, paint=False, soft=0.0, pat=None, pat_period=20,
             alpha=1.0, glow=0.0):
        """One piece of paper. paint=True = flat painted mark (eyes, mouths)."""
        self.n += 1
        seed = self.seed * 7919 + self.n
        sc = self.scale * K
        pts = np.asarray(pts, np.float32) * K
        if rough > 0:
            pts = roughen(pts, seed, (0.35 if paint else 0.75) * rough * sc, max(2.0, 5 * sc))
        off = LIGHT * 4.5 * sc * shadow
        sig = 3.2 * sc
        pad = int(abs(off).max() + 3 * sig + 6 + soft * 3 * K)
        x0, y0 = np.floor(pts.min(0)).astype(int) - pad
        x1, y1 = np.ceil(pts.max(0)).astype(int) + pad
        X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(self.pw, x1), min(self.ph, y1)
        if X1 <= X0 or Y1 <= Y0:
            return
        hw = (Y1 - Y0, X1 - X0)
        m = poly_mask(*hw, pts - [X0, Y0])
        if soft > 0:
            m = blur(m, soft * sc)
        m *= alpha
        P = self.P[Y0:Y1, X0:X1]
        A = self.A[Y0:Y1, X0:X1]
        if shadow > 0 and not paint:
            sm = blur(shift(m, off[0], off[1]), sig)
            P *= (1 - 0.40 * shadow * sm)[..., None]
        col = np.empty(hw + (3,), np.float32)
        col[:] = hexc(color)
        col *= shade
        if not paint:
            col *= self.G[Y0:Y1, X0:X1, None]
            yy, xx = np.mgrid[Y0:Y1, X0:X1].astype(np.float32)
            c = pts.mean(0)
            ext = max(1.0, float(np.abs(pts - c).max()))
            t = ((xx - c[0]) * LIGHT[0] + (yy - c[1]) * LIGHT[1]) / (2 * ext)
            col *= (1 - grad * t)[..., None]
            if pat:
                col *= pattern(pat, xx - x0, yy - y0, pat_period * sc, seed)[..., None]
            if crease:
                for (p, q, dk) in crease:
                    p = np.asarray(p, np.float32) * K
                    q = np.asarray(q, np.float32) * K
                    d = q - p
                    side = (d[0] * (yy - p[1]) - d[1] * (xx - p[0])) > 0
                    col[side] *= (1 - dk)
                    ln = np.zeros(hw, np.uint8)
                    cv2.line(ln, tuple(int(v) for v in np.round((p - [X0, Y0]) * 16)),
                             tuple(int(v) for v in np.round((q - [X0, Y0]) * 16)), 255,
                             max(1, int(1.2 * sc)), cv2.LINE_AA, 4)
                    col *= (1 + 0.10 * ln.astype(np.float32)[..., None] / 255)
            if rim > 0:
                d = max(1.0, 1.6 * sc)
                lit = m * (1 - shift(m, LIGHT[0] * d, LIGHT[1] * d))
                drk = m * (1 - shift(m, -LIGHT[0] * d, -LIGHT[1] * d))
                col = col * (1 - 0.5 * rim * lit)[..., None] + \
                    0.5 * rim * lit[..., None] * np.array([1, .97, .9], np.float32)
                col *= (1 - 0.28 * rim * drk)[..., None]
        if glow > 0:
            col = col + glow
        self.P[Y0:Y1, X0:X1] = col * m[..., None] + P * (1 - m)[..., None]
        self.A[Y0:Y1, X0:X1] = m + A * (1 - m)

    def rect(self, x0, y0, x1, y1, color, **kw):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, **kw)

    def ellipse(self, cx, cy, rx, ry, color, rot=0.0, n=None, **kw):
        self.poly(ellipse_pts(cx, cy, rx, ry, rot, n=n), color, **kw)

    def stroke(self, pts, color, width, **kw):
        """A tapered painted line (brows, strings, cracks)."""
        pts = np.asarray(pts, np.float32)
        left, right = [], []
        for i in range(len(pts)):
            a = pts[max(0, i - 1)]
            b = pts[min(len(pts) - 1, i + 1)]
            t = b - a
            n = np.array([-t[1], t[0]]) / (np.linalg.norm(t) + 1e-6)
            taper = 0.55 + 0.45 * math.sin(math.pi * (i + 0.5) / len(pts))
            left.append(pts[i] + n * width / 2 * taper)
            right.append(pts[i] - n * width / 2 * taper)
        kw.setdefault('paint', True)
        self.poly(np.array(left + right[::-1]), color, **kw)


# ------------------------------------------------------------ scene
_PREP = {}


def _prepare(item, focus, dof, near_mult, shadow_len):
    """Blur + shadow for one layer, cached (static set pieces are reused every frame)."""
    s = dof * abs(item['z'] - focus) * (near_mult if item['z'] < focus else 1.0) * K
    key = (item.get('key'), round(s * 2) / 2, round(shadow_len, 2)) if item.get('key') else None
    if key and key in _PREP:
        return _PREP[key]
    L = item['layer']
    ys, xs = np.nonzero(L.A > 0.002)
    if len(xs) == 0:
        res = (np.zeros((1, 1, 4), np.float32), None, 0, 0, 0)
        return res
    m = int(3 * s + 4)
    bx, by = max(0, xs.min() - m), max(0, ys.min() - m)
    ex, ey = min(L.pw, xs.max() + m + 1), min(L.ph, ys.max() + m + 1)
    RGBA = np.dstack([L.P[by:ey, bx:ex], L.A[by:ey, bx:ex]])
    if s >= 0.35:
        RGBA = blur(RGBA, s)
    lift = item['lift']
    if lift > 0:
        A = RGBA[..., 3]
        pad = int(shadow_len * lift * K + 40 * K)
        Ap = cv2.copyMakeBorder(A, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        Sh = blur(shift(Ap, LIGHT[0] * shadow_len * lift * K, LIGHT[1] * shadow_len * lift * K),
                  (3 + 4 * lift) * K + s)
    else:
        Sh, pad = None, 0
    res = (RGBA, Sh, pad, bx, by)
    if key:
        if len(_PREP) > 60:
            _PREP.pop(next(iter(_PREP)))
        _PREP[key] = res
    return res


class Scene:
    def __init__(self, w=1080, h=1920, bg='#20181a'):
        self.w, self.h = w, h
        self.pw, self.ph = int(math.ceil(w * K)), int(math.ceil(h * K))
        self.bg = hexc(bg)
        self.items = []

    def add(self, layer, z, lift=1.0, x=0, y=0, dx=0, dy=0, key=None, name=''):
        """Put a layer (any size) with its top-left at logical (x, y), extra offset (dx, dy).
        key = cache name for layers that never change (set pieces)."""
        self.items.append(dict(layer=layer, z=z, lift=lift, x=x + dx, y=y + dy, key=key, name=name))

    def render(self, focus=2.0, dof=0.85, shadow=0.42, shadow_len=10.0, cam=(0, 0, 1.0),
               near_mult=4.0, extra_shadow=None):
        """cam = (pan_x, pan_y, zoom) in logical px. Nearer layers move/zoom more (parallax)."""
        out = np.empty((self.ph, self.pw, 3), np.float32)
        out[:] = self.bg
        px, py, zoom = cam
        cx, cy = self.pw / 2, self.ph / 2
        for it in sorted(self.items, key=lambda d: -d['z']):
            RGBA, Sh, pad, bx, by = _prepare(it, focus, dof, near_mult, shadow_len)
            z = max(it['z'], 0.25)
            par = 2.0 / z
            zz = 1 + (zoom - 1) * par
            tx = it['x'] * K + bx
            ty = it['y'] * K + by
            # layer px -> frame px: zoom about frame centre, then pan (parallax-scaled)
            ox = zz * tx + (1 - zz) * cx - px * par * K
            oy = zz * ty + (1 - zz) * cy - py * par * K
            if Sh is not None:
                M2 = np.float32([[zz, 0, ox - zz * pad], [0, zz, oy - zz * pad]])
                S = cv2.warpAffine(Sh, M2, (self.pw, self.ph), flags=cv2.INTER_LINEAR)
                out *= (1 - shadow * S)[..., None]
            M = np.float32([[zz, 0, ox], [0, zz, oy]])
            ident = abs(zz - 1) < 1e-6 and abs(ox) < 1e-6 and abs(oy) < 1e-6 and \
                RGBA.shape[0] == self.ph and RGBA.shape[1] == self.pw
            W = RGBA if ident else cv2.warpAffine(RGBA, M, (self.pw, self.ph), flags=cv2.INTER_LINEAR)
            out = W[..., :3] + out * (1 - W[..., 3:4])
        return out


# ------------------------------------------------------------ grade
_GRADE = {}

LIGHTS = {  # time-of-day looks: (multiply tint, lift, warmth)
    'dusk': ((1.00, 0.96, 0.92), 0.00, 0.04),
    'day': ((1.03, 1.02, 0.99), 0.02, 0.01),
    'night': ((0.66, 0.72, 0.98), 0.00, -0.03),
    'lamp': ((1.00, 0.90, 0.78), 0.00, 0.05),
    'storm': ((0.62, 0.66, 0.74), 0.00, -0.02),
}


def grade(img, glows=(), light='dusk', vignette=0.30, grain=0.010, frame=0, bloom=0.07,
          letterbox=0, flash=0.0, flash_color='#FFFFFF', sharpen=0.35):
    """glows: (x, y, radius, color, amount) in logical px - lanterns, windows, sun, fireflies.
    Light tint is applied BEFORE glows, so lit lanterns stay bright at night."""
    h, w = img.shape[:2]
    if (h, w) not in _GRADE:
        hs, ws = h // 4, w // 4
        yy, xx = np.mgrid[0:hs, 0:ws].astype(np.float32)
        r = np.sqrt(((xx - ws / 2) / (ws / 2)) ** 2 + ((yy - hs / 2) / (hs / 2)) ** 2)
        vig = cv2.resize(np.clip(r - 0.35, 0, None) ** 1.6, (w, h))
        rng = np.random.default_rng(9)
        noise = [rng.standard_normal((h, w)).astype(np.float32) for _ in range(6)]
        _GRADE[(h, w)] = (yy, xx, vig, noise)
    yy, xx, vig, noise = _GRADE[(h, w)]
    tint, lift, warm = LIGHTS.get(light, LIGHTS['dusk'])
    out = img * np.array(tint, np.float32) + lift
    if glows:
        f = np.zeros(yy.shape + (3,), np.float32)
        for (gx, gy, rad, color, amt) in glows:
            d2 = ((xx - gx * K / 4) ** 2 + (yy - gy * K / 4) ** 2) / (rad * K / 4) ** 2
            f += (np.exp(-d2) * amt)[..., None] * hexc(color)
        out += cv2.resize(f, (w, h), interpolation=cv2.INTER_LINEAR)
    hi = np.clip(out - 0.72, 0, None)
    small = cv2.resize(hi, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    out += cv2.resize(cv2.GaussianBlur(small, (0, 0), w * 0.005), (w, h)) * bloom * 3
    out[..., 0] *= 1 + warm
    out[..., 2] *= 1 - warm
    out *= (1 - vignette * vig)[..., None]
    out = out / (1 + 0.25 * out) * 1.25
    out = np.clip(out, 0, 1)
    out = out * out * (3 - 2 * out) * 0.35 + out * 0.65
    out += (noise[frame % 6] * grain)[..., None]
    if flash > 0:
        out = out * (1 - flash) + hexc(flash_color) * flash
    out = np.clip(out, 0, 1)
    if sharpen > 0:  # gentle unsharp mask: keeps the paper edges crisp on phones (user found the look blurry)
        out = np.clip(out * (1 + sharpen) - cv2.GaussianBlur(out, (0, 0), 1.2 * K) * sharpen, 0, 1)
    if letterbox:
        lb = int(letterbox * K)
        out[:lb] = 0
        out[h - lb:] = 0
    return (out * 255 + 0.5).astype(np.uint8)
