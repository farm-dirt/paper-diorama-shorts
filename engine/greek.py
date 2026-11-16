"""Greek starter kit for the "Tiny Olympus" channel (original designs, cut-paper style).

Importing this module registers everything into the engine:
  SETS     temple (day, dusk, night) - marble temple on a hill above the Aegean, olive trees
           olympus (day, storm)      - golden thrones on a cloud floor above the mountains
           sea_cliff (day, storm)    - white cliffs, a sailing ship, rolling paper waves
           cave (fire, dark)         - a rock cave lit by a fire pit (giants, monsters, hiding places)
  CAST     zeus, hera, aphrodite, ares, mortal_man, mortal_woman
           All share the human bones (root legL legR torso head armR armL + prop), so every HUMAN
           pose and the puppet walk work. Props: pose "prop": bolt | trident | spear | goblet | apple | scroll.

Make another god or mortal in a project's custom.py with the same look, so a character looks the
same in every short:
    import greek
    def register(CAST, rigs, POSES, SETS):
        greek.add_figure('poseidon', robe='#2F6F73', robe2='#E8DCC3', hair='#E8E4DA', style='beard_long',
                         headwear='diadem', prop='trident')
        rigs['poseidon'] = CAST['poseidon']()
Figure options: robe, robe2 (drape), trim, skin, hair, style (beard_long | beard_short | bun | long_wavy |
short | veil), headwear (None | laurel | diadem | helmet), height ('tall' | 'mid'), skirt ('long' | 'short').
Add a reusable figure to this file (and push it) when it will appear in more than one short.
"""
import math
import numpy as np
from paperkit import Layer, ellipse_pts, chamfer
import cast as C
import sets as S
from cast import P, E, mx, Rig

W, H = S.W, S.H
INK = C.INK
GOLD = '#D8A93A'
MARBLE = '#EDE6D6'
MARBLE_SH = '#CFC5B0'
SKIN_L = '#EBC39C'
SKIN_M = '#C98F62'
SKIN_D = '#9A6646'


