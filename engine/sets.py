"""Diorama sets (locations). All original.

get_set(name, variant) -> dict:
  items  : paper layers [{layer, z, lift, x, y, key, move(t)->(dx, dy)}]
  glows  : f(t) -> [(x, y, radius, color, amount)]  lights added in grade()
  floor  : y where actors' feet stand (logical px)
  marks  : named x positions for actors (L, C, R ...)
  focus, light : defaults for the camera focus plane and time-of-day grade

Depth guide (z): 10 backdrop - 7..9 far - 3..6 mid set - 2.4 floor - 2.0 actors
(focus) - < 1.5 foreground (heavy blur). Bigger lift = floats higher = longer shadow.

To add a location: write build_<name>(variant) returning the same dict and add it
to SETS. Reuse the helpers band(), hill(), palm(), hut(). Keep pieces as cut paper:
rough edges on, a crease or pattern on big shapes, 4-7 colour values max.
"""
import math
import numpy as np
import paperkit
from paperkit import Layer, ellipse_pts, chamfer, noise1d

W, H = 1080, 1920
_CACHE = {}


def item(layer, z, lift=1.0, x=0, y=0, key=None, move=None):
    return dict(layer=layer, z=z, lift=lift, x=x, y=y, key=key, move=move)


def band(y0, amp, wl, phase, bottom, step=10, x0=-60, x1=W + 60):
    xs = np.arange(x0, x1 + step, step, dtype=np.float32)
    ys = y0 + amp * np.sin(2 * math.pi * xs / wl + phase)
    return np.concatenate([np.stack([xs, ys], 1), [[x1, bottom], [x0, bottom]]]).astype(np.float32)


def hill(base, height, seed, bottom, step=14, x0=-60, x1=W + 60):
    xs = np.arange(x0, x1 + step, step, dtype=np.float32)
    n = noise1d(len(xs), seed, 9)
    n = np.convolve(n, np.ones(5) / 5, 'same')
    ys = base - height * (0.55 + 0.45 * n / (np.abs(n).max() + 1e-6))
    return np.concatenate([np.stack([xs, ys], 1), [[x1, bottom], [x0, bottom]]]).astype(np.float32)


def wave_strip(y, color, wl, amp, seed, speed, direction=1, z=4.0, lift=0.6, key=''):
    """A paper wave strip that slides sideways forever (seamless)."""
    L = Layer(int(W + 3 * wl), H - y + 80, seed=seed)
    L.poly(band(40, amp, wl, 0, H - y + 80, step=8, x0=0, x1=W + 3 * wl), color)
    return item(L, z, lift, x=-1.5 * wl, y=y - 40, key=key,
                move=lambda t: (direction * ((speed * t) % wl), 0))


def sky_bands(seed, base, bands):
    L = Layer(W, H, seed=seed, grain=0.09)
    L.rect(0, 0, W, H, base, rim=0, shadow=0, rough=0)
    for i, (y, c, a) in enumerate(bands):
        L.poly(band(y, a, 520 + 90 * i, i * 1.7, H), c, grad=0.05)
    return L


def clouds(seed, specs, color='#F3C7A6'):
    L = Layer(W + 400, 900, seed=seed)
    for (cx, cy, s_) in specs:
        for (dx, dy, r) in [(-60, 10, 46), (0, -12, 62), (66, 6, 44), (10, 26, 50)]:
            L.ellipse(cx + dx * s_, cy + dy * s_, r * s_ * 1.4, r * s_, color, shade=0.95)
    return L


