"""Synthesize the food / kitchen sound pack into assets/sfx/ (no downloads, no licence needed).

    python3 tools/make_food_sfx.py            # writes assets/sfx/<name>.wav for every sound below
    python3 tools/make_food_sfx.py --audition OUT.mp3   # also writes one file with all sounds in a row

Sounds: steam_hiss, sizzle, boil_bubbles, water_pour, rice_pour, knife_chop, knife_chops, crunch,
bite_soft, chew, slurp, spoon_scoop, lid_clink, lid_rattle, stomach_growl, sneeze.
Everything is built from filtered noise and short tones, so it is ours (made by this script).
"""
import os, sys, wave, subprocess
import numpy as np

SR = 48000
rng = np.random.default_rng(7)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'sfx')


def n(d):
    return rng.standard_normal(int(d * SR))


def band(x, lo, hi, soft=0.15):
    """Band-pass by FFT mask with soft edges (lo/hi in Hz)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo > 0:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** (2 / soft))
    if hi:
        m *= 1 / (1 + (f / hi) ** (2 / soft))
    return np.fft.irfft(X * m, len(x))


def env(L, a, r, hold=0.0):
    """attack a s, hold, then exponential release with time-constant r s."""
    t = np.arange(L) / SR
    e = np.where(t < a, t / max(a, 1e-4), np.exp(-np.maximum(t - a - hold, 0) / r))
    return e


def fade(x, fi=0.05, fo=0.2):
    x = x.copy()
    a, b = int(fi * SR), int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)
    return x


def place(buf, s, t):
    i = int(t * SR)
    j = min(len(buf), i + len(s))
    if i < len(buf):
        buf[i:j] += s[:j - i]


def norm(x, peak=0.8):
    return x / (np.abs(x).max() + 1e-9) * peak


def burst(d, lo, hi, a=0.001, r=0.01):
    s = band(n(d), lo, hi)
    return s * env(len(s), a, r)


def tone(d, f0, f1=None, r=0.05, a=0.002):
    t = np.arange(int(d * SR)) / SR
    f = np.linspace(f0, f1 or f0, len(t)) if np.isscalar(f0) else f0
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), a, r)


# ---------------- sounds ----------------
def steam_hiss(d=5.0):
    t = np.arange(int(d * SR)) / SR
    wob = 0.75 + 0.25 * np.sin(2 * np.pi * 0.7 * t) * np.sin(2 * np.pi * 0.23 * t + 1)
    s = band(n(d), 2500, 9000) * wob + 0.25 * band(n(d), 900, 2500) * wob
    return norm(fade(s, 0.4, 0.6), 0.5)


def sizzle(d=5.0):
    s = 0.18 * band(n(d), 3000, 12000)
    for _ in range(int(55 * d)):           # fat crackles
        c = burst(0.02, 2500, 11000, 0.0005, rng.uniform(0.002, 0.008)) * rng.uniform(0.2, 1.0)
        place(s, c, rng.uniform(0, d - 0.03))
    for _ in range(int(8 * d)):            # bigger pops
        c = burst(0.04, 1200, 8000, 0.0005, 0.012) * rng.uniform(0.6, 1.3)
        place(s, c, rng.uniform(0, d - 0.05))
    return norm(fade(s, 0.15, 0.4), 0.7)


def bubble(f):
    d = rng.uniform(0.03, 0.08)
    return tone(d, f, f * rng.uniform(1.6, 2.4), r=d / 3, a=0.001)


def boil_bubbles(d=5.0):
    s = 0.15 * band(n(d), 60, 400)
    for _ in range(int(22 * d)):
        place(s, bubble(rng.uniform(250, 700)) * rng.uniform(0.3, 1.0), rng.uniform(0, d - 0.1))
    return norm(fade(s, 0.3, 0.5), 0.65)


def water_pour(d=3.0, lo_start=500, lo_end=1100):
    t = np.arange(int(d * SR)) / SR
    s = np.zeros(len(t))
    # moving band = rising pitch as the pot fills; gurgle by amplitude flutter
    seg = 0.05
    for k in range(int(d / seg)):
        c = lo_start + (lo_end - lo_start) * k * seg / d
        piece = band(n(seg * 2), c * 0.7, c * 2.2) * np.hanning(int(seg * 2 * SR))
        place(s, piece * rng.uniform(0.6, 1.0), k * seg)
    flutter = 0.7 + 0.3 * np.sin(2 * np.pi * 9 * t + rng.uniform(0, 6))
    s = s * flutter + 0.3 * band(n(d), 3000, 8000)
    for _ in range(int(10 * d)):
        place(s, bubble(rng.uniform(400, 900)) * 0.6, rng.uniform(0, d - 0.1))
    return norm(fade(s, 0.15, 0.5), 0.7)


def rice_pour(d=2.0):
    s = np.zeros(int(d * SR))
    for _ in range(int(600 * d)):          # many tiny grain ticks
        c = burst(0.006, 3000, 12000, 0.0002, 0.0012) * rng.uniform(0.1, 1.0)
        place(s, c, rng.uniform(0, d - 0.01))
    return norm(fade(s, 0.2, 0.5), 0.6)


def knife_chop():
    s = np.zeros(int(0.35 * SR))
    place(s, burst(0.01, 3000, 12000, 0.0002, 0.002) * 0.6, 0)        # blade click
    place(s, tone(0.15, 190, 150, r=0.035) * 0.9, 0.002)              # board thump
    place(s, burst(0.08, 700, 2200, 0.0005, 0.02) * 0.7, 0.002)       # wood knock
    return norm(s, 0.85)


def knife_chops(k=5, gap=0.32):
    s = np.zeros(int((k * gap + 0.4) * SR))
    for i in range(k):
        place(s, knife_chop() * rng.uniform(0.75, 1.0), i * gap + rng.uniform(-0.02, 0.02))
    return norm(s, 0.85)


def crunch():
    s = np.zeros(int(0.5 * SR))
    t = 0.0
    for i in range(rng.integers(12, 18)):
        lo = rng.uniform(800, 2500)
        c = burst(0.03, lo, lo * rng.uniform(2.5, 5), 0.0003, rng.uniform(0.003, 0.012))
        place(s, c * rng.uniform(0.4, 1.0) * (1.2 if i == 0 else 1), t)
        t += rng.uniform(0.008, 0.03)
    place(s, tone(0.12, 120, 90, r=0.03) * 0.3, 0)
    return norm(s, 0.85)


def bite_soft():
    s = np.zeros(int(0.45 * SR))
    place(s, burst(0.2, 200, 1800, 0.004, 0.05), 0)                    # soft squish
    for _ in range(6):
        place(s, burst(0.015, 1500, 5000, 0.0005, 0.004) * 0.25, rng.uniform(0, 0.08))
    return norm(s, 0.7)


def chew(k=4):
    s = np.zeros(int((k * 0.38 + 0.3) * SR))
    for i in range(k):
        b = band(n(0.22), 250, 2000) * env(int(0.22 * SR), 0.03, 0.05)
        place(s, b * rng.uniform(0.6, 1.0), i * 0.38)
        for _ in range(3):
            place(s, burst(0.01, 1500, 4000, 0.0005, 0.003) * 0.2, i * 0.38 + rng.uniform(0, 0.12))
    return norm(fade(s, 0.01, 0.1), 0.6)


def slurp(d=1.0):
    t = np.arange(int(d * SR)) / SR
    s = np.zeros(len(t))
    seg = 0.025
    for k in range(int(d / seg)):
        c = 450 + 2300 * (k * seg / d) ** 1.4
        piece = band(n(seg * 2), c * 0.8, c * 1.6, 0.1) * np.hanning(int(seg * 2 * SR))
        place(s, piece, k * seg)
    flutter = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 14 * t))
    s *= flutter * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.6
    for _ in range(8):
        place(s, bubble(rng.uniform(500, 1100)) * 0.35, rng.uniform(0.1, d - 0.1))
    return norm(fade(s, 0.03, 0.12), 0.7)


def spoon_scoop():
    d = 0.55
    s = band(n(d), 1200, 6000) * env(int(d * SR), 0.05, 0.12, hold=0.15) * 0.5
    place(s, lid_clink(soft=True) * 0.35, 0.0)
    for _ in range(80):
        place(s, burst(0.006, 2500, 9000, 0.0002, 0.0015) * rng.uniform(0.05, 0.3), rng.uniform(0.05, 0.4))
    return norm(s, 0.6)


def lid_clink(soft=False):
    d = 0.6
    parts = [(1180, 0.12), (2870, 0.08), (4120, 0.05), (5630, 0.035), (7210, 0.02)]
    s = sum(tone(d, f, r=r * (0.6 if soft else 1.0), a=0.0005) * (1 / (i + 1)) for i, (f, r) in enumerate(parts))
    place(s, burst(0.004, 4000, 14000, 0.0001, 0.001) * 0.5, 0)
    return norm(s, 0.6 if soft else 0.75)


def lid_rattle(d=1.6):
    s = np.zeros(int(d * SR))
    t = 0.0
    while t < d - 0.4:
        place(s, lid_clink(soft=True) * rng.uniform(0.25, 0.8), t)
        t += rng.uniform(0.05, 0.11)
    return norm(fade(s, 0.1, 0.4), 0.65)


def stomach_growl(d=1.6):
    t = np.arange(int(d * SR)) / SR
    f = 95 + 40 * np.sin(2 * np.pi * 1.3 * t) + 25 * np.sin(2 * np.pi * 5.7 * t)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 11 * t))
    gur = band(n(d), 150, 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t) ** 2)
    s = (body * 0.7 + gur * 0.5) * np.sin(np.pi * t / d) ** 0.8
    for _ in range(6):
        place(s, bubble(rng.uniform(180, 320)) * 0.5, rng.uniform(0.1, d - 0.2))
    return norm(s, 0.75)


def sneeze():
    s = np.zeros(int(1.3 * SR))
    ah = band(n(0.55), 400, 2500) * np.linspace(0, 1, int(0.55 * SR)) ** 2 * 0.25   # breath in
    place(s, ah, 0)
    choo = band(n(0.45), 900, 9000) * env(int(0.45 * SR), 0.004, 0.09)
    place(s, choo, 0.62)
    place(s, tone(0.2, 220, 120, r=0.05) * 0.4, 0.62)
    return norm(s, 0.85)


SOUNDS = {'steam_hiss': steam_hiss, 'sizzle': sizzle, 'boil_bubbles': boil_bubbles,
          'water_pour': water_pour, 'rice_pour': rice_pour, 'knife_chop': knife_chop,
          'knife_chops': knife_chops, 'crunch': crunch, 'bite_soft': bite_soft, 'chew': chew,
          'slurp': slurp, 'spoon_scoop': spoon_scoop, 'lid_clink': lid_clink,
          'lid_rattle': lid_rattle, 'stomach_growl': stomach_growl, 'sneeze': sneeze}


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for name, fn in SOUNDS.items():
        x = fn()
        write_wav(os.path.join(OUT, name + '.wav'), x)
        made[name] = x
        print(f'{name:14s} {len(x) / SR:4.1f} s  peak {np.abs(x).max():.2f}')
    if '--audition' in sys.argv:
        out = sys.argv[sys.argv.index('--audition') + 1]
        gap = np.zeros(int(0.7 * SR))
        seq = np.concatenate([np.concatenate([made[k], gap]) for k in SOUNDS])
        tmp = out + '.tmp.wav'
        write_wav(tmp, seq)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-b:a', '192k', out], check=True)
        os.remove(tmp)
        print('audition:', out, f'{len(seq) / SR:.1f} s')
