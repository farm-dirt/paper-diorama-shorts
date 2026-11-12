"""Original cast for paper-diorama-shorts (designed for this skill, not from any film), built as simple 2D rigs.

Each character = bones (parent, offset, parts(pose)). Parts are dicts in the
bone's local space: {'pts': Nx2, 'color': hex, ...Layer.poly kwargs}.
Pose keys: bone angles in degrees + 'blink' (0-1), 'mouth' (0-1), 'look' (-1..1),
'eyes' (1 normal, 1.5 wide/shocked, 0.6 squint), 'brow' (-1 worried .. 0 .. 1 angry),
'face' (1 or -1 to flip), 'bob' (px, vertical body offset), 'prop' (e.g. 'oar').

  ILAW      - 9-year-old girl, mustard folded raincoat, black zigzag bob,
              faceted 12-sided paper face, carries a red paper lantern.
  MANG OSO  - old ferryman with a cardboard-box head, folded white
              paper mustache and brows, teal knit sweater, rust cap.
  KUPAS     - a little dog folded from old newspaper; triangle face,
              flop ears, boat-shaped body.
"""
import math
import numpy as np
from paperkit import Layer, ellipse_pts, chamfer

SKIN_A = '#EBC39C'
SKIN_B = '#D49A6A'
INK = '#241C1E'
CREAM = '#F4EFE6'
NEWS = '#ECE2CB'

PALETTE = {
    'Mustard': '#E0A33A', 'Terracotta': '#C8553D', 'Deep teal': '#2F6F73',
    'Lantern red': '#D2453A', 'Rust': '#8C3B2E', 'Newsprint': NEWS,
    'Dusk plum': '#6A4560', 'Ink': INK,
}


def mx(pts):
    p = np.array(pts, np.float32)
    p[:, 0] *= -1
    return p


def P(pts, color, **kw):
    d = dict(pts=np.asarray(pts, np.float32), color=color)
    d.update(kw)
    return d


def E(cx, cy, rx, ry, color, n=None, **kw):
    return P(ellipse_pts(cx, cy, rx, ry, n=n), color, **kw)


def _M(tx, ty, ang=0.0, s=1.0, sx=1.0):
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return np.array([[c * s * sx, -sn * s, tx], [sn * s * sx, c * s, ty], [0, 0, 1]], np.float32)


def _apply(M, pts):
    pts = np.asarray(pts, np.float32)
    return pts @ M[:2, :2].T + M[:2, 2]


class Rig:
    def __init__(self, bones, order, height):
        self.bones, self.order, self.height = bones, order, height

    def draw(self, layer, x, y, scale, pose):
        pose = dict(pose)
        face = pose.get('face', 1)
        world = {}

        def W(name):
            if name in world:
                return world[name]
            b = self.bones[name]
            ang = pose.get(name, b.get('rest', 0.0))
            if b['parent'] is None:
                M = _M(x, y + pose.get('bob', 0) * scale, 0, scale, face) @ _M(*b['off'], ang)
            else:
                M = W(b['parent']) @ _M(*b['off'], ang)
            if b.get('hang'):  # keep the bone hanging straight down (lanterns)
                M = _M(M[0, 2], M[1, 2], pose.get(name, 0.0), scale, face)
            world[name] = M
            return M

        self.world = world
        for name in self.order:
            M = W(name)
            for part in self.bones[name]['parts'](pose):
                kw = {k: v for k, v in part.items() if k not in ('pts', 'color')}
                if 'crease' in kw:
                    kw['crease'] = [(_apply(M, [p])[0], _apply(M, [q])[0], dk)
                                    for (p, q, dk) in kw['crease']]
                layer.poly(_apply(M, part['pts']), part['color'], **kw)

    def render(self, pose=None, scale=1.0, seed=1, pad=60):
        """Render alone onto a transparent layer. Returns (layer, feet_x, feet_y)."""
        w = int((max(self.height * 0.9, 420) + 2 * pad) * scale)
        h = int((self.height + 2 * pad) * scale)
        L = Layer(w, h, seed=seed, scale=scale)
        self.draw(L, w / 2, h - pad * scale, scale, pose or {})
        return L, w / 2, h - pad * scale