# ================================================================ figures
def _figure(robe, robe2, trim=GOLD, skin=SKIN_L, hair='#3A2A22', style='short', headwear=None,
            height='tall', skirt='long', blush=False, default_prop=None):
    hip = 330 if height == 'tall' else 300
    leg = hip - 40

    def legs(side):
        def parts(p):
            f = (lambda a: a) if side < 0 else mx
            out = [P([(-22, 0), (22, 0), (20, leg), (-20, leg)], skin, shade=0.92)]
            out.append(P(f([(-22, leg - 6), (22, leg - 6), (24, leg + 18), (-40, leg + 20), (-42, leg + 30), (26, leg + 30)]),
                         '#8A5A3C', crease=[((-22, leg + 10), (24, leg + 10), 0.12)]))  # sandal
            out.append(P([(-22, leg - 70), (22, leg - 70), (22, leg - 62), (-22, leg - 62)], '#8A5A3C', rim=0))  # strap
            return out
        return parts

    def torso(p):
        hem = leg - 6 if skirt == 'long' else 120
        body = chamfer([(-92, -hip), (92, -hip), (104, -hip + 110), (118, hem), (-118, hem), (-104, -hip + 110)], 14)
        folds = [((x, -hip + 40), (x * 1.2, hem), 0.07) for x in (-50, 0, 50)]
        out = [P(body, robe, crease=folds)]
        out.append(P([(-118, hem - 22), (118, hem - 22), (118, hem), (-118, hem)], trim, shade=0.95, pat='vstripes', pat_period=14))
        # himation: a diagonal drape over the left shoulder
        out.append(P([(30, -hip - 6), (98, -hip + 4), (110, -hip + 140), (-110, 40), (-112, -40), (-20, -hip + 120)],
                     robe2, crease=[((60, -hip), (-100, 0), 0.10)], shade=0.98))
        out.append(P([(-104, -40), (-112, -40), (-110, 40), (-102, 40)], trim, rim=0))
        out.append(P([(-30, -hip - 4), (30, -hip - 4), (20, -hip + 26), (-20, -hip + 26)], skin, shade=0.9))  # neckline
        return out

    def head(p):
        blink = p.get('blink', 0.0)
        mouth = p.get('mouth', 0.0)
        lk = p.get('look', 0.0) * 4
        es = p.get('eyes', 1.0)
        out = [P([(-20, -16), (20, -16), (20, 14), (-20, 14)], skin, shade=0.85)]
        # hair behind the face
        if style in ('long_wavy', 'veil'):
            back = [(-96, -150), (-104, -40), (-112, 60), (-80, 90), (80, 90), (112, 60), (104, -40), (96, -150)]
            out.append(P(back, '#D9CBB0' if style == 'veil' else hair, crease=[((0, -150), (0, 90), 0.08)]))
        if style != 'short' or headwear != 'helmet':
            out.append(E(0, -112, 84, 100, hair, n=16))
        out.append(E(0, -100, 72, 92, skin, n=12, crease=[((0, -190), (0, -10), 0.05)]))
        out.append(P([(-2, -102), (12, -66), (-6, -62)], skin, shade=0.84, shadow=0.6, rim=0.6))  # nose
        if blush:
            out += [E(-42, -64, 12, 8, '#E07A5F', paint=True, soft=4, alpha=0.5),
                    E(42, -64, 12, 8, '#E07A5F', paint=True, soft=4, alpha=0.5)]
        for sx in (-1, 1):
            ex = sx * 30 + lk
            br = p.get('brow', 0.0) * sx
            if blink > 0.7:
                out.append(P([(ex - 8, -106), (ex + 8, -106), (ex + 8, -103), (ex - 8, -103)], INK, paint=True))
            else:
                out.append(E(ex, -106, 7 * es, 9 * es * (1 - blink) + 0.5, INK, paint=True))
                out.append(E(ex + 2 * es, -110, 2.2 * es, 2.2 * es, '#FFFFFF', paint=True, rough=0))
            dy = -6 * (es - 1)
            bc = hair if style not in ('beard_long',) else '#B8B2A6'
            out.append(P([(sx * 18, -130 + 4 * br + dy), (sx * 30, -134 + dy), (sx * 44, -131 - 4 * br + dy),
                          (sx * 44, -126 - 4 * br + dy), (sx * 30, -129 + dy), (sx * 18, -125 + 4 * br + dy)], bc, paint=True))
        # beards
        if style == 'beard_long':
            out.append(P([(-70, -84), (70, -84), (64, -10), (36, 48), (0, 74), (-36, 48), (-64, -10)], hair,
                         crease=[((0, -84), (0, 74), 0.08), ((-30, -60), (-20, 50), 0.06)]))
        elif style == 'beard_short':
            out.append(P([(-68, -78), (68, -78), (60, -20), (30, 4), (0, 12), (-30, 4), (-60, -20)], hair))
        if style in ('beard_long', 'beard_short'):
            out.append(P([(-34, -62), (0, -70), (34, -62), (24, -54), (0, -60), (-24, -54)], hair, shade=0.9))
            m_col = '#3A1A1A'
            out.append(E(0, -46, 12, 2 + 8 * mouth, m_col, paint=True))
        else:
            if mouth > 0.05:
                out.append(E(0, -42, 9, 2 + 9 * mouth, '#5A1E1E', paint=True))
            else:
                out.append(P([(-9, -44), (0, -40), (9, -44), (0, -38)], '#7A2A2A', paint=True))
        # hair in front / on top
        if style == 'bun':
            out.append(E(0, -210, 38, 32, hair, n=12, crease=[((-30, -210), (30, -210), 0.1)]))
            out.append(P([(-78, -140), (-60, -186), (0, -196), (60, -186), (78, -140), (30, -170), (0, -160), (-30, -170)], hair))
        elif style in ('long_wavy',):
            out.append(P([(-80, -130), (-62, -186), (0, -198), (62, -186), (80, -130), (40, -168), (-10, -150), (-50, -164)], hair))
        elif style == 'veil':
            out.append(P([(-90, -140), (-70, -196), (0, -212), (70, -196), (90, -140), (60, -172), (0, -184), (-60, -172)], '#D9CBB0'))
        elif style in ('beard_long', 'beard_short', 'short') and headwear != 'helmet':
            wav = [(-80, -128), (-74, -176), (-36, -200), (0, -204), (36, -200), (74, -176), (80, -128),
                   (62, -150), (44, -136), (24, -158), (4, -140), (-18, -160), (-40, -140), (-60, -156)]
            out.append(P(wav, hair))
        # headwear
        if headwear == 'laurel':
            for k in range(-5, 6):
                if k == 0:
                    continue
                a = math.radians(-90 + k * 15)
                cx, cy = 86 * math.cos(a), -112 + 100 * math.sin(a)
                out.append(P(ellipse_pts(cx, cy, 16, 7, a + math.pi / 2 * (1 if k > 0 else -1) * 0.6, n=10), GOLD, glow=0.04))
        elif headwear == 'diadem':
            pts = [(-66, -178), (-50, -214), (-30, -190), (0, -232), (30, -190), (50, -214), (66, -178)]
            out.append(P(pts, GOLD, crease=[((0, -232), (0, -178), 0.1)], glow=0.05))
            out.append(E(0, -198, 8, 8, '#D2453A', n=10, paint=True))
        elif headwear == 'helmet':
            out.append(P(chamfer([(-92, -118), (-86, -196), (0, -224), (86, -196), (92, -118), (66, -128), (0, -150),
                                  (-66, -128)], 6), '#B07A3A', crease=[((0, -224), (0, -150), 0.1)]))
            out.append(P([(-12, -150), (12, -150), (9, -98), (-9, -98)], '#B07A3A', shade=0.9))  # nose guard
            crest = [(-84, -196), (-44, -262), (20, -278), (82, -252), (92, -196), (40, -212), (-20, -214)]
            out.append(P(crest, '#C8553D', crease=[((-40, -258), (60, -214), 0.1)]))
        return out

    def arm(side):
        def parts(p):
            return [
                P([(-30, -4), (30, -4), (26, 70), (-26, 70)], robe, shade=0.94),  # short sleeve
                P([(-20, 50), (20, 50), (21, 252), (-21, 252)], skin, shade=0.95, crease=[((0, 60), (0, 252), 0.05)]),
                P([(-22, 236), (22, 236), (22, 250), (-22, 250)], trim, rim=0),  # bracelet
                E(0, 276, 24, 26, skin, n=12),
            ]
        return parts

    def prop(p):
        kind = p.get('prop', default_prop)
        if kind == 'bolt':
            z = [(-6, -10), (30, -110), (6, -112), (40, -220), (-24, -96), (2, -94), (-30, -10)]
            return [P(z, '#FFD23F', glow=0.18, crease=[((-6, -10), (40, -220), 0.08)])]
        if kind == 'trident':
            return [P([(-5, 60), (5, 60), (5, -300), (-5, -300)], '#8A6A3A'),
                    P([(-46, -300), (46, -300), (46, -286), (-46, -286)], GOLD),
                    P([(-46, -300), (-38, -300), (-42, -370)], GOLD), P([(-4, -300), (4, -300), (0, -390)], GOLD),
                    P([(38, -300), (46, -300), (42, -370)], GOLD)]
        if kind == 'spear':
            return [P([(-5, 80), (5, 80), (5, -320), (-5, -320)], '#8A6A3A', crease=[((0, 80), (0, -320), 0.1)]),
                    P([(-16, -320), (16, -320), (0, -390)], '#B9B4A8')]
        if kind == 'goblet':
            return [P([(-30, -70), (30, -70), (16, -30), (-16, -30)], GOLD), P([(-4, -30), (4, -30), (4, -6), (-4, -6)], GOLD),
                    P([(-20, -8), (20, -8), (20, 0), (-20, 0)], GOLD)]
        if kind == 'apple':
            return [E(0, -34, 26, 24, '#E8B43A', n=14, glow=0.10), P([(-2, -58), (2, -58), (6, -72), (2, -72)], '#5A3A22', rim=0),
                    P(ellipse_pts(12, -66, 10, 5, -0.5, n=8), '#4E6E44')]
        if kind == 'scroll':
            return [P([(-40, -60), (40, -60), (40, -10), (-40, -10)], '#EFE3C4', pat='hplanks', pat_period=10),
                    E(-42, -35, 8, 28, '#C9B48A', n=10), E(42, -35, 8, 28, '#C9B48A', n=10)]
        return []

    def make():
        bones = {
            'root': dict(parent=None, off=(0, -hip), parts=lambda p: []),
            'legL': dict(parent='root', off=(-40, 0), parts=legs(-1)),
            'legR': dict(parent='root', off=(40, 0), parts=legs(1)),
            'torso': dict(parent='root', off=(0, 0), parts=torso),
            'head': dict(parent='torso', off=(0, -hip - 8), parts=head),
            'armR': dict(parent='torso', off=(-96, -hip + 18), rest=8, parts=arm(-1)),
            'armL': dict(parent='torso', off=(96, -hip + 18), rest=-8, parts=arm(1)),
            'held': dict(parent='armL', off=(0, 276), hang=True, parts=prop),
        }
        order = ['legL', 'legR', 'torso', 'head', 'armR', 'armL', 'held']
        return Rig(bones, order, 2 * hip + 240)
    make.leg = leg
    return make