def palm(L, x, base, h, lean=0.0, color='#3F5B3A', trunk='#7A5638'):
    top = (x + lean * h, base - h)
    pts = []
    for i in range(9):
        u = i / 8
        cx = x + lean * h * u * u
        cy = base - h * u
        w_ = 16 - 7 * u
        pts.append((cx - w_, cy))
    pts2 = [(p[0] + 2 * (16 - 7 * (i / 8)), p[1]) for i, p in enumerate(pts)]
    L.poly(pts + pts2[::-1], trunk, pat='hplanks', pat_period=26)
    for k in range(7):
        a = math.radians(-170 + k * 30)
        ln = 150 + 25 * math.sin(k * 2.1)
        ex, ey = top[0] + ln * math.cos(a), top[1] + ln * math.sin(a) * 0.55 + 40
        mx, my = top[0] + ln * 0.5 * math.cos(a), top[1] + ln * 0.5 * math.sin(a) * 0.55 - 16
        n = np.array([-(ey - top[1]), ex - top[0]]) / (math.hypot(ex - top[0], ey - top[1]) + 1e-6)
        L.poly([top, (mx + n[0] * 22, my + n[1] * 22), (ex, ey), (mx - n[0] * 10, my - n[1] * 10)],
               color, shade=0.85 + 0.15 * (k % 2), crease=[(top, (ex, ey), 0.12)])


def hut(L, x, y, w, h, wall='#B5654A', roof='#C29A52', stilts=True, window_lit=False, seed_shade=1.0):
    if stilts:
        for sx in np.linspace(x + 10, x + w - 20, 4):
            L.rect(sx, y + h, sx + 10, y + h + 120, '#3E2A22', rim=0.5)
        L.rect(x - 10, y + h - 4, x + w + 10, y + h + 12, '#5E3B27')
    L.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], wall, pat='vstripes', pat_period=14,
           crease=[((x + w / 2, y), (x + w / 2, y + h), 0.1)], shade=seed_shade)
    L.rect(x + w * 0.13, y + h * 0.26, x + w * 0.36, y + h * 0.71, '#FFC46B' if window_lit else '#4A3328',
           glow=0.25 if window_lit else 0, rim=0.4)
    L.rect(x + w * 0.61, y + h * 0.34, x + w * 0.85, y + h, '#5E3B27')
    L.poly([(x - w * 0.15, y + 8), (x + w / 2, y - h * 0.8), (x + w * 1.15, y + 8)], roof, pat='stripes',
           pat_period=9, crease=[((x + w / 2, y - h * 0.8), (x + w / 2, y + 8), 0.12)])


