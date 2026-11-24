#!/usr/bin/env python3
"""foley - makes BRAND-NEW sound effects for one short (no downloads, nothing reused from older shorts).

    python3 tools/foley.py PROJECT_DIR            # writes PROJECT_DIR/project-files/sfx/<name>.wav
    python3 tools/foley.py PROJECT_DIR --audition OUT.mp3

project.json:  "foley": {"step1": {"kind": "snow_step"}, "chime": {"kind": "icicle_chime", "n": 6}, ...}
Every sound is synthesized from noise, tones and physics-style models with a seed taken from the
project slug + the sound's name, so every short gets its own takes of every sound (user rule, 24 Nov
2026: "create something new always"). audio.py loads project-files/sfx/ before the shared library, so
these names can be cued in "sfx" like any other sound. Beds (bed_*) are long, quiet, loopable ambiences:
cue them with "dur", "fadeIn", "fadeOut". No bed goes below 150 Hz (the user dislikes low rumbles).

Kinds: snow_step ice_step ice_creak ice_ping ice_crack thump_snow paper_unfold pencil_scratch paper_tap latch
door_swing breath_out drip icicle_chime lantern_click mitten_rub spoon_tap shatter bamboo_snap wobble
scoop bite_soft sparkle_warm swoosh_dive fog_hiss gust whip iris_whoomp snow_plop
bed_room bed_morning bed_river bed_woods bed_cave bed_glow
wet_step bell_ring cable_hum rail_creak crust_crackle bread_tear mist_whoosh honey_pour lid_clink oven_crackle crumb_squeeze
bed_fogwind bed_street bed_bakery bed_dawn
knife_saw flour_pour glass_clink lid_screw bubble_pop dough_pat
"""
import json
import os
import subprocess
import sys
import wave
import zlib

import numpy as np

SR = 48000