FIGURES = {
    'zeus': dict(robe='#EDE6D6', robe2='#3F6FA8', hair='#E8E4DA', style='beard_long', headwear='laurel',
                 skin=SKIN_M, default_prop=None),
    'hera': dict(robe='#2F6F73', robe2='#6A4560', hair='#2B1E1A', style='bun', headwear='diadem', blush=True,
                 height='mid', skin=SKIN_L),
    'aphrodite': dict(robe='#F0B9A8', robe2='#EDE6D6', hair='#C9773A', style='long_wavy', headwear=None, blush=True,
                      height='mid', skin=SKIN_L),
    'ares': dict(robe='#8C3B2E', robe2='#5B4636', trim='#B07A3A', hair='#2B1E1A', style='beard_short',
                 headwear='helmet', skirt='short', skin=SKIN_M),
    'mortal_man': dict(robe='#C9A777', robe2='#7A5638', trim='#8C3B2E', hair='#3A2A22', style='short',
                       skirt='short', skin=SKIN_D),
    'mortal_woman': dict(robe='#7E7A9A', robe2='#D9CBB0', trim='#C8553D', hair='#2B1E1A', style='veil',
                         height='mid', blush=True, skin=SKIN_M),
}
SCALE = {'zeus': 0.84, 'hera': 0.80, 'aphrodite': 0.80, 'ares': 0.84, 'mortal_man': 0.80, 'mortal_woman': 0.78}