# =========================================================== HARBOR
def build_harbor(variant='dusk'):
    night = variant == 'night'
    its = []
    if night:
        sky = sky_bands(101, '#101A33', [(300, '#16244A', 26), (520, '#1E2F58', 30), (720, '#283A66', 24),
                                         (880, '#34477A', 22), (980, '#40538A', 18)])
        sky.ellipse(760, 520, 90, 90, '#F4EFE6', glow=0.12)
        r = np.random.default_rng(4)
        for _ in range(38):
            sx_, sy_ = r.uniform(30, W - 30), r.uniform(60, 900)
            s_ = r.uniform(4, 9)
            sky.poly([(sx_, sy_ - s_), (sx_ + s_ * .3, sy_ - s_ * .3), (sx_ + s_, sy_), (sx_ + s_ * .3, sy_ + s_ * .3),
                      (sx_, sy_ + s_), (sx_ - s_ * .3, sy_ + s_ * .3), (sx_ - s_, sy_), (sx_ - s_ * .3, sy_ - s_ * .3)],
                     '#FFE7A8', shadow=0.4, glow=0.15)
    else:
        sky = sky_bands(101, '#2A4560', [(260, '#3E5470', 26), (470, '#6B5C80', 30), (640, '#A8687D', 24),
                                         (790, '#DB7F5E', 22), (920, '#F2A465', 18)])
        sky.ellipse(300, 905, 112, 112, '#FFD98A', glow=0.10)
    its.append(item(sky, 10, 0, key=f'harbor-sky-{variant}'))
    cl = clouds(102, [(760, 420, 1.0), (240, 610, 0.8)], '#3A4A70' if night else '#F3C7A6')
    its.append(item(cl, 9.5, 0.6, x=-200, y=0, key=f'harbor-cloud-{variant}', move=lambda t: (6 * t, 0)))
    far = Layer(W, H, seed=103)
    far.poly(hill(1030, 170, 7, H), '#3B2E4E' if night else '#8C5A6E', grad=0.06)
    its.append(item(far, 8, 1.0, key=f'harbor-far-{variant}'))
    isl = Layer(W, H, seed=104)
    isl.poly(hill(1070, 110, 21, H), '#2B2240' if night else '#6A4560')
    for hx in (120, 190, 860):
        isl.rect(hx, 1010, hx + 44, 1048, '#241C33' if night else '#4F3349', rim=0.6)
        isl.poly([(hx - 8, 1012), (hx + 22, 984), (hx + 52, 1012)], '#241C33' if night else '#4F3349', rim=0.6)
        isl.ellipse(hx + 22, 1030, 5, 6, '#FFC46B', paint=True, glow=0.3)
    its.append(item(isl, 7, 1.0, key=f'harbor-isl-{variant}'))
    cols = ['#24506A', '#1F4660', '#1A3C54', '#163449'] if night else ['#4E8A8C', '#3B7A7D', '#2F6A6E', '#265C61']
    for k, (y, z) in enumerate([(1095, 6), (1180, 5), (1290, 4.2), (1420, 3.2)]):
        wl = 180 + 40 * k
        its.append(wave_strip(y, cols[k], wl, 9 + 2 * k, 110 + k, 26 + 10 * k, 1 if k % 2 else -1, z, 0.6,
                              key=f'harbor-wave{k}-{variant}'))
        if k == 1:
            hl = Layer(W, H, seed=120)
            hut(hl, 760, 1035, 230, 116, window_lit=True)
            its.append(item(hl, z - 0.3, 1.0, key=f'harbor-hut-{variant}'))
            boat = Layer(300, 200, seed=130)
            bx, by = 150, 150
            boat.poly([(bx - 70, by - 22), (bx + 70, by - 22), (bx + 46, by + 10), (bx - 46, by + 10)], '#C8553D',
                      crease=[((bx - 70, by - 8), (bx + 70, by - 8), 0.12)])
            boat.rect(bx - 2, by - 92, bx + 2, by - 22, '#3A2A22', rim=0)
            boat.poly([(bx + 4, by - 88), (bx + 52, by - 34), (bx + 4, by - 34)], '#F4EFE6')
            its.append(item(boat, z - 0.15, 0.7, x=60, y=1075, key='harbor-boat',
                            move=lambda t: (14 * math.sin(t * 0.6), 5 * math.sin(t * 1.7))))
    dock = Layer(W, H, seed=140)
    dock.poly([(-40, 1585), (W + 40, 1555), (W + 40, 1700), (-40, 1730)], '#8A5A3C', pat='planks', pat_period=64, grad=0.12)
    dock.poly([(-40, 1722), (W + 40, 1692), (W + 40, H + 20), (-40, H + 20)], '#5E3B27', pat='planks', pat_period=64)
    for px in (90, 990):
        dock.rect(px - 26, 1470, px + 26, H + 20, '#6E4630', crease=[((px, 1468), (px, H), 0.12)])
        dock.rect(px - 28, 1520, px + 28, 1540, '#D8C29A')
    its.append(item(dock, 2.4, 0.5, key='harbor-dock'))
    lights = Layer(W, H, seed=150)
    pts = [(90 + i * 900 / 7, 1470 + 26 * math.sin(math.pi * i / 7)) for i in range(8)]
    for a, b in zip(pts, pts[1:]):
        lights.stroke([a, b], '#2A2020', 3, rough=0)
    lamps = []
    for i, (lx, ly) in enumerate(pts[1:-1]):
        lights.rect(lx - 2, ly, lx + 2, ly + 8, '#2A2020', rim=0)
        lights.ellipse(lx, ly + 24, 14, 17, ['#D2453A', '#E0A33A', '#F4EFE6'][i % 3], n=12,
                       crease=[((lx, ly + 7), (lx, ly + 41), 0.08)], glow=0.12)
        lamps.append((lx, ly + 24))
    its.append(item(lights, 2.3, 1.2, key='harbor-lights'))
    fg = Layer(W, H, seed=160)
    for i in range(7):
        bx = -20 + i * 34
        fg.poly([(bx, H + 20), (bx + 26, H + 20), (bx + 18, H - 330 + 30 * (i % 3)), (bx + 6, H - 340 + 30 * (i % 3))],
                ['#3F5B3A', '#4E6E44', '#36503A'][i % 3])
    for r_, sh in [(150, 0.85), (112, 1.0), (76, 0.85), (40, 1.0)]:
        fg.ellipse(W - 70, H - 40, r_, r_ * 0.42, '#C9A46A', shade=sh)
    its.append(item(fg, 0.7, 1.5, key='harbor-fg'))

    def glows(t):
        g = [(760, 520, 380, '#9FB7FF', 0.16)] if night else [(300, 905, 520, '#FF9A4D', 0.22)]
        g += [(x, y, 60, '#FFB060', 0.16 if night else 0.10) for (x, y) in lamps]
        g += [(820, 1100, 90, '#FFB060', 0.18 if night else 0.08)]
        return g
    return dict(items=its, glows=glows, floor=1660, focus=2.0, light='night' if night else 'dusk',
                marks={'L': 290, 'CL': 450, 'C': 560, 'CR': 680, 'R': 830})


