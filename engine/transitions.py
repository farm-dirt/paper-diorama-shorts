"""transitions - motivated scene-to-scene transitions (paper-diorama-shorts).

A scene can start with  "tin": {"type": TYPE, "dur": 0.6, "at": [x, y]}  in project.json.
During the first `dur` seconds of that scene the previous scene keeps playing underneath and the
two pictures are joined by one of these (all work on finished, graded frames):

  cut   - plain hard cut (default, no "tin")
  dive  - the camera dives INTO a point of the old picture ("at", e.g. a place drawn on a map) and the
          new place grows out of it. Use for map -> place, window -> outside, eye -> memory.
  fog   - a cold breath / mist fogs the screen, then clears on the new place (walking on, time passing).
  gust  - a sweep of blown snow / dust / petals wipes across (travel sideways, weather changes).
  dark  - an iris closes into shadow ("at" = where it closes), then opens in the new place
          (walking into a cave, a door, under water).
  whip  - fast whip-pan with motion blur (sudden attention, "meanwhile").
  flash - a soft white flash (a crack, a bite, a big glow).
Why: a hard cut between unrelated pictures makes a short feel like a slideshow; a transition that is
caused by something on screen tells the viewer HOW we got from one place to the next.
"""
import math
import numpy as np
import cv2

_TEX = {}


def _sm(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _noise(h, w, seed, scale):
    key = (h, w, seed, scale)
    if key not in _TEX:
        r = np.random.default_rng(seed)
        small = r.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
        n = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
        n = cv2.GaussianBlur(n, (0, 0), scale * 0.35)
        n = (n - n.min()) / (n.max() - n.min() + 1e-6)
        _TEX[key] = n
    return _TEX[key]


def _zoom(img, f, px, py):
    """Scale img by f about pixel (px, py) (stays in frame)."""
    M = np.float32([[f, 0, (1 - f) * px], [0, f, (1 - f) * py]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def blend(A, B, u, spec, t, k=1.0):
    """A = old scene frame, B = new scene frame (uint8 RGB, same size), u = 0..1 progress."""
    kind = spec.get('type', 'cut')
    h, w = B.shape[:2]
    Af = A.astype(np.float32) / 255
    Bf = B.astype(np.float32) / 255
    at = spec.get('at', [540, 960])
    px, py = at[0] * k, at[1] * k
    if kind == 'dive':
        e = _sm(u)
        A2 = _zoom(Af, 1 + 5.0 * e ** 1.6, px, py)
        B2 = _zoom(Bf, 1.0 + 0.45 * (1 - e) ** 2, w / 2, h / 2)
        m = _sm((u - 0.30) / 0.45)
        # radial light-burst at the dive point so the joint reads as "flying into the drawing"
        yy, xx = np.ogrid[:h, :w]
        g = np.exp(-(((xx - px) ** 2 + (yy - py) ** 2) / (w * (0.15 + 0.5 * e)) ** 2)).astype(np.float32)
        out = A2 * (1 - m) + B2 * m + (0.35 * math.sin(math.pi * u) * g)[..., None]
    elif kind == 'fog':
        n = _noise(h, w, 11, 90)
        n2 = _noise(h, w, 12, 40)
        rise = int(80 * k * u)
        n = np.roll(n, -rise, 0)
        dens = math.sin(math.pi * u) ** 0.6
        fogm = np.clip(dens * (0.75 + 0.45 * n + 0.2 * n2), 0, 1)
        fogc = np.array(spec.get('color', [0.90, 0.94, 0.98]), np.float32)
        base = Af if u < 0.5 else Bf
        if 0.38 < u < 0.62:
            mm = (u - 0.38) / 0.24
            base = Af * (1 - mm) + Bf * mm
        blurred = cv2.GaussianBlur(base, (0, 0), 1 + 14 * dens * k)
        out = blurred * (1 - fogm[..., None]) + fogc * fogm[..., None]
    elif kind == 'gust':
        e = _sm(u)
        yy, xx = np.mgrid[:h, :w].astype(np.float32)
        d = (xx / w) * 0.85 + (yy / h) * 0.35            # diagonal sweep, left -> right
        n = _noise(h, w, 21, 60)
        edge = -0.25 + 1.6 * e
        m = np.clip((edge - d + 0.12 * (n - 0.5)) / 0.18, 0, 1)
        band = np.exp(-((d - edge) / 0.09) ** 2) * (0.6 + 0.6 * n)
        # streaks of blown snow concentrated on the moving edge
        r = np.random.default_rng(int(t * 24))
        streak = np.zeros((h, w), np.float32)
        for _ in range(90):
            y0 = r.uniform(0, h)
            x0 = (edge - 0.35 * y0 / h + r.uniform(-0.12, 0.12)) / 0.85 * w
            ln = r.uniform(40, 160) * k
            cv2.line(streak, (int(x0 - ln), int(y0 - ln * 0.25)), (int(x0), int(y0)), r.uniform(0.4, 1.0),
                     max(1, int(r.uniform(2, 6) * k)), cv2.LINE_AA)
        streak = cv2.GaussianBlur(streak, (0, 0), 1.5 * k)
        snow = np.clip(0.85 * band + streak, 0, 1)[..., None]
        out = Af * (1 - m[..., None]) + Bf * m[..., None]
        out = out * (1 - snow) + np.array([0.95, 0.97, 1.0], np.float32) * snow
    elif kind == 'dark':
        yy, xx = np.ogrid[:h, :w]
        R = math.hypot(max(px, w - px), max(py, h - py)) * 1.05
        if u < 0.5:
            rr = R * (1 - _sm(u / 0.5)) ** 1.2
            dist = np.sqrt((xx - px) ** 2 + (yy - py) ** 2)
            m = np.clip((rr - dist) / (60 * k) + 0.5, 0, 1).astype(np.float32)
            out = Af * m[..., None]
        else:
            rr = R * _sm((u - 0.5) / 0.5) ** 1.2
            cx, cy = w / 2, h * 0.45
            dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            m = np.clip((rr - dist) / (90 * k) + 0.5, 0, 1).astype(np.float32)
            out = Bf * m[..., None]
    elif kind == 'whip':
        e = _sm(u)
        sp = math.sin(math.pi * u)
        ks = max(1, int(140 * k * sp)) | 1
        ker = np.zeros((1, ks), np.float32)
        ker[0, :] = 1.0 / ks
        if u < 0.5:
            src, off = Af, -w * 0.5 * e
        else:
            src, off = Bf, w * 0.5 * (1 - e)
        M = np.float32([[1, 0, off], [0, 1, 0]])
        out = cv2.filter2D(cv2.warpAffine(src, M, (w, h), borderMode=cv2.BORDER_REFLECT), -1, ker)
    elif kind == 'flash':
        m = _sm((u - 0.35) / 0.2)
        out = Af * (1 - m) + Bf * m
        f = math.sin(math.pi * u) ** 2 * spec.get('amount', 0.75)
        out = out * (1 - f) + np.array(spec.get('color', [1.0, 0.98, 0.92]), np.float32) * f
    else:
        return B
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)