def add_figure(name, scale=0.8, **opts):
    """Register a new Greek figure (same look as the starter cast). Returns the factory."""
    f = _figure(**opts)
    C.CAST[name] = f
    LEGS[name] = f.leg
    _register_pose(name, scale)
    return f


LEGS = {}


def _register_pose(name, scale):
    try:
        import director as DR
    except Exception:
        return
    DR.POSES.setdefault(name, DR.HUMAN)
    DR.DEFAULT_SCALE.setdefault(name, scale)
    DR.LEG.setdefault(name, LEGS[name])


for _n, _o in FIGURES.items():
    _f = _figure(**_o)
    C.CAST[_n] = _f
    LEGS[_n] = _f.leg


# ================================================================ sets
def column(L, x, top, bottom, w=56, color=MARBLE):
    L.rect(x - w / 2 - 10, top - 26, x + w / 2 + 10, top, color, shade=0.95)  # capital
    L.rect(x - w / 2 - 6, top - 36, x + w / 2 + 6, top - 26, color)
    L.poly([(x - w / 2, top), (x + w / 2, top), (x + w / 2 + 4, bottom), (x - w / 2 - 4, bottom)], color,
           pat='vstripes', pat_period=max(6, w / 5), crease=[((x, top), (x, bottom), 0.06)])
    L.rect(x - w / 2 - 10, bottom, x + w / 2 + 10, bottom + 18, color, shade=0.92)


def temple_front(L, cx, base, width, height, color=MARBLE, n=6):
    top = base - height
    L.rect(cx - width / 2 - 30, base, cx + width / 2 + 30, base + 22, color, shade=0.9)
    L.rect(cx - width / 2 - 50, base + 22, cx + width / 2 + 50, base + 44, color, shade=0.86)
    for k in range(n):
        x = cx - width / 2 + 30 + k * (width - 60) / (n - 1)
        column(L, x, top, base, w=width / (n * 2.2), color=color)
    L.rect(cx - width / 2 - 20, top - 70, cx + width / 2 + 20, top - 36, color, shade=0.96, pat='vstripes', pat_period=22)
    L.poly([(cx - width / 2 - 30, top - 70), (cx + width / 2 + 30, top - 70), (cx, top - 70 - height * 0.32)], color,
           crease=[((cx, top - 70 - height * 0.32), (cx, top - 70), 0.08)])