# =========================================================== ROOM (interior)
def build_room(variant='lamp'):
    night = variant in ('night', 'lamp')
    its = []
    wall = Layer(W, H, seed=201, grain=0.08)
    wall.rect(0, 0, W, H, '#C9A27A', rim=0, shadow=0, rough=0, pat='vstripes', pat_period=60)
    wall.rect(0, 1380, W, 1420, '#E8DCC3')  # skirting/chair rail
    its.append(item(wall, 6, 0, key='room-wall'))
    win = Layer(W, H, seed=202)
    wx, wy, ww, wh = 140, 520, 420, 520
    win.rect(wx - 22, wy - 22, wx + ww + 22, wy + wh + 22, '#E8DCC3')
    win.rect(wx, wy, wx + ww, wy + wh, '#1C2A4E' if night else '#9FD0D6', rim=0.3, grad=0.2)
    if night:
        win.ellipse(wx + ww * 0.7, wy + 140, 46, 46, '#F4EFE6', glow=0.15)
    win.poly(hill(wy + wh - 60, 60, 33, wy + wh, x0=wx, x1=wx + ww), '#16203A' if night else '#5E8F6A', rim=0.5)
    win.rect(wx + ww / 2 - 6, wy, wx + ww / 2 + 6, wy + wh, '#E8DCC3')
    win.rect(wx, wy + wh / 2 - 6, wx + ww, wy + wh / 2 + 6, '#E8DCC3')
    win.poly([(wx - 30, wy - 40), (wx + 90, wy - 40), (wx + 60, wy + wh + 40), (wx - 30, wy + wh + 40)], '#8C3B2E',
             crease=[((wx + 20, wy - 40), (wx + 10, wy + wh + 40), 0.1)])
    win.poly([(wx + ww + 30, wy - 40), (wx + ww - 90, wy - 40), (wx + ww - 60, wy + wh + 40),
              (wx + ww + 30, wy + wh + 40)], '#8C3B2E', crease=[((wx + ww - 20, wy - 40), (wx + ww - 10, wy + wh + 40), 0.1)])
    its.append(item(win, 5.6, 0.8, key=f'room-window-{variant}'))
    deco = Layer(W, H, seed=203)
    deco.rect(700, 600, 940, 790, '#5E3B27')
    deco.rect(718, 618, 922, 772, '#E8DCC3', pat='news', pat_period=18)
    deco.ellipse(820, 700, 50, 56, '#8C5A6E', n=14, shade=0.9)
    deco.rect(720, 1100, 1000, 1400, '#7A5638', pat='hplanks', pat_period=100,
              crease=[((860, 1100), (860, 1400), 0.1)])
    deco.rect(700, 1080, 1020, 1110, '#5E3B27')
    deco.rect(838, 1000, 882, 1080, '#C8553D')  # lamp base
    deco.poly([(790, 900), (930, 900), (960, 1004), (760, 1004)], '#F2D9A0', glow=0.18,
              crease=[((860, 900), (860, 1004), 0.06)])
    deco.rect(650, 1300, 700, 1400, '#2F6F73')  # plant pot
    for k in range(5):
        a = math.radians(-140 + k * 25)
        deco.ellipse(675 + 80 * math.cos(a), 1240 + 70 * math.sin(a), 60, 22, '#4E6E44', rot=a, n=10,
                     shade=0.85 + 0.05 * k)
    its.append(item(deco, 4.5, 0.9, key='room-deco'))
    floor = Layer(W, H, seed=204)
    floor.poly([(-40, 1420), (W + 40, 1420), (W + 40, H + 20), (-40, H + 20)], '#9A6A43', pat='planks', pat_period=90, grad=0.18)
    floor.ellipse(540, 1700, 470, 120, '#2F6F73', n=40, pat='stripes', pat_period=22)
    its.append(item(floor, 2.4, 0.3, key='room-floor'))
    fg = Layer(W, H, seed=205)
    fg.rect(-40, 1560, 220, 1960, '#6E4630', crease=[((90, 1560), (90, 1960), 0.1)])
    fg.rect(-40, 1520, 260, 1580, '#7A5638')
    fg.ellipse(980, 1880, 160, 90, '#8C3B2E', n=18)
    its.append(item(fg, 0.8, 1.4, key='room-fg'))

    def glows(t):
        g = [(860, 960, 420, '#FFB060', 0.30 if night else 0.12), (860, 960, 120, '#FFD58A', 0.25)]
        if night:
            g.append((wx + ww * 0.7, wy + 140, 160, '#9FB7FF', 0.10))
        else:
            g.append((350, 780, 500, '#FFF2D0', 0.15))
        return g
    return dict(items=its, glows=glows, floor=1700, focus=2.0, light='lamp' if night else 'day',
                marks={'L': 280, 'CL': 420, 'C': 540, 'CR': 660, 'R': 800})