# =============================================================== ILAW
def ilaw():
    MUST = '#E0A33A'

    def leg(side):
        def parts(p):
            f = (lambda a: a)
            return [
                P([(-13, 0), (13, 0), (12, 205), (-12, 205)], '#2B3A55'),
                P(f([(-15, 186), (15, 186), (16, 226), (30, 232), (34, 252), (-17, 252)]) if side > 0 else
                  mx([(-15, 186), (15, 186), (16, 226), (30, 232), (34, 252), (-17, 252)]),
                  '#C8553D', crease=[((-15, 222), (16, 222), 0.12)]),
            ]
        return parts

    def torso(p):
        coat = chamfer([(-62, -205), (62, -205), (114, 85), (-114, 85)], 14)
        return [
            P(coat, MUST, crease=[((0, -205), (0, 85), 0.10)]),
            P([(-30, -205), (0, -150), (-6, -205)], MUST, shade=0.86),
            P([(30, -205), (0, -150), (6, -205)], MUST, shade=0.80),
            P([(-92, 2), (-38, 2), (-36, 18), (-94, 18)], MUST, shade=0.88),
            P([(92, 2), (38, 2), (36, 18), (94, 18)], MUST, shade=0.84),
            E(12, -125, 6, 6, '#3A2A22', n=10), E(12, -70, 6, 6, '#3A2A22', n=10),
            E(12, -15, 6, 6, '#3A2A22', n=10),
        ]

    def head(p):
        blink = p.get('blink', 0.0)
        mouth = p.get('mouth', 0.0)
        lk = p.get('look', 0.0) * 4
        out = [
            P([(-15, -14), (15, -14), (15, 12), (-15, 12)], SKIN_A, shade=0.85),
            E(0, -95, 106, 112, MUST, n=20, shade=0.90),
            E(0, -96, 85, 92, INK, n=18),
            E(0, -90, 70, 80, SKIN_A, n=12, crease=[((0, -170), (0, -10), 0.05)]),
            P([(-3, -86), (9, -68), (-6, -64)], SKIN_A, shade=0.84, shadow=0.6, rim=0.6),
        ]
        bang = [(-80, -118), (-74, -168), (-30, -186), (30, -186), (74, -168), (80, -118)]
        zig = [(80, -118), (62, -138), (46, -122), (26, -142), (8, -124), (-12, -144),
               (-30, -124), (-50, -142), (-64, -124)]
        out.append(P(bang + zig[1:], INK))
        hood = np.concatenate([ellipse_pts(0, -96, 104, 112, a0=math.radians(195), a1=math.radians(345), n=16),
                               ellipse_pts(0, -96, 84, 94, a0=math.radians(345), a1=math.radians(195), n=16)[::-1][::-1]])
        out.append(P(hood, MUST))
        out += [
            E(-44, -60, 13, 9, '#E07A5F', paint=True, soft=4, alpha=0.55),
            E(44, -60, 13, 9, '#E07A5F', paint=True, soft=4, alpha=0.55),
        ]
        for sx in (-1, 1):
            ex = sx * 28 + lk
            es = p.get('eyes', 1.0)
            br = p.get('brow', 0.0) * sx
            if blink > 0.7:
                out.append(P([(ex - 8, -88), (ex + 8, -88), (ex + 8, -85), (ex - 8, -85)], INK, paint=True))
            else:
                out.append(E(ex, -88, 7 * es, 10 * es * (1 - blink), INK, paint=True))
                out.append(E(ex + 2 * es, -92 - 2 * (es - 1), 2.4 * es, 2.4 * es, '#FFFFFF', paint=True, rough=0))
            dy = -6 * (es - 1)
            out.append(P([(sx * 20, -114 + 4 * br + dy), (sx * 29, -117 + dy), (sx * 38, -115 - 4 * br + dy),
                          (sx * 38, -112 - 4 * br + dy), (sx * 29, -114 + dy), (sx * 20, -111 + 4 * br + dy)], INK, paint=True))
        if mouth > 0.05:
            out.append(E(0, -46, 9, 2 + 9 * mouth, '#5A1E1E', paint=True))
        else:
            out.append(P([(-8, -48), (0, -44), (8, -48), (0, -42)], '#5A1E1E', paint=True))
        return out

    def arm(side):
        def parts(p):
            return [
                P([(-17, 0), (17, 0), (21, 148), (-21, 148)], MUST, shade=0.96,
                  crease=[((0, 0), (0, 148), 0.07)]),
                P([(-22, 138), (22, 138), (22, 160), (-22, 160)], MUST, shade=0.82),
                E(0, 176, 18, 19, SKIN_A, n=12),
            ]
        return parts

    def lantern(p):
        ribs = [((x, 50), (x, 132), 0.05) for x in (-24, 0, 24)]
        return [
            P([(-2, -4), (2, -4), (2, 50), (-2, 50)], '#3A2A22', rim=0),
            P([(-20, 40), (20, 40), (20, 52), (-20, 52)], '#3A2A22'),
            E(0, 92, 42, 46, '#D2453A', n=16, crease=ribs, glow=0.12),
            E(0, 92, 20, 30, '#FFC46B', paint=True, soft=10, alpha=0.6),
            P([(-20, 132), (20, 132), (20, 142), (-20, 142)], '#3A2A22'),
            P([(-6, 142), (6, 142), (0, 172)], '#E0A33A'),
        ]

    bones = {
        'root': dict(parent=None, off=(0, -250), parts=lambda p: []),
        'legL': dict(parent='root', off=(-30, 0), parts=leg(-1)),
        'legR': dict(parent='root', off=(30, 0), parts=leg(1)),
        'torso': dict(parent='root', off=(0, 0), parts=torso),
        'head': dict(parent='torso', off=(0, -200), parts=head),
        'armR': dict(parent='torso', off=(-64, -188), rest=10, parts=arm(-1)),
        'armL': dict(parent='torso', off=(64, -188), rest=-22, parts=arm(1)),
        'lantern': dict(parent='armL', off=(0, 176), hang=True, parts=lantern),
    }
    order = ['legL', 'legR', 'torso', 'armR', 'head', 'armL', 'lantern']
    return Rig(bones, order, 640)