class F:
    def __init__(self, seed):
        self.r = np.random.default_rng(seed)

    # ---------- building blocks
    def n(self, d):
        return self.r.standard_normal(int(d * SR))

    @staticmethod
    def band(x, lo, hi, soft=0.25):
        X = np.fft.rfft(x)
        f = np.fft.rfftfreq(len(x), 1 / SR)
        m = np.ones_like(f)
        if lo > 0:
            m *= 1 / (1 + (lo / np.maximum(f, 1)) ** (2 / soft))
        if hi:
            m *= 1 / (1 + (f / hi) ** (2 / soft))
        return np.fft.irfft(X * m, len(x))

    @staticmethod
    def env(L, a, r, hold=0.0):
        t = np.arange(L) / SR
        return np.where(t < a, t / max(a, 1e-4), np.exp(-np.maximum(t - a - hold, 0) / r))

    @staticmethod
    def t(d):
        return np.arange(int(d * SR)) / SR

    @staticmethod
    def put(out, x, at):
        i = int(at * SR)
        if i >= len(out):
            return out
        k = min(len(x), len(out) - i)
        out[i:i + k] += x[:k]
        return out

    def reverb(self, x, size=0.5, wet=0.25, bright=6000):
        L = int(size * SR)
        ir = self.band(self.r.standard_normal(L), 200, bright) * np.exp(-np.arange(L) / (size * SR / 5))
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        xx = np.concatenate([x, np.zeros(L)])
        y = np.convolve(x, ir)[:len(xx)]
        y = np.concatenate([y, np.zeros(len(xx) - len(y))])
        return xx * (1 - wet) + y * wet * 1.4

    def reson(self, x, freqs, q=40):
        """Bank of resonators (modal filter) excited by x."""
        X = np.fft.rfft(x)
        f = np.fft.rfftfreq(len(x), 1 / SR)
        H = np.zeros_like(f)
        for fr, g in freqs:
            bw = fr / q
            H += g / (1 + ((f - fr) / bw) ** 2)
        return np.fft.irfft(X * H, len(x))

    def grains(self, d, rate, lo, hi, decay=0.004, shape=None):
        """Many tiny clicks (crunch, crackle, sparkle)."""
        out = np.zeros(int(d * SR) + SR // 10)
        k = int(rate * d)
        times = np.sort(self.r.random(k) * d)
        for tt in times:
            g = self.band(self.n(0.012), lo * self.r.uniform(0.8, 1.2), hi) * self.env(int(0.012 * SR), 0.0004, decay)
            amp = self.r.uniform(0.2, 1.0) * (shape(tt / d) if shape else 1.0)
            self.put(out, g * amp, tt)
        return out

    def chirp(self, f0, f1, d, decay):
        t = self.t(d)
        f = f1 + (f0 - f1) * np.exp(-t / (d / 4))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * self.env(len(t), 0.001, decay)

    def partials(self, base, ratios, d, decays, amps=None):
        t = self.t(d)
        y = np.zeros(len(t))
        for i, rr in enumerate(ratios):
            a = 1.0 if amps is None else amps[i]
            y += a * np.sin(2 * np.pi * base * rr * t + self.r.uniform(0, 6)) * np.exp(-t / decays[i])
        return y * self.env(len(t), 0.0015, 10)

    # ---------- winter travel
    def snow_step(self, p):
        d = self.r.uniform(0.22, 0.32)
        crunch = self.grains(d, self.r.uniform(260, 380), 700, 5000, 0.004, lambda u: (1 - u) ** 1.3 * min(1, u * 12))
        thud = self.band(self.n(0.12), 110, 500) * self.env(int(0.12 * SR), 0.004, 0.04)
        out = np.zeros(len(crunch))
        self.put(out, crunch * 0.8, 0)
        self.put(out, thud * 2.4, 0.005)
        return self.reverb(out, 0.25, 0.08)

    def ice_creak(self, p):
        d = self.r.uniform(0.6, 0.9)
        t = self.t(d)
        rate = 30 + 60 * (0.5 + 0.5 * np.sin(2 * np.pi * self.r.uniform(1.2, 2.5) * t + 1.3)) * np.sin(np.pi * t / d)
        ph = np.cumsum(rate) / SR
        pulses = np.diff(np.floor(ph), prepend=0) > 0
        ex = pulses.astype(float) * self.r.uniform(0.5, 1.0, len(t)) + 0.05 * self.r.standard_normal(len(t))
        y = self.reson(ex, [(self.r.uniform(380, 460), 1.0), (self.r.uniform(860, 980), 0.7), (1700, 0.35)], q=12)
        y *= np.sin(np.pi * t / d) ** 0.7
        return self.reverb(self.band(y, 180, 5000), 0.8, 0.3)

    def ice_ping(self, p):
        out = np.zeros(int(1.6 * SR))
        for i in range(p.get('n', 2)):
            c = self.chirp(self.r.uniform(2600, 4200), self.r.uniform(380, 700), 0.5, self.r.uniform(0.12, 0.25))
            self.put(out, c * self.r.uniform(0.5, 1.0), i * self.r.uniform(0.08, 0.2))
        return self.reverb(out, 1.4, 0.45, 5000)

    def ice_crack(self, p):
        out = np.zeros(int(1.4 * SR))
        snap = self.band(self.n(0.02), 600, 9000) * self.env(int(0.02 * SR), 0.0003, 0.003)
        self.put(out, snap * 2.0, 0)
        self.put(out, self.grains(0.55, 260, 1800, 9000, 0.003, lambda u: (1 - u) ** 2), 0.01)
        for i in range(3):
            self.put(out, self.chirp(self.r.uniform(3000, 4500), self.r.uniform(400, 700), 0.45, 0.16) * 0.6, 0.02 + i * 0.13)
        return self.reverb(out, 1.2, 0.35, 6000)

    def thump_snow(self, p):
        out = np.zeros(int(0.6 * SR))
        self.put(out, self.band(self.n(0.25), 120, 700) * self.env(int(0.25 * SR), 0.004, 0.06) * 1.6, 0)
        self.put(out, self.grains(0.25, 300, 900, 6000, 0.003, lambda u: 1 - u), 0.005)
        return self.reverb(out, 0.3, 0.1)

    def ice_step(self, p):
        """A careful boot on hard ice: hollow knock + a faint singing ping under it."""
        out = np.zeros(int(1.0 * SR))
        k = self.reson(self.band(self.n(0.1), 0, 4000) * self.env(int(0.1 * SR), 0.0006, 0.008),
                       [(self.r.uniform(280, 340), 1.0), (self.r.uniform(650, 760), 0.6), (1400, 0.25)], q=18)
        self.put(out, k / (np.abs(k).max() + 1e-9), 0)
        self.put(out, self.grains(0.06, 300, 2000, 6000, 0.002) * 0.25, 0.002)
        self.put(out, self.chirp(self.r.uniform(1800, 2400), 500, 0.4, 0.12) * 0.12, 0.03)
        return self.reverb(out, 0.9, 0.25, 5000)

    def snow_plop(self, p):
        out = np.zeros(int(1.0 * SR))
        self.put(out, self.band(self.n(0.3), 150, 900) * self.env(int(0.3 * SR), 0.006, 0.08) * 1.5, 0)
        self.put(out, self.grains(0.4, 220, 1200, 7000, 0.004, lambda u: (1 - u) ** 1.5), 0.01)
        hiss = self.band(self.n(0.7), 2500, 9000) * self.env(int(0.7 * SR), 0.02, 0.25) * 0.25
        self.put(out, hiss, 0.05)
        return out

    def breath_out(self, p):
        d = 1.0
        t = self.t(d)
        x = self.band(self.n(d), 250, 3200)
        x = self.reson(x, [(700, 0.8), (1150, 1.0), (2400, 0.4)], q=4) + 0.3 * x
        e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6 * np.exp(-t * 0.8)
        return x * e

    def fog_hiss(self, p):
        d = p.get('d', 0.9)
        t = self.t(d)
        x = self.band(self.n(d), 500, 5000)
        return x * np.sin(np.pi * t / d) ** 1.5

    def gust(self, p):
        d = p.get('d', 0.9)
        t = self.t(d)
        x = self.band(self.n(d), 900, 7000)
        turb = 0.6 + 0.4 * self.band(self.r.standard_normal(len(t)), 0, 12, 0.6)
        turb /= np.abs(turb).max()
        out = x * np.sin(np.pi * t / d) ** 1.2 * (0.6 + 0.4 * turb)
        return out + self.grains(d, 160, 2500, 9000, 0.002, lambda u: np.sin(np.pi * u))[:len(out)] * 0.4

    def whip(self, p):
        d = 0.38
        t = self.t(d)
        x = self.n(d)
        lo = 400 + 3000 * t / d
        y = np.zeros_like(x)
        for i, (a, b) in enumerate([(0, 0.5), (0.5, 1.0)]):
            s, e = int(a * len(x)), int(b * len(x))
            y[s:e] = self.band(x[s:e], lo[s], lo[s] * 4)
        return y * np.sin(np.pi * t / d) ** 2

    def swoosh_dive(self, p):
        d = p.get('d', 0.8)
        t = self.t(d)
        x = self.n(d)
        segs = 8
        y = np.zeros_like(x)
        for i in range(segs):
            s, e = int(i * len(x) / segs), int((i + 1) * len(x) / segs)
            f = 300 * (12 ** (i / segs))
            y[s:e] = self.band(x[s:e], f, f * 3)
        flutter = 1 + 0.35 * np.sin(2 * np.pi * (18 + 30 * t / d) * t)
        sh = self.r.uniform(0, 1, 5)
        return y * np.sin(np.pi * t / d) ** 1.2 * flutter + self.partials(1800, [1, 1.5, 2.01], d, [0.3, 0.25, 0.2]) * 0.05 * np.sin(np.pi * t / d)

    def iris_whoomp(self, p):
        d = 0.7
        t = self.t(d)
        x = self.band(self.n(d), 160, 800) * np.sin(np.pi * np.clip(t / 0.5, 0, 1)) ** 2
        return self.reverb(x, 0.9, 0.4, 3000)

    # ---------- paper + small hand sounds
    def paper_unfold(self, p):
        d = p.get('d', 0.9)
        out = np.zeros(int(d * SR) + SR // 4)
        for i in range(p.get('n', 4)):
            at = self.r.uniform(0, d - 0.15)
            dd = self.r.uniform(0.06, 0.18)
            b = self.band(self.n(dd), 1500, 9000) * self.env(int(dd * SR), 0.003, dd / 3)
            self.put(out, b * self.r.uniform(0.4, 1.0), at)
            self.put(out, self.grains(dd, 400, 2000, 9000, 0.002) * 0.6, at)
        return out

    def pencil_scratch(self, p):
        out = np.zeros(int(0.6 * SR))
        for (a, d) in [(0.0, 0.08), (0.1, 0.22)]:
            t = self.t(d)
            x = self.band(self.n(d), 2200, 8000) * (0.6 + 0.4 * np.sin(2 * np.pi * 90 * t)) * np.sin(np.pi * t / d) ** 0.5
            self.put(out, x, a)
        return out

    def paper_tap(self, p):
        return self.band(self.n(0.05), 200, 1800) * self.env(int(0.05 * SR), 0.001, 0.012)

    def latch(self, p):
        out = np.zeros(int(0.5 * SR))
        for i, at in enumerate((0.0, 0.09)):
            c = self.partials(self.r.uniform(2000, 2600), [1, 1.71, 2.9], 0.15, [0.03, 0.02, 0.015]) * (1.0 if i else 0.7)
            self.put(out, c + self.band(self.n(0.15), 1000, 6000) * self.env(int(0.15 * SR), 0.0005, 0.005), at)
        return self.reverb(out, 0.4, 0.15)

    def door_swing(self, p):
        d = 0.8
        t = self.t(d)
        rate = 22 + 25 * np.sin(np.pi * t / d)
        pulses = np.diff(np.floor(np.cumsum(rate) / SR), prepend=0) > 0
        ex = pulses.astype(float) + 0.03 * self.r.standard_normal(len(t))
        y = self.reson(ex, [(620, 1.0), (1150, 0.6), (1900, 0.3)], q=14) * np.sin(np.pi * t / d) ** 0.8 * 0.6
        air = self.band(self.n(d), 600, 4000) * np.sin(np.pi * t / d) ** 2 * 0.35
        return self.reverb(y + air, 0.4, 0.12)

    def drip(self, p):
        c = self.chirp(self.r.uniform(700, 900), self.r.uniform(1800, 2600), 0.12, 0.03)
        return self.reverb(c, p.get('room', 0.6), p.get('wet', 0.35), 7000)

    def icicle_chime(self, p):
        out = np.zeros(int(2.4 * SR))
        n = p.get('n', 6)
        for i in range(n):
            base = self.r.uniform(1700, 2700)
            c = self.partials(base, [1, 2.76, 5.40, 8.93], 1.6, [0.7, 0.35, 0.18, 0.1], [1, 0.5, 0.25, 0.12])
            self.put(out, c * self.r.uniform(0.4, 1.0), i * self.r.uniform(0.05, 0.13))
        return self.reverb(out, 1.0, 0.3, 9000)

    def lantern_click(self, p):
        out = np.zeros(int(1.0 * SR))
        self.put(out, self.partials(3200, [1, 1.8], 0.08, [0.012, 0.01]) + self.band(self.n(0.08), 1500, 8000) * self.env(int(0.08 * SR), 0.0004, 0.004), 0)
        whf = self.band(self.n(0.5), 300, 2500) * np.sin(np.pi * np.clip(self.t(0.5) / 0.5, 0, 1)) ** 2 * 0.5
        self.put(out, whf, 0.05)
        return out

    def mitten_rub(self, p):
        d = p.get('d', 1.8)
        t = self.t(d)
        x = self.band(self.n(d), 1200, 7500)
        stroke = np.abs(np.sin(np.pi * p.get('rate', 3.2) * t)) ** 1.5
        frost = self.grains(d, 260, 3000, 9000, 0.002, lambda u: 1.0 - 0.5 * u)[:len(t)] * 0.35
        return (x * 0.6 + frost) * stroke * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.15)

    def spoon_tap(self, p):
        c = self.partials(self.r.uniform(2900, 3300), [1, 1.72, 2.51, 3.6], 0.6, [0.08, 0.05, 0.03, 0.02], [1, 0.6, 0.4, 0.2])
        k = self.band(self.n(0.02), 1500, 9000) * self.env(int(0.02 * SR), 0.0002, 0.002)
        out = c * 0.7
        out[:len(k)] += k
        return self.reverb(out, 0.9, 0.3, 8000)

    def shatter(self, p):
        out = np.zeros(int(2.0 * SR))
        self.put(out, self.ice_crack({}) * 0.7, 0)
        for i in range(40):
            at = self.r.exponential(0.18)
            if at > 1.2:
                continue
            g = self.partials(self.r.uniform(3000, 8000), [1, 1.6], 0.12, [0.03, 0.02]) * self.r.uniform(0.15, 0.6)
            self.put(out, g, at)
        return self.reverb(out, 1.0, 0.3, 9000)

    def bamboo_snap(self, p):
        out = np.zeros(int(1.0 * SR))
        snap = self.band(self.n(0.03), 700, 8000) * self.env(int(0.03 * SR), 0.0003, 0.005)
        self.put(out, snap * 1.6, 0)
        self.put(out, self.grains(0.14, 300, 1200, 6000, 0.003, lambda u: 1 - u), 0.004)
        tok = self.reson(self.band(self.n(0.3), 0, 3000) * self.env(int(0.3 * SR), 0.0005, 0.006), [(330, 1.0), (680, 0.6), (1050, 0.3)], q=25)
        self.put(out, tok / (np.abs(tok).max() + 1e-9) * 0.9, 0.012)
        return self.reverb(out, 0.7, 0.2)

    def wobble(self, p):
        d = p.get('d', 1.0)
        t = self.t(d)
        vib = np.sin(2 * np.pi * 9 * t)
        dec = np.exp(-t * 2.8)
        f = 230 + 40 * vib * dec
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.abs(vib)) * dec
        sq = self.band(self.n(d), 300, 1600) * np.abs(vib) * dec * 0.35
        return (tone * 0.8 + sq) * np.minimum(1, t / 0.01)

    def scoop(self, p):
        d = 0.42
        t = self.t(d)
        x = self.n(d)
        y = np.zeros_like(x)
        for i in range(6):
            s, e = int(i * len(x) / 6), int((i + 1) * len(x) / 6)
            f = 350 * (4 ** (i / 6))
            y[s:e] = self.reson(x[s:e], [(f, 1.0)], q=6)
        y = y * np.sin(np.pi * t / d) ** 0.8
        suck = self.chirp(300, 900, 0.1, 0.03) * 0.3
        self.put(y, suck, d - 0.1)
        return y

    def bite_soft(self, p):
        out = np.zeros(int(0.7 * SR))
        self.put(out, self.band(self.n(0.09), 150, 1800) * self.env(int(0.09 * SR), 0.002, 0.025) * 1.3, 0)
        self.put(out, self.reson(self.band(self.n(0.15), 200, 2500), [(500, 1), (900, 0.5)], q=5) * self.env(int(0.15 * SR), 0.01, 0.05) * 0.5, 0.12)
        return out

    def sparkle_warm(self, p):
        out = np.zeros(int(2.6 * SR))
        notes = [1046.5, 1174.7, 1318.5, 1568.0, 1760.0, 2093.0]
        for i in range(p.get('n', 7)):
            f = notes[self.r.integers(len(notes))]
            c = self.partials(f, [1, 2.0, 3.0], 1.2, [0.5, 0.3, 0.15], [1, 0.25, 0.08])
            c *= np.minimum(1, self.t(1.2) / 0.03)
            self.put(out, c * self.r.uniform(0.3, 0.8), i * self.r.uniform(0.1, 0.22))
        return self.reverb(out, 1.2, 0.35, 9000)

    # ---------- beds (long, quiet, no low rumble)
    def _air(self, d, lo=400, hi=4000):
        x = self.band(self.n(d), lo, hi)
        slow = self.band(self.r.standard_normal(len(x)), 0, 0.5, 0.6)
        slow = 0.6 + 0.4 * slow / (np.abs(slow).max() + 1e-9)
        return x * slow

    def bed_room(self, p):
        d = p.get('d', 4.0)
        out = self._air(d, 250, 1800) * 0.25
        for k in range(int(d)):  # a slow wooden clock
            self.put(out, self.band(self.n(0.03), 800, 4000) * self.env(int(0.03 * SR), 0.0005, 0.004) * (0.5 if k % 2 else 0.35), k + 0.3)
        return out

    def bed_morning(self, p):
        d = p.get('d', 7.0)
        out = self._air(d, 700, 5000) * 0.5
        for i in range(int(d / 1.5)):
            self.put(out, self.partials(self.r.uniform(1800, 2600), [1, 2.76], 1.5, [0.6, 0.3]) * 0.08, self.r.uniform(0, d - 1))
        return out

    def bed_river(self, p):
        d = p.get('d', 7.0)
        out = self._air(d, 800, 5000) * 0.45
        for i in range(int(d / 2.2)):
            self.put(out, self.chirp(self.r.uniform(1400, 2200), self.r.uniform(300, 500), 0.9, 0.35) * 0.12, self.r.uniform(0, d - 1))
        return self.reverb(out, 1.2, 0.3, 5000)[:len(out)]

    def bed_woods(self, p):
        d = p.get('d', 7.0)
        out = self._air(d, 600, 3500) * 0.3
        out += self.grains(d, 30, 3000, 9000, 0.002)[:len(out)] * 0.15  # snow sifting off branches
        for i in range(int(d / 2.5)):  # far little birds
            at = self.r.uniform(0, d - 0.6)
            for j in range(self.r.integers(2, 4)):
                c = self.chirp(self.r.uniform(3200, 4200), self.r.uniform(4500, 5600), 0.08, 0.025) * 0.06
                self.put(out, c, at + j * 0.11)
        return out

    def bed_cave(self, p):
        d = p.get('d', 6.0)
        out = self._air(d, 180, 1400) * 0.25
        for i in range(int(d * 1.2)):
            self.put(out, self.chirp(self.r.uniform(700, 1000), self.r.uniform(1600, 2600), 0.1, 0.02) * 0.35, self.r.uniform(0, d - 0.3))
        return self.reverb(out, 1.6, 0.45, 5000)[:len(out)]

    def bed_glow(self, p):
        d = p.get('d', 6.0)
        t = self.t(d)
        y = np.zeros(len(t))
        for f, a in [(196.0, 0.5), (293.7, 0.4), (392.0, 0.35), (587.3, 0.15)]:
            y += a * np.sin(2 * np.pi * f * t + self.r.uniform(0, 6)) * (0.8 + 0.2 * np.sin(2 * np.pi * self.r.uniform(0.1, 0.3) * t))
        return y * np.minimum(1, t / 1.0) * 0.4 + self._air(d, 400, 2500) * 0.1

    # ---------- bakery / coastal town (added 24 Nov 2026 for fog-sourdough-boule)
    def wet_step(self, p):
        d = self.r.uniform(0.2, 0.3)
        slap = self.band(self.n(0.1), 300, 2600) * self.env(int(0.1 * SR), 0.003, 0.03)
        grit = self.grains(d, self.r.uniform(90, 160), 1200, 6000, 0.003, lambda u: (1 - u) ** 1.6)
        out = np.zeros(len(grit))
        self.put(out, grit * 0.5, 0.01)
        self.put(out, slap * 1.8, 0.0)
        return self.reverb(out, 0.3, 0.12)

    def bell_ring(self, p):
        out = np.zeros(int(2.4 * SR))
        base = self.r.uniform(1050, 1250)
        for i in range(p.get('n', 2)):
            y = self.partials(base, [1, 2.4, 3.9, 5.6], 2.0, [0.9, 0.5, 0.3, 0.15], [1, 0.5, 0.3, 0.15])
            self.put(out, y * 0.7, i * self.r.uniform(0.32, 0.45))
        return self.reverb(out, 1.2, 0.3, 7000)

    def cable_hum(self, p):
        d = p.get('d', 1.2)
        t = self.t(d)
        ex = self.n(d)
        y = self.reson(ex, [(self.r.uniform(520, 640), 1.0), (self.r.uniform(1300, 1500), 0.5)], q=25)
        return y * np.sin(np.pi * t / d) ** 0.8 * 0.5

    def rail_creak(self, p):
        return self.ice_creak(p) * 0.6

    def crust_crackle(self, p):
        d = p.get('d', 1.0)
        shape = lambda u: (1 - u) ** 0.9 * min(1, u * 14)
        c = self.grains(d, p.get('rate', 140), 1500, 7500, 0.0025, shape)
        tick = self.reson(self.band(self.n(d), 800, 6000) * self.env(int(d * SR), 0.002, d / 3), [(2400, 1.0), (4100, 0.6)], q=8)
        out = c[:int(d * SR)] + 0.15 * tick
        return self.reverb(out, 0.3, 0.1)

    def bread_tear(self, p):
        d = p.get('d', 0.9)
        out = np.zeros(int(d * SR) + SR // 5)
        self.put(out, self.crust_crackle({'d': d * 0.8, 'rate': 190}) * 0.9, 0)
        rip = self.band(self.n(d), 500, 4200) * np.sin(np.pi * self.t(d) / d) ** 2
        self.put(out, rip * 0.25, 0.05)
        return self.reverb(out, 0.35, 0.12)

    def mist_whoosh(self, p):
        d = p.get('d', 1.4)
        t = self.t(d)
        y = self.band(self.n(d), 1500, 7000) * np.sin(np.pi * t / d) ** 1.4
        return y * 0.5

    def honey_pour(self, p):
        d = p.get('d', 2.0)
        t = self.t(d)
        y = np.zeros(len(t))
        rate = 14 + 6 * np.sin(2 * np.pi * 0.7 * t)
        ph = np.cumsum(rate) / SR
        pulses = (np.diff(np.floor(ph), prepend=0) > 0).astype(float)
        y = self.reson(pulses * self.r.uniform(0.4, 1.0, len(t)), [(self.r.uniform(520, 700), 1.0), (self.r.uniform(1100, 1500), 0.5)], q=14)
        y *= self.env(len(t), 0.25, d / 2.5, hold=d * 0.4)
        return self.band(y, 220, 3800) * 0.5

    def lid_clink(self, p):
        out = np.zeros(int(1.2 * SR))
        y = self.partials(self.r.uniform(900, 1100), [1, 1.7, 2.9, 4.1], 0.7, [0.18, 0.1, 0.06, 0.04], [1, 0.6, 0.3, 0.2])
        self.put(out, y * 0.8, 0)
        self.put(out, self.band(self.n(0.05), 1500, 6000) * self.env(int(0.05 * SR), 0.001, 0.012) * 0.4, 0)
        return self.reverb(out, 0.5, 0.2)

    def oven_crackle(self, p):
        d = p.get('d', 2.0)
        return self.grains(d, 22, 1800, 7000, 0.006, lambda u: 0.6 + 0.4 * np.sin(u * 20)) * 0.5

    def crumb_squeeze(self, p):
        d = 0.5
        y = self.grains(d, 90, 900, 3800, 0.005, lambda u: np.sin(np.pi * u))
        return self.reverb(y * 0.7, 0.2, 0.08)

    def knife_saw(self, p):
        """Bread knife sawing through crust: n back-and-forth strokes, each a rough scrape with a crackle."""
        d = p.get('d', 2.0)
        n = int(p.get('n', 6))
        out = np.zeros(int(d * SR) + SR // 4)
        for i in range(n):
            sd = d / n * 0.92
            t = self.t(sd)
            sc = self.band(self.n(sd), 700, 5200) * np.sin(np.pi * t / sd) ** 0.7
            sc *= 0.7 + 0.3 * np.sin(2 * np.pi * 40 * t)
            self.put(out, sc * 0.45, i * d / n)
            self.put(out, self.grains(sd, 120, 1800, 6500, 0.002, lambda u: np.sin(np.pi * u)) * 0.5, i * d / n)
        return self.reverb(out, 0.25, 0.08)

    def flour_pour(self, p):
        d = p.get('d', 1.8)
        t = self.t(d)
        y = self.band(self.n(d), 2500, 9000) * self.env(len(t), 0.15, d / 3, hold=d * 0.5)
        y *= 0.75 + 0.25 * np.sin(2 * np.pi * 9 * t + 1.3)
        return y * 0.34

    def glass_clink(self, p):
        out = np.zeros(int(1.0 * SR))
        y = self.partials(self.r.uniform(2300, 2800), [1, 2.3, 3.9], 0.5, [0.1, 0.06, 0.04], [1, 0.45, 0.25])
        self.put(out, y * 0.5, 0)
        return self.reverb(out, 0.3, 0.12)

    def lid_screw(self, p):
        d = p.get('d', 0.6)
        out = np.zeros(int(d * SR) + SR // 8)
        for i in range(5):
            self.put(out, self.band(self.n(0.04), 1200, 5000) * self.env(int(0.04 * SR), 0.002, 0.012) * 0.5, i * d / 5)
        sq = self.chirp(1800, 2600, d * 0.7, 3.0) * 0.12
        self.put(out, sq, 0.02)
        return out

    def bubble_pop(self, p):
        d = 0.12
        y = self.chirp(self.r.uniform(500, 800), self.r.uniform(1200, 1800), d, 22) * 0.6
        return self.reverb(y, 0.2, 0.08)

    def dough_pat(self, p):
        d = 0.35
        t = self.t(d)
        y = np.sin(2 * np.pi * (110 - 50 * t / d) * t) * np.exp(-t * 16) * 0.8
        y += self.band(self.n(d), 300, 1800) * np.exp(-t * 30) * 0.3
        return self.reverb(y, 0.2, 0.06)

    def bed_fogwind(self, p):
        d = p.get('d', 6.0)
        t = self.t(d)
        y = self._air(d, 450, 2200) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * t + 1.0))
        return y * 0.4

    def bed_street(self, p):
        d = p.get('d', 6.0)
        out = self._air(d, 500, 2600) * 0.2
        for _ in range(int(d * 0.5)):
            self.put(out, self.partials(self.r.uniform(1400, 1900), [1, 2.7], 0.5, [0.3, 0.15]) * 0.12, self.r.uniform(0, d - 0.6))
        return self.reverb(out, 1.0, 0.3, 5000)[:len(out)]

    def bed_bakery(self, p):
        d = p.get('d', 6.0)
        out = self._air(d, 350, 1800) * 0.12
        self.put(out, np.zeros(1), 0)
        return out + self.oven_crackle({'d': d})[:len(out)] * 0.35

    def bed_dawn(self, p):
        d = p.get('d', 6.0)
        t = self.t(d)
        y = self._air(d, 900, 3800) * 0.12
        for _ in range(int(d * 0.8)):
            self.put(y, self.chirp(self.r.uniform(2200, 3200), self.r.uniform(3200, 4200), 0.12, 0.03) * 0.2, self.r.uniform(0, d - 0.3))
        return y


def write_wav(path, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def main():
    P = os.path.abspath(sys.argv[1])
    proj = json.load(open(os.path.join(P, 'project-files', 'project.json')))
    out = os.path.join(P, 'project-files', 'sfx')
    os.makedirs(out, exist_ok=True)
    made = []
    for name, spec in proj.get('foley', {}).items():
        seed = zlib.crc32((proj.get('slug', '') + '/' + name).encode())
        f = F(seed)
        kind = spec['kind']
        if not hasattr(f, kind):
            sys.exit(f'!! unknown foley kind {kind} for {name}')
        x = getattr(f, kind)(spec)
        x = F.band(x, spec.get('hp', 150 if kind.startswith('bed_') else 60), None)
        x[:96] *= np.linspace(0, 1, 96)
        x[-480:] *= np.linspace(1, 0, 480)
        write_wav(os.path.join(out, name + '.wav'), x)
        made.append(name)
    print(f'foley: {len(made)} new sounds -> {out}')
    if '--audition' in sys.argv:
        dst = sys.argv[sys.argv.index('--audition') + 1]
        lst = os.path.join(out, '_list.txt')
        open(lst, 'w').write(''.join(f"file '{os.path.join(out, m)}.wav'\n" for m in made))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-b:a', '160k', dst], check=True)
        os.remove(lst)


if __name__ == '__main__':
    main()