def olive(L, x, base, h, seed=1):
    r = np.random.default_rng(seed)
    L.poly([(x - 10, base), (x + 10, base), (x + 18 + r.uniform(-8, 8), base - h * 0.55), (x + 4, base - h * 0.6),
            (x - 14, base - h * 0.5)], '#6E5A44', crease=[((x, base), (x + 6, base - h * 0.55), 0.1)])
    for k in range(9):
        a = r.uniform(0, 2 * math.pi)
        L.ellipse(x + 6 + math.cos(a) * h * 0.26, base - h * 0.68 + math.sin(a) * h * 0.16, h * 0.17, h * 0.1,
                  ['#7F8F5A', '#6E7E4E', '#8FA06A'][k % 3], rot=a, n=10)


def build_temple(variant='day'):
    night, dusk = variant == 'night', variant == 'dusk'
    its = []
    if night:
        sky = S.sky_bands(501, '#101A33', [(320, '#16244A', 24), (560, '#1E2F58', 28), (800, '#2A3C68', 22)])
        sky.ellipse(800, 420, 80, 80, '#F4EFE6', glow=0.12)
    elif dusk:
        sky = S.sky_bands(501, '#2A4560', [(280, '#3E5470', 26), (500, '#6B5C80', 28), (700, '#C9727A', 22), (880, '#F2A465', 18)])
        sky.ellipse(260, 900, 110, 110, '#FFD98A', glow=0.10)
    else:
        sky = S.sky_bands(501, '#6FA8C8', [(380, '#87BBD3', 26), (640, '#A9D0DA', 20), (880, '#D3E6E0', 14)])
        sky.ellipse(820, 330, 86, 86, '#FFF2C8', glow=0.10)
    its.append(S.item(sky, 10, 0, key=f'temple-sky-{variant}'))
    cl = S.clouds(502, [(250, 420, 0.9), (780, 600, 1.0)], '#3A4A70' if night else ('#F3C7A6' if dusk else '#F4EFE6'))
    its.append(S.item(cl, 9.5, 0.6, x=-200, key=f'temple-cloud-{variant}', move=lambda t: (5 * t, 0)))
    sea = S.Layer(W, H, seed=503)
    sea.poly(S.band(1000, 6, 400, 0, H), '#1F3A5A' if night else ('#4E6A8C' if dusk else '#3C86A8'), pat='hplanks', pat_period=36)
    its.append(S.item(sea, 8.5, 0.6, key=f'temple-sea-{variant}'))
    hill = S.Layer(W, H, seed=504)
    hill.poly(S.hill(1180, 220, 31, H), '#3B3550' if night else ('#8C6A5E' if dusk else '#B4A06E'), grad=0.06)
    its.append(S.item(hill, 7.5, 1.0, key=f'temple-hill-{variant}'))
    tl = S.Layer(W, H, seed=505)
    temple_front(tl, 560, 1060, 520, 300, color='#8E8AA6' if night else MARBLE)
    its.append(S.item(tl, 6.2, 1.0, key=f'temple-front-{variant}'))
    trees = S.Layer(W, H, seed=506)
    olive(trees, 120, 1300, 420, 3)
    olive(trees, 960, 1320, 380, 5)
    its.append(S.item(trees, 4.0, 1.0, key=f'temple-trees-{variant}'))
    ground = S.Layer(W, H, seed=507)
    ground.poly(S.hill(1560, 24, 41, H + 20), '#C9B48A' if not night else '#5A5470', pat='check', pat_period=60, grad=0.12)
    its.append(S.item(ground, 2.4, 0.3, key=f'temple-ground-{variant}'))
    fg = S.Layer(W, H, seed=508)
    column(fg, 40, 1380, H - 40, w=110, color=MARBLE_SH if not night else '#6A6688')
    fg.poly([(W - 220, H + 20), (W - 160, 1700), (W - 60, 1660), (W + 40, 1700), (W + 40, H + 20)], '#9A8E78')
    its.append(S.item(fg, 0.8, 1.5, key=f'temple-fg-{variant}'))

    def glows(t):
        if night:
            return [(800, 420, 380, '#9FB7FF', 0.16), (560, 900, 160, '#FFB060', 0.10)]
        if dusk:
            return [(260, 900, 520, '#FF9A4D', 0.22)]
        return [(820, 330, 480, '#FFF2D0', 0.10)]
    return dict(items=its, glows=glows, floor=1650, focus=2.0, light='night' if night else ('dusk' if dusk else 'day'),
                marks={'L': 250, 'CL': 400, 'C': 540, 'CR': 680, 'R': 820})