# =============================================================== MANG OSO
def mang_oso():
    TEAL = '#2F6F73'

    def leg(side):
        def parts(p):
            f = (lambda a: a) if side < 0 else mx
            return [
                P([(-32, 0), (32, 0), (29, 290), (-29, 290)], '#5B4636',
                  crease=[((4, 0), (2, 290), 0.08)]),
                P(f([(-30, 282), (30, 282), (32, 304), (-56, 306), (-58, 320), (34, 320)]), '#2C2522',
                  crease=[((-30, 296), (32, 296), 0.1)]),
            ]
        return parts

    def torso(p):
        body = chamfer([(-100, -330), (100, -330), (110, -40), (98, 34), (-98, 34), (-110, -40)], 16)
        return [
            P(body, TEAL, pat='stripes', pat_period=24, crease=[((22, -330), (12, 34), 0.09)]),
            P([(-44, -348), (44, -348), (48, -318), (-48, -318)], '#E8DCC3'),
            P([(-98, 20), (98, 20), (98, 40), (-98, 40)], TEAL, shade=0.8),
        ]

    def head(p):
        blink = p.get('blink', 0.0)
        mouth = p.get('mouth', 0.0)
        lk = p.get('look', 0.0) * 3
        out = [
            P([(-24, -16), (24, -16), (24, 14), (-24, 14)], SKIN_B, shade=0.8),
            E(-84, -96, 14, 20, SKIN_B, n=10, shade=0.88),
            P(chamfer([(-80, -190), (70, -190), (70, -6), (-80, -6)], 12), SKIN_B),
            P([(70, -188), (94, -174), (94, -16), (70, -6)], SKIN_B, shade=0.74),
        ]
        for sx in (-1, 1):
            ex = sx * 34 - 5 + lk
            es = p.get('eyes', 1.0)
            if blink > 0.6:
                out.append(P([(ex - 7, -106), (ex + 7, -106), (ex + 7, -103), (ex - 7, -103)], INK, paint=True))
            else:
                out.append(E(ex, -106, 6 * es, 7 * es * (1 - blink) + 0.5, INK, paint=True))
        br = p.get('brow', 0.0) * 8
        up = -8 * (p.get('eyes', 1.0) - 1)
        out += [
            P([(-66, -132 - br + up), (-20, -140 + br + up), (-16, -124 + br + up), (-62, -118 - br + up)], CREAM),
            P([(10, -140 + br + up), (54, -134 - br + up), (58, -120 - br + up), (12, -124 + br + up)], CREAM),
            E(-5, -34, 16, 3 + 10 * mouth, '#4A1A1A', paint=True),
            P([(-8, -124), (24, -62), (-18, -58)], SKIN_B, shade=0.80, shadow=0.8),
            P([(-4, -62), (-58, -56), (-82, -30), (-44, -38), (-4, -44)], CREAM,
              crease=[((-4, -54), (-70, -42), 0.12)]),
            P([(-6, -62), (48, -56), (72, -30), (36, -38), (-6, -44)], CREAM,
              crease=[((-6, -54), (60, -42), 0.12)]),
            P([(-90, -165), (-82, -214), (-30, -232), (58, -226), (98, -190), (96, -160)], '#8C3B2E',
              crease=[((-30, -232), (-20, -165), 0.08)]),
            P([(-94, -170), (112, -170), (126, -150), (-92, -150)], '#8C3B2E', shade=0.8),
        ]
        return out

    def oar(p):
        if p.get('prop') != 'oar':
            return []
        return [P([(-6, -420), (6, -420), (6, 200), (-6, 200)], '#9A6A43', crease=[((0, -420), (0, 200), 0.1)]),
                P(chamfer([(-30, 200), (30, 200), (34, 356), (-34, 356)], 18), '#9A6A43',
                  crease=[((0, 200), (0, 356), 0.12)])]

    def arm(side):
        def parts(p):
            return [
                P([(-23, 0), (23, 0), (25, 252), (-25, 252)], TEAL, shade=0.92,
                  crease=[((0, 0), (0, 252), 0.07)]),
                P([(-26, 236), (26, 236), (26, 256), (-26, 256)], '#E8DCC3'),
                E(0, 280, 26, 28, SKIN_B, n=12),
            ]
        return parts

    bones = {
        'root': dict(parent=None, off=(0, -320), parts=lambda p: []),
        'legL': dict(parent='root', off=(-40, 0), parts=leg(-1)),
        'legR': dict(parent='root', off=(40, 0), parts=leg(1)),
        'torso': dict(parent='root', off=(0, 0), parts=torso),
        'head': dict(parent='torso', off=(0, -340), parts=head),
        'armR': dict(parent='torso', off=(-100, -312), rest=8, parts=arm(-1)),
        'armL': dict(parent='torso', off=(100, -312), rest=-8, parts=arm(1)),
        'oar': dict(parent='armR', off=(0, 270), hang=True, parts=oar),
    }
    order = ['legL', 'legR', 'oar', 'torso', 'head', 'armR', 'armL']
    return Rig(bones, order, 860)