# =========================================================== FOREST (night, balete tree)
def build_forest(variant='night'):
    its = []
    sky = sky_bands(301, '#1A2650', [(500, '#22306A', 30), (800, '#2C3C7A', 26), (1000, '#38488A', 20)])
    sky.ellipse(330, 420, 120, 120, '#F4EFE6', glow=0.18)
    its.append(item(sky, 10, 0, key='forest-sky'))
    for k, (base, hgt, col, z) in enumerate([(1150, 380, '#2A3762', 8), (1250, 300, '#223058', 6.5)]):
        L = Layer(W, H, seed=310 + k)
        L.poly(hill(base, hgt, 40 + k, H, step=18), col)
        r = np.random.default_rng(k)
        for _ in range(6):
            tx = r.uniform(0, W)
            th = r.uniform(260, 420)
            L.poly([(tx - 50, base - 40), (tx, base - 40 - th), (tx + 50, base - 40)], col, shade=0.9)
        its.append(item(L, z, 1.0, key=f'forest-far{k}'))
    tree = Layer(W, H, seed=320)
    tx, ty = 700, 1600
    r = np.random.default_rng(3)
    for k in range(14):  # canopy: clusters of cut-paper leaf blobs
        a = k / 13
        cx_ = tx - 430 + 900 * a + r.uniform(-40, 40)
        cy_ = ty - 1010 + 120 * math.sin(a * math.pi * 2.2) * 0.4 - 80 * math.sin(a * math.pi) + r.uniform(-30, 30)
        tree.ellipse(cx_, cy_, r.uniform(110, 160), r.uniform(80, 120), ['#2E4A4A', '#355454', '#284242'][k % 3],
                     n=14, shade=0.95 + 0.1 * (k % 2))
    # buttress trunk with flared roots
    tree.poly([(tx - 260, ty), (tx - 120, ty - 140), (tx - 110, ty - 640), (tx - 170, ty - 900), (tx + 60, ty - 980),
               (tx + 240, ty - 880), (tx + 150, ty - 620), (tx + 160, ty - 140), (tx + 300, ty)], '#6A5A7A',
              pat='vstripes', pat_period=26, crease=[((tx + 20, ty), (tx + 10, ty - 950), 0.14)])
    for (x0_, x1_) in [(-110, -40), (0, 50), (70, 130)]:  # dark gaps between trunk strands
        tree.poly([(tx + x0_, ty - 60), (tx + x0_ + 20, ty - 700), (tx + x1_ - 20, ty - 700), (tx + x1_, ty - 60)],
                  '#3E3350', shade=0.9, rim=0.5)
    tree.ellipse(tx + 15, ty - 330, 46, 70, '#1A1426', n=12)  # hollow
    for k in range(18):  # hanging aerial roots: thin paper strips
        rx = tx - 380 + k * 46 + r.uniform(-10, 10)
        top = ty - 930 + r.uniform(-30, 30)
        ln = r.uniform(360, 720)
        tree.poly([(rx, top), (rx + 9, top), (rx + 6 + 12 * math.sin(k), top + ln), (rx + 1 + 12 * math.sin(k), top + ln)],
                  '#7A6A8A', shade=0.75 + 0.25 * (k % 3) / 2, rim=0.6)
    its.append(item(tree, 3.6, 1.2, key='forest-tree'))
    ground = Layer(W, H, seed=330)
    ground.poly(hill(1640, 50, 61, H + 20), '#3A4A5E', grad=0.1)
    ground.poly(hill(1700, 30, 62, H + 20), '#2E3C52', pat='news', pat_period=30)
    its.append(item(ground, 2.4, 0.4, key='forest-ground'))
    fg = Layer(W, H, seed=340)
    for k in range(9):
        a = math.radians(-160 + k * 16)
        fg.ellipse(120 + 260 * math.cos(a) * 0.6, H + 30 + 300 * math.sin(a), 150, 34, '#3A6A4E', rot=a, n=12,
                   shade=0.8 + 0.05 * (k % 3), crease=[((120, H), (120 + 300 * math.cos(a) * .6, H + 300 * math.sin(a)), .1)])
    for k in range(7):
        a = math.radians(-120 - k * 10)
        fg.ellipse(W - 60 + 230 * math.cos(a) * 0.7, H + 20 + 260 * math.sin(a), 130, 30, '#335E44', rot=a, n=12)
    its.append(item(fg, 0.8, 1.6, key='forest-fg'))
    rf = np.random.default_rng(11)
    flies = [(rf.uniform(80, W - 80), rf.uniform(900, 1600), rf.uniform(0, 6.28), rf.uniform(0.4, 1.0)) for _ in range(14)]

    def glows(t):
        g = [(330, 420, 520, '#9FB7FF', 0.20)]
        for (fx, fy, ph, sp) in flies:
            x = fx + 40 * math.sin(t * sp + ph)
            y = fy + 30 * math.sin(t * sp * 1.3 + ph * 2)
            a = 0.5 + 0.5 * math.sin(t * 3 * sp + ph)
            g.append((x, y, 7, '#FFE58A', 1.2 * a))
            g.append((x, y, 38, '#CFFF8A', 0.14 * a))
        return g
    return dict(items=its, glows=glows, floor=1690, focus=2.0, light='night',
                marks={'L': 230, 'CL': 380, 'C': 540, 'CR': 700, 'R': 860})