def build_olympus(variant='day'):
    storm = variant == 'storm'
    its = []
    sky = S.sky_bands(601, '#2E3550' if storm else '#7FB0D8',
                      [(300, '#3A4266', 26), (560, '#4A5278', 24), (820, '#5E6690', 18)] if storm else
                      [(360, '#98C2E2', 26), (620, '#BBD6EA', 20), (860, '#E6EEF0', 14)])
    its.append(S.item(sky, 10, 0, key=f'olympus-sky-{variant}'))
    mt = S.Layer(W, H, seed=602)
    mt.poly([(-60, 1100), (200, 760), (380, 900), (600, 620), (860, 880), (1140, 1100), (1140, H), (-60, H)],
            '#5E5A7A' if storm else '#9C9AB8', crease=[((600, 620), (640, 1100), 0.12), ((200, 760), (240, 1100), 0.12)])
    mt.poly([(560, 680), (600, 620), (650, 690), (620, 700), (600, 680), (580, 700)], '#F4EFE6')
    its.append(S.item(mt, 8.5, 1.0, key=f'olympus-mt-{variant}'))
    cl = S.clouds(603, [(200, 1000, 1.6), (560, 1060, 1.9), (920, 990, 1.6)], '#4A5070' if storm else '#F4EFE6')
    its.append(S.item(cl, 7.0, 0.6, x=-200, y=0, key=f'olympus-cloudbank-{variant}', move=lambda t: (4 * math.sin(t * 0.3) * 6, 0)))
    hall = S.Layer(W, H, seed=604)
    for x in (130, 950):
        column(hall, x, 760, 1420, w=80, color=MARBLE)
    hall.rect(60, 700, W - 60, 740, MARBLE, shade=0.95, pat='vstripes', pat_period=26)
    # Zeus's golden throne, centre stage between the marks (actors stand at CL / CR beside it)
    cx = 550
    hall.poly([(cx - 150, 1000), (cx - 110, 880), (cx, 820), (cx + 110, 880), (cx + 150, 1000)], GOLD, shade=0.95, glow=0.04,
              crease=[((cx, 820), (cx, 1000), 0.1)])
    hall.poly(chamfer([(cx - 130, 1000), (cx + 130, 1000), (cx + 120, 1440), (cx - 120, 1440)], 12), GOLD,
              crease=[((cx, 1000), (cx, 1440), 0.08)], glow=0.04)
    hall.rect(cx - 160, 1240, cx + 160, 1290, '#8C3B2E')
    for sx in (-1, 1):
        hall.rect(cx + sx * 150 - 18, 1150, cx + sx * 150 + 18, 1440, '#C9A04A')
    hall.ellipse(cx, 900, 26, 26, '#D2453A', n=12, paint=True)
    its.append(S.item(hall, 5.0, 1.0, key=f'olympus-hall-{variant}'))
    floor = S.Layer(W, H, seed=605)
    floor.poly(S.band(1500, 18, 300, 0, H + 20), '#E8E4DA' if not storm else '#8A8EA8', pat='check', pat_period=80, grad=0.12)
    its.append(S.item(floor, 2.4, 0.3, key=f'olympus-floor-{variant}'))
    fg = S.clouds(606, [(80, 1780, 1.6), (1000, 1800, 1.5)], '#F4EFE6' if not storm else '#5A6080')
    its.append(S.item(fg, 0.8, 1.5, x=-200, y=0, key=f'olympus-fg-{variant}'))

    def glows(t):
        g = [(550, 1200, 420, '#FFE7A8', 0.14)]
        if storm:
            flash = max(0.0, math.sin(t * 2.1)) ** 24
            g = [(700, 500, 700, '#CFE0FF', 0.10 + 0.40 * flash)]
        return g
    return dict(items=its, glows=glows, floor=1640, focus=2.0, light='night' if storm else 'day',
                marks={'L': 260, 'CL': 400, 'C': 550, 'CR': 700, 'R': 820})