# =============================================================== KUPAS
def kupas():
    def leg(shade):
        def parts(p):
            return [P([(-8, 0), (8, 0), (7, 105), (-9, 105)], NEWS, shade=shade, pat='news')]
        return parts

    def body(p):
        return [
            P([(-120, -40), (112, -40), (86, 26), (-96, 26)], NEWS, pat='news',
              crease=[((-120, -8), (112, -8), 0.10)]),
            P([(-120, -40), (112, -40), (102, -27), (-112, -27)], NEWS, shade=1.04),
        ]

    def tail(p):
        return [P([(0, 0), (-34, -66), (14, 6)], NEWS, shade=0.92, pat='news')]

    def head(p):
        blink = p.get('blink', 0.0)
        mouth = p.get('mouth', 0.0)
        out = [
            P([(-50, -72), (50, -72), (0, 44)], NEWS, pat='news',
              crease=[((0, -72), (0, 44), 0.06)]),
            P([(-18, 4), (18, 4), (0, 44)], NEWS, shade=0.9),
        ]
        if mouth > 0.1:
            out.append(P([(-6, 36), (6, 36), (0, 36 + 18 * mouth)], '#C8553D', paint=True))
        out += [
            P([(-50, -72), (-18, -72), (-64, -2)], NEWS, shade=0.76, pat='news',
              crease=[((-34, -72), (-60, -10), 0.08)]),
            P([(50, -72), (18, -72), (64, -2)], NEWS, shade=0.72, pat='news',
              crease=[((34, -72), (60, -10), 0.08)]),
            E(0, 36, 9, 7, INK, paint=True),
        ]
        for sx in (-1, 1):
            if blink > 0.6:
                out.append(P([(sx * 16 - 6, -30), (sx * 16 + 6, -30), (sx * 16 + 6, -27), (sx * 16 - 6, -27)], INK, paint=True))
            else:
                es = p.get('eyes', 1.0)
                out.append(E(sx * 16, -28, 5 * es, 6 * es * (1 - blink) + 0.5, INK, paint=True))
        return out

    bones = {
        'root': dict(parent=None, off=(0, -120), parts=lambda p: []),
        'legBL': dict(parent='root', off=(-70, 10), parts=leg(0.78)),
        'legFL': dict(parent='root', off=(64, 10), parts=leg(0.78)),
        'tail': dict(parent='root', off=(-112, -34), rest=0, parts=tail),
        'body': dict(parent='root', off=(0, 0), parts=body),
        'legBR': dict(parent='root', off=(-46, 14), parts=leg(0.95)),
        'legFR': dict(parent='root', off=(88, 14), parts=leg(0.95)),
        'head': dict(parent='root', off=(104, -52), parts=head),
    }
    order = ['legBL', 'legFL', 'tail', 'body', 'legBR', 'legFR', 'head']
    return Rig(bones, order, 300)


CAST = {'ilaw': ilaw, 'mang_oso': mang_oso, 'kupas': kupas}