# =========================================================== VILLAGE (day/dusk)
def build_village(variant='day'):
    dusk = variant == 'dusk'
    its = []
    if dusk:
        sky = sky_bands(401, '#3E5470', [(400, '#6B5C80', 30), (650, '#C9727A', 24), (880, '#F2A465', 20)])
    else:
        sky = sky_bands(401, '#7DB8C8', [(420, '#93C6CF', 28), (700, '#B3D8D2', 22), (920, '#D8E8D0', 16)])
    sky.ellipse(820, 360, 90, 90, '#FFE7A8' if not dusk else '#FFD98A', glow=0.1)
    its.append(item(sky, 10, 0, key=f'village-sky-{variant}'))
    cl = clouds(402, [(260, 380, 0.9), (700, 560, 1.1)], '#F4EFE6' if not dusk else '#F3C7A6')
    its.append(item(cl, 9.5, 0.6, x=-200, key=f'village-cloud-{variant}', move=lambda t: (5 * t, 0)))
    mt = Layer(W, H, seed=403)
    mt.poly([(-60, 1150), (260, 780), (480, 1020), (720, 700), (1140, 1150), (1140, H), (-60, H)],
            '#7E7A9A' if not dusk else '#7A5A78', crease=[((720, 700), (760, 1150), 0.12), ((260, 780), (300, 1150), 0.12)])
    its.append(item(mt, 8.5, 1.0, key=f'village-mt-{variant}'))
    fld = Layer(W, H, seed=404)
    fld.poly(hill(1180, 60, 71, H), '#7FA35A' if not dusk else '#6A7A4A', pat='stripes', pat_period=18)
    its.append(item(fld, 6.5, 0.8, key=f'village-field-{variant}'))
    huts = Layer(W, H, seed=405)
    palm(huts, 90, 1280, 420, 0.25)
    hut(huts, 180, 1010, 260, 150, window_lit=dusk)
    hut(huts, 620, 1040, 220, 130, wall='#A85A44', window_lit=dusk, seed_shade=0.95)
    palm(huts, 930, 1300, 470, -0.2, color='#4E6E44')
    its.append(item(huts, 4.2, 1.0, key=f'village-huts-{variant}'))
    road = Layer(W, H, seed=406)
    road.poly(hill(1520, 20, 81, H + 20), '#C9A777', pat='news', pat_period=40, grad=0.12)
    road.poly([(380, 1520), (700, 1520), (1100, H + 20), (-20, H + 20)], '#B8925E', rim=0.6)
    its.append(item(road, 2.4, 0.3, key=f'village-road-{variant}'))
    fg = Layer(W, H, seed=407)
    for k in range(6):
        x = -30 + k * 70
        fg.rect(x, 1600 + 10 * (k % 2), x + 34, H + 20, '#C9A46A', crease=[((x + 17, 1600), (x + 17, H), 0.12)])
    fg.rect(-40, 1680, 420, 1710, '#A8834F')
    fg.rect(-40, 1800, 420, 1830, '#A8834F')
    for k in range(4):
        a = math.radians(-120 - k * 15)
        fg.ellipse(W - 40 + 240 * math.cos(a) * 0.7, H + 20 + 240 * math.sin(a), 140, 34, '#3F5B3A', rot=a, n=12)
    its.append(item(fg, 0.8, 1.5, key=f'village-fg-{variant}'))

    def glows(t):
        g = [(820, 360, 520, '#FFD98A' if dusk else '#FFF2D0', 0.22 if dusk else 0.10)]
        if dusk:
            g += [(260, 1080, 70, '#FFB060', 0.15), (680, 1100, 60, '#FFB060', 0.15)]
        return g
    return dict(items=its, glows=glows, floor=1640, focus=2.0, light='dusk' if dusk else 'day',
                marks={'L': 250, 'CL': 400, 'C': 540, 'CR': 680, 'R': 830})


SETS = {'harbor': build_harbor, 'room': build_room, 'forest': build_forest, 'village': build_village}
VARIANTS = {'harbor': ['dusk', 'night'], 'room': ['lamp', 'day'], 'forest': ['night'], 'village': ['day', 'dusk']}


def get_set(name, variant=None):
    variant = variant or VARIANTS[name][0]
    key = (name, variant, paperkit.K)
    if key not in _CACHE:
        _CACHE.clear()  # one set in memory at a time keeps RAM low
        _CACHE[key] = SETS[name](variant)
    return _CACHE[key]