def build_sea_cliff(variant='day'):
    storm = variant == 'storm'
    its = []
    sky = S.sky_bands(701, '#28304A' if storm else '#78B4D2',
                      [(320, '#323B58', 24), (600, '#3E4866', 22)] if storm else [(400, '#94C6DC', 24), (720, '#C3E0E4', 16)])
    its.append(S.item(sky, 10, 0, key=f'cliff-sky-{variant}'))
    cl = S.clouds(702, [(300, 380, 1.2), (820, 520, 1.0)], '#4A5070' if storm else '#F4EFE6')
    its.append(S.item(cl, 9.5, 0.6, x=-200, key=f'cliff-cloud-{variant}', move=lambda t: ((14 if storm else 5) * t, 0)))
    cols = ['#1E3A52', '#1A3348', '#162C40', '#12263A'] if storm else ['#3C86A8', '#33789A', '#2A6A8A', '#225C7A']
    for k, (y, z) in enumerate([(1040, 7), (1140, 6), (1260, 5), (1400, 4.2)]):
        its.append(S.wave_strip(y, cols[k], 180 + 40 * k, (14 if storm else 8) + 3 * k, 710 + k, (40 if storm else 22) + 10 * k,
                                1 if k % 2 else -1, z, 0.6, key=f'cliff-wave{k}-{variant}'))
        if k == 1:
            ship = S.Layer(420, 420, seed=720)
            bx, by = 210, 330
            ship.poly([(bx - 150, by - 40), (bx + 150, by - 40), (bx + 110, by + 20), (bx - 110, by + 20)], '#7A5638',
                      pat='hplanks', pat_period=14, crease=[((bx - 150, by - 20), (bx + 150, by - 20), 0.1)])
            ship.rect(bx - 4, by - 280, bx + 4, by - 40, '#3A2A22', rim=0)
            ship.poly([(bx - 110, by - 260), (bx + 110, by - 260), (bx + 96, by - 90), (bx - 96, by - 90)], '#EDE6D6',
                      pat='vstripes', pat_period=40)
            ship.ellipse(bx + 150, by - 30, 16, 12, '#2F6F73', n=10)
            its.append(S.item(ship, z - 0.2, 0.7, x=520, y=780, key='cliff-ship',
                              move=lambda t: (18 * math.sin(t * 0.5), (9 if storm else 5) * math.sin(t * 1.4))))
    cliff = S.Layer(W, H, seed=730)
    cliff.poly([(-60, 900), (120, 880), (300, 980), (380, 1200), (420, 1480), (380, H + 20), (-60, H + 20)], '#E4DCCB',
               crease=[((120, 880), (200, 1500), 0.10), ((300, 980), (330, 1500), 0.08)], pat='hplanks', pat_period=90)
    cliff.poly([(-60, 880), (120, 860), (300, 960), (290, 990), (120, 900), (-60, 920)], '#7F9A5A')
    its.append(S.item(cliff, 3.0, 1.0, key=f'cliff-rock-{variant}'))
    ledge = S.Layer(W, H, seed=731)
    ledge.poly(S.hill(1560, 22, 51, H + 20), '#CFC5B0', grad=0.12, pat='check', pat_period=70)
    its.append(S.item(ledge, 2.4, 0.3, key=f'cliff-ledge-{variant}'))
    fg = S.Layer(W, H, seed=732)
    for i in range(6):
        bx = W - 260 + i * 50
        fg.poly([(bx, H + 20), (bx + 30, H + 20), (bx + 20, H - 300 + 30 * (i % 3)), (bx + 8, H - 310)], ['#6E7E4E', '#7F8F5A'][i % 2])
    its.append(S.item(fg, 0.8, 1.5, key=f'cliff-fg-{variant}'))

    def glows(t):
        if storm:
            flash = max(0.0, math.sin(t * 1.7 + 1)) ** 30
            return [(760, 380, 700, '#CFE0FF', 0.08 + 0.45 * flash)]
        return [(860, 300, 480, '#FFF2D0', 0.10)]
    return dict(items=its, glows=glows, floor=1650, focus=2.0, light='night' if storm else 'day',
                marks={'L': 260, 'CL': 400, 'C': 560, 'CR': 690, 'R': 820})


def build_cave(variant='fire'):
    fire = variant == 'fire'
    its = []
    back = S.Layer(W, H, seed=801)
    back.rect(0, 0, W, H, '#2A2026', rim=0, shadow=0, rough=0)
    for k, (y, c) in enumerate([(300, '#352830'), (620, '#3E2E34'), (960, '#47343A')]):
        back.poly(S.hill(y, 160, 81 + k, H), c)
    its.append(S.item(back, 10, 0, key=f'cave-back-{variant}'))
    arch = S.Layer(W, H, seed=802)
    arch.poly([(-60, -20), (W + 60, -20), (W + 60, 1300), (900, 1200), (860, 700), (700, 380), (380, 360), (200, 700),
               (160, 1200), (-60, 1300)], '#5A4448', crease=[((380, 360), (200, 1200), 0.10), ((700, 380), (900, 1200), 0.10)])
    for (x, y, r) in [(120, 400, 60), (980, 520, 80), (300, 180, 50), (820, 160, 70)]:
        arch.ellipse(x, y, r, r * 0.7, '#4E3A3E', n=7)
    its.append(S.item(arch, 6.0, 1.2, key=f'cave-arch-{variant}'))
    rocks = S.Layer(W, H, seed=803)
    for (x, y, r) in [(140, 1380, 120), (960, 1400, 140), (820, 1330, 70)]:
        rocks.ellipse(x, y, r, r * 0.6, '#5E4A4E', n=7, crease=[((x - r, y), (x + r, y - 10), 0.1)])
    if fire:
        rocks.ellipse(560, 1440, 120, 30, '#3A2A26', n=10)
        for k, c in enumerate(['#D2453A', '#E0A33A', '#FFD98A']):
            s_ = 1 - k * 0.28
            rocks.poly([(560 - 90 * s_, 1440), (560 - 40 * s_, 1300 - 20 * k), (560, 1240 + 30 * k), (560 + 50 * s_, 1310 - 20 * k),
                        (560 + 90 * s_, 1440)], c, glow=0.12 + 0.05 * k)
    its.append(S.item(rocks, 3.4, 1.0, key=f'cave-rocks-{variant}'))
    floor = S.Layer(W, H, seed=804)
    floor.poly(S.hill(1540, 20, 91, H + 20), '#4A3A3A', grad=0.14)
    its.append(S.item(floor, 2.4, 0.3, key=f'cave-floor-{variant}'))
    fg = S.Layer(W, H, seed=805)
    fg.poly([(-60, H + 20), (-60, 1500), (120, 1620), (200, H + 20)], '#2E2226')
    fg.poly([(W + 60, H + 20), (W + 60, 1480), (900, 1640), (840, H + 20)], '#2E2226')
    its.append(S.item(fg, 0.8, 1.5, key=f'cave-fg-{variant}'))

    def glows(t):
        if not fire:
            return [(540, 600, 400, '#6A7AA8', 0.08)]
        fl = 0.04 * math.sin(t * 9) + 0.03 * math.sin(t * 14.3)
        return [(560, 1320, 520, '#FF8A3D', 0.34 + fl), (560, 1300, 160, '#FFD98A', 0.22 + fl)]
    return dict(items=its, glows=glows, floor=1650, focus=2.0, light='lamp' if fire else 'night',
                marks={'L': 260, 'CL': 400, 'C': 560, 'CR': 700, 'R': 820})


GREEK_SETS = {'temple': build_temple, 'olympus': build_olympus, 'sea_cliff': build_sea_cliff, 'cave': build_cave}
GREEK_VARIANTS = {'temple': ['day', 'dusk', 'night'], 'olympus': ['day', 'storm'], 'sea_cliff': ['day', 'storm'],
                  'cave': ['fire', 'dark']}
S.SETS.update(GREEK_SETS)
S.VARIANTS.update(GREEK_VARIANTS)
