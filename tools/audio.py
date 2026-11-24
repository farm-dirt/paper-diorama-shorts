#!/usr/bin/env python3
"""Synthesize SFX + music bed and mix them under the voice-over.

usage: python3 audio.py PROJECT_DIR
reads  PROJECT_DIR/project-files/project.json  (sfx cues, music settings)
       PROJECT_DIR/project-files/timing.json
       PROJECT_DIR/voice-over/<voice file named in project.json>
writes PROJECT_DIR/audio/mix.wav  (final, -14 LUFS, true peak <= -1 dBFS)
       PROJECT_DIR/audio/mix.mp3  (for the browser preview)

LEVELS (user preference: background must never fight the voice):
  music  = 8 % of the voice level during speech (-22 dB), rises to 14 % in long pauses
  sfx    = peaks at 35 % of the voice peak
  room   = 2 % of the voice level everywhere (quiet air), so the mix is never digital silence
Override in project.json: "mix": {"music": 0.08, "musicPause": 0.14, "sfx": 0.35, "roomTone": 0.02}
Recorded music: "music": {"track": "greek_folk", "start": 0, "stops": [[a, b]]} (files in assets/music/)
"""
import json, os, subprocess, sys, re
import numpy as np

SR = 48000
BANNED = {'wind', 'dark_click'}  # user rule, Nov 2026: low rumbles that drone under scenes; use wind_howl
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(SR * d)) / SR


def env_ad(n, a=0.005, d=None):
    e = np.ones(n)
    na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    if d:
        e *= np.exp(-np.arange(n) / (d * SR))
    return e


def sweep(f0, f1, d, wave='sine'):
    f = np.geomspace(f0, f1, int(SR * d)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) if wave == 'sine' else np.sign(np.sin(ph)) * 0.5


def noise(d):
    return rng.standard_normal(int(SR * d))


def lp(x, a):  # one-pole low-pass, a in (0,1): smaller = darker
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y


# ---------------- SFX library (all original, synthesized) ----------------
def sfx_pop():      return sweep(900, 300, 0.07) * env_ad(int(0.07 * SR), 0.002, 0.02)
def sfx_boing():
    d = 0.55; t = t_(d); f = 220 + 140 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(len(t), 0.004, 0.25)
def sfx_whoosh():
    d = 0.4; n = noise(d); t = t_(d); a = 0.02 + 0.5 * np.sin(np.pi * t / d) ** 2
    return lp(n, 0.08) * np.sin(np.pi * t / d) ** 2 * 3 * a
def sfx_thud():     return (sweep(160, 45, 0.25) + 0.3 * lp(noise(0.25), 0.05)) * env_ad(int(0.25 * SR), 0.002, 0.07)
def sfx_bonk():     return (sweep(700, 500, 0.18) * 0.6 + sweep(1400, 1000, 0.18) * 0.3) * env_ad(int(0.18 * SR), 0.001, 0.05)
def sfx_ding():
    t = t_(1.0); return (np.sin(2 * np.pi * 1568 * t) + 0.4 * np.sin(2 * np.pi * 3136 * t) + 0.2 * np.sin(2 * np.pi * 4700 * t)) * env_ad(len(t), 0.002, 0.3) * 0.6
def sfx_sparkle():
    out = np.zeros(int(0.7 * SR))
    for k, f in enumerate([2093, 2637, 3136, 4186, 3520]):
        s = int(k * 0.08 * SR); t = t_(0.3); tone = np.sin(2 * np.pi * f * t) * env_ad(len(t), 0.002, 0.08)
        out[s:s + len(tone)] += tone[:len(out) - s] * 0.5
    return out
def sfx_slide_up():   return sweep(300, 1500, 0.45) * env_ad(int(0.45 * SR), 0.01) * 0.7
def sfx_slide_down(): return sweep(1500, 250, 0.5) * env_ad(int(0.5 * SR), 0.01) * 0.7
def sfx_tick():       return lp(noise(0.03), 0.6) * env_ad(int(0.03 * SR), 0.0005, 0.006)
def sfx_gulp():       return sweep(500, 180, 0.12) * env_ad(int(0.12 * SR), 0.003, 0.05) + np.concatenate([np.zeros(int(.13*SR)), sweep(420, 160, 0.12) * env_ad(int(0.12 * SR), 0.003, 0.05)])[:int(0.12*SR)]
def sfx_drumroll():
    d = 1.2; out = np.zeros(int(d * SR))
    for k in range(int(d * 22)):
        s = int(k / 22 * SR); h = lp(noise(0.05), 0.3) * env_ad(int(0.05 * SR), 0.001, 0.015) * (0.4 + 0.6 * k / (d * 22))
        out[s:s + len(h)] += h[:len(out) - s]
    return out
def sfx_tada():
    out = np.zeros(int(1.2 * SR))
    for s0, fs in [(0, [523, 659, 784]), (0.16, [523, 659, 784, 1047])]:
        t = t_(1.0 if s0 else 0.15); ch = sum(np.sign(np.sin(2 * np.pi * f * t)) * 0.12 + np.sin(2 * np.pi * f * t) * 0.2 for f in fs)
        ch *= env_ad(len(t), 0.005, 0.5 if s0 else 0.08); s = int(s0 * SR); out[s:s + len(ch)] += ch[:len(out) - s]
    return out
def sfx_wahwah():
    out = np.zeros(int(2.0 * SR))
    for k, f in enumerate([392, 370, 349, 330]):
        d = 0.9 if k == 3 else 0.38; t = t_(d); vib = 1 + (0.03 * np.sin(2 * np.pi * 6 * t) if k == 3 else 0)
        tone = lp(np.sign(np.sin(2 * np.pi * np.cumsum(f * vib) / SR)), 0.15) * env_ad(len(t), 0.02, 0.6)
        s = int(k * 0.4 * SR); out[s:s + len(tone)] += tone[:len(out) - s] * 0.6
    return out
def sfx_footstep():  return lp(noise(0.06), 0.15) * env_ad(int(0.06 * SR), 0.001, 0.015) * 1.5
def sfx_record_scratch():
    d = 0.35; t = t_(d); f = 600 * np.abs(np.sin(2 * np.pi * 5 * t)) + 100
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + lp(noise(d), 0.3) * 0.5) * env_ad(len(t), 0.002, 0.15)

SFX = {k[4:]: v for k, v in globals().items() if k.startswith('sfx_')}

# ---------------- Recorded SFX (user's own library) ----------------
# Any WAV/MP3 in <engine>/assets/sfx/ is usable by its file name (e.g. paper_rip.wav -> "paper_rip").
# A recorded sound with the same name as a synth one replaces it; the synth stays as "<name>_synth".
SFX_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'sfx')


def load_audio(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


RECORDED = set()
if os.path.isdir(SFX_DIR):
    for fn in sorted(os.listdir(SFX_DIR)):
        stem, ext = os.path.splitext(fn)
        if ext.lower() not in ('.wav', '.mp3', '.flac', '.ogg'):
            continue
        if stem in SFX and stem not in RECORDED:
            SFX[stem + '_synth'] = SFX[stem]
        SFX[stem] = (lambda p=os.path.join(SFX_DIR, fn): load_audio(p))
        RECORDED.add(stem)


def shape_cue(s, cue):
    """Apply optional cue options: dur (cut length, s), fadeIn / fadeOut (s)."""
    if cue.get('dur'):
        s = s[:int(cue['dur'] * SR)]
    s = s.copy()
    for key, rev in (('fadeIn', False), ('fadeOut', True)):
        n = min(len(s), int(cue.get(key, 0) * SR))
        if n > 1:
            ramp = np.linspace(0, 1, n)
            if rev: s[-n:] *= ramp[::-1]
            else: s[:n] *= ramp
    if not cue.get('fadeOut') and cue.get('dur'):  # avoid a click on hard cuts
        n = min(len(s), int(0.02 * SR)); s[-n:] *= np.linspace(1, 0, n)
    return s


# ---------------- music bed: light pizzicato/marimba loop ----------------
def music(dur, bpm=112, key=0, stops=()):
    beat = 60 / bpm; n = int(dur * SR) + SR; out = np.zeros(n)
    prog = [[0, 4, 7], [9, 12, 16], [5, 9, 12], [7, 11, 14]]  # I vi IV V
    base = 261.63 * 2 ** (key / 12)

    def note(f, d, amp, kind):
        t = t_(d)
        if kind == 'mar':
            w = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)
            return w * env_ad(len(t), 0.002, 0.18) * amp
        w = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
        return w * env_ad(len(t), 0.004, 0.25) * amp
    step, k = beat / 2, 0
    while k * step < dur + 1:
        bar = int(k // 8) % 4; ch = prog[bar]; s = int(k * step * SR)
        if k % 8 == 0 or k % 8 == 4:  # bass on beats 1 and 3
            b = note(base / 2 * 2 ** (ch[0] / 12), beat * 1.6, 0.55, 'bass'); out[s:s + len(b)] += b[:n - s]
        pat = [0, 1, 2, 1, 0, 2, 1, 2][k % 8]
        m = note(base * 2 * 2 ** (ch[pat] / 12), step * 1.8, 0.28 if k % 2 == 0 else 0.18, 'mar'); out[s:s + len(m)] += m[:n - s]
        k += 1
    out = out[:int(dur * SR)]
    return apply_stops(out, stops)  # musical "freeze" for gags/tension: duck, never zero


MUSIC_DIR = os.path.join(os.path.dirname(SFX_DIR), 'music')


def music_tracks():
    if not os.path.isdir(MUSIC_DIR): return []
    return sorted(os.path.splitext(f)[0] for f in os.listdir(MUSIC_DIR)
                  if os.path.splitext(f)[1].lower() in ('.wav', '.mp3', '.flac', '.ogg'))


def music_track(name, dur, start=0.0, stops=()):
    """Recorded music bed from assets/music/<name>: starts at `start` s, loops (1 s crossfade) to fill
    `dur`, fades in 1 s, applies the same stops as the synth bed (duck to STOP_FLOOR, never silence)."""
    path = next(os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR) if os.path.splitext(f)[0] == name)
    src = load_audio(path)[int(start * SR):]
    n = int(dur * SR); out = src.copy(); xf = SR
    while len(out) < n:
        a, b = out[-xf:], src[:xf]; r = np.linspace(0, 1, xf)
        out = np.concatenate([out[:-xf], a * (1 - r) + b * r, src[xf:]])
    out = out[:n]
    fi = min(SR, n); out[:fi] *= np.linspace(0, 1, fi)
    return apply_stops(out, stops)


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


STOP_FLOOR = 0.12   # music "stops" duck to 12 % (about -18 dB), never to zero: zero = dead air on phones
STOP_MAX = 0.4      # a silence beat longer than this feels like the video broke (Kumakatok, Nov 2026)


def apply_stops(out, stops):
    """Tension beat: quick 60 ms duck to STOP_FLOOR, held at most STOP_MAX s, 0.15 s fade back."""
    for a, b in stops:
        if b - a > STOP_MAX:
            print(f'!! music stop {a:.2f}-{b:.2f} is {b - a:.2f} s; capped to {STOP_MAX} s (longer feels like dead air)')
            b = a + STOP_MAX
        i0, i1 = int(a * SR), min(len(out), int(b * SR))
        if i0 >= i1: continue
        g = np.ones(len(out)); fd = min(int(0.06 * SR), i0); fu = min(int(0.15 * SR), len(out) - i1)
        g[i0 - fd:i0] = np.linspace(1, STOP_FLOOR, fd) if fd else g[i0 - fd:i0]
        g[i0:i1] = STOP_FLOOR
        if fu > 0: g[i1:i1 + fu] = np.linspace(STOP_FLOOR, 1, fu)
        out *= g
    return out


def room_tone(n, level):
    """Very quiet low-passed noise under the whole mix, so no moment is ever digital silence."""
    w = rng.standard_normal(n + SR)
    k = int(0.004 * SR); w = np.convolve(w, np.ones(k) / k, mode='same')[:n]
    return w / rms(w) * level


def load_project_sfx(P):
    """This short's own sounds (made by foley.py) win over the shared library."""
    d = os.path.join(P, 'project-files', 'sfx')
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            stem, ext = os.path.splitext(fn)
            if ext.lower() in ('.wav', '.mp3', '.flac', '.ogg'):
                SFX[stem] = (lambda p=os.path.join(d, fn): load_audio(p))


def main():
    P = sys.argv[1]
    proj = json.load(open(os.path.join(P, 'project-files', 'project.json')))
    tim = json.load(open(os.path.join(P, 'project-files', 'timing.json')))
    load_project_sfx(P)
    if not proj.get('voice'):
        return main_sound_only(P, proj, tim)
    mixcfg = {'music': 0.08, 'musicPause': 0.14, 'sfx': 0.35}; mixcfg.update(proj.get('mix', {}))
    vpath = os.path.join(P, 'voice-over', proj['voice'])
    # voice compression (default on, mix.voiceComp false to skip): evens out quiet syllables so the
    # narrator stays clear on phone speakers and over food/ASMR sounds (user note, 23 Nov 2026)
    # "narrator polish" (default on; mix.voicePolish false to skip): warmth (180 Hz up), less mud (380 Hz
    # down), clearer words (3.2 kHz up), softer S sounds, even level, and a tiny room so the AI voice
    # sounds like a studio narrator instead of dry and flat (user note, 23 Nov 2026)
    polish = ('highpass=f=75,equalizer=f=180:t=q:w=0.9:g=2.5,equalizer=f=380:t=q:w=1.2:g=-2.5,'
              'equalizer=f=3200:t=q:w=1.0:g=2,deesser=i=0.35,'
              'acompressor=threshold=-24dB:ratio=3:attack=5:release=120:makeup=5dB:knee=4,'
              'aecho=0.85:0.6:18|31:0.10|0.06')
    comp = 'highpass=f=70,acompressor=threshold=-24dB:ratio=3.5:attack=4:release=90:makeup=6dB:knee=4'
    chain = polish if mixcfg.get('voicePolish', True) else (comp if mixcfg.get('voiceComp', True) else '')
    vaf = ['-af', 'aresample=48000,' + chain] if chain else []
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', vpath] + vaf + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    voice = np.frombuffer(raw, np.float32).astype(np.float64)
    vdur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vpath],
                                capture_output=True, text=True).stdout.strip() or 0)
    if vdur:  # the polish's room tail must not make the audio longer than the voice-over (video length)
        voice = voice[:int(round(vdur * SR))]
    dur = len(voice) / SR
    # voice level = RMS of speaking parts only
    sp = np.zeros(len(voice), bool)
    for a, b in tim['speech']: sp[int(a * SR):int(b * SR)] = True
    vr = rms(voice[sp]) if sp.any() else rms(voice)
    vpk = float(np.abs(voice).max())

    bed = np.zeros(len(voice))
    mcfg = proj.get('music', {'on': True})
    if mcfg.get('on', True):
        if mcfg.get('track'):
            if mcfg['track'] not in music_tracks():
                sys.exit('!! unknown music track %s -> available: %s' % (mcfg['track'], ', '.join(music_tracks())))
            m = music_track(mcfg['track'], dur, mcfg.get('start', 0.0), mcfg.get('stops', []))[:len(voice)]
        else:
            m = music(dur, mcfg.get('bpm', 112), mcfg.get('key', 0), mcfg.get('stops', []))[:len(voice)]
        if len(m) < len(voice): m = np.concatenate([m, np.zeros(len(voice) - len(m))])
        m = m / rms(m) * vr
        # gain curve: music% during speech, musicPause% in pauses >= 0.6 s, smoothed 150 ms
        g = np.full(len(voice), mixcfg['music'])
        for a, b in tim['pauses']:
            if b - a >= 0.6: g[int(a * SR):int(b * SR)] = mixcfg['musicPause']
        k = int(0.15 * SR); g = np.convolve(g, np.ones(k) / k, mode='same')
        fade = int(0.4 * SR); m[-fade:] *= np.linspace(1, 0, fade)
        bed += m * g
    fx = np.zeros(len(voice))
    bad = [c['name'] for c in proj.get('sfx', []) if c['name'] in BANNED]
    if bad:
        sys.exit('!! banned sound(s) in project.json (user rule): %s -> remove them or pick another' % ', '.join(sorted(set(bad))))
    unknown = [c['name'] for c in proj.get('sfx', []) if c['name'] not in SFX]
    if unknown:
        sys.exit('!! unknown sfx: %s -> available: %s' % (', '.join(sorted(set(unknown))), ', '.join(sorted(SFX))))
    for cue in proj.get('sfx', []):
        name = cue['name']
        s = shape_cue(SFX[name](), cue); s = s / (np.abs(s).max() + 1e-9) * vpk * mixcfg['sfx'] * cue.get('gain', 1.0)
        i = int(cue['t'] * SR); fx[i:i + len(s)] += s[:max(0, len(fx) - i)]
    # sound effects step back while the narrator talks (mix.sfxUnderVoice, default 0.6)
    duck = np.where(sp, mixcfg.get('sfxUnderVoice', 0.6), 1.0)
    k = int(0.08 * SR); duck = np.convolve(duck, np.ones(k) / k, mode='same')
    fx *= duck
    # room tone ~ -34 dB under the voice: inaudible under speech, but pauses never go to dead air
    mix = voice + bed + fx + room_tone(len(voice), vr * mixcfg.get('roomTone', 0.02))
    os.makedirs(os.path.join(P, 'audio'), exist_ok=True)
    tmp = os.path.join(P, 'audio', 'mix_raw.wav')
    pcm = np.clip(mix / max(1.0, np.abs(mix).max()), -1, 1)
    import wave
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((pcm * 32767).astype(np.int16).tobytes())
    # loudness: the TALKING parts are set to -14 LUFS (so loud sound-only moments can't pull the
    # voice down), then a true-peak limiter catches the peaks
    tmp2 = os.path.join(P, 'audio', 'mix_speech.wav')
    with wave.open(tmp2, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((pcm[sp] * 32767).astype(np.int16).tobytes())
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp2 if sp.any() else tmp, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    os.remove(tmp2)
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])
    gain = -13.0 - I  # talking parts a touch above -14 so the whole video lands at about -14 LUFS
    out = os.path.join(P, 'audio', 'mix.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'volume={gain:.2f}dB,alimiter=limit=0.89:attack=3:release=50:level=disabled',
                    '-ar', '48000', '-ac', '2', out], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-b:a', '160k', os.path.join(P, 'audio', 'mix.mp3')], check=True)
    os.remove(tmp)
    print(f'mix ok  dur={dur:.2f}s  measured {I:.1f} LUFS -> gain {gain:+.1f} dB  sfx={len(proj.get("sfx", []))}')


def main_sound_only(P, proj, tim):
    """No narrator (pure ASMR shorts): only the cued sounds, mixed and set to -14 LUFS.
    Cue gains are relative: each cue is peak-normalised, then x gain. Beds: gain 0.1-0.3."""
    dur = tim.get('dur') or proj['scenes'][-1]['end']
    n = int(round(dur * SR))
    fx = np.zeros(n)
    bad = [c['name'] for c in proj.get('sfx', []) if c['name'] in BANNED]
    if bad:
        sys.exit('!! banned sound(s) in project.json (user rule): %s' % ', '.join(sorted(set(bad))))
    unknown = sorted({c['name'] for c in proj.get('sfx', []) if c['name'] not in SFX})
    if unknown:
        sys.exit('!! unknown sfx: %s' % ', '.join(unknown))
    cache = {}
    for cue in proj.get('sfx', []):
        name = cue['name']
        if name not in cache:
            cache[name] = SFX[name]()
        s = shape_cue(cache[name], cue)
        s = s / (np.abs(s).max() + 1e-9) * 0.5 * cue.get('gain', 1.0)
        i = int(cue['t'] * SR)
        if i < 0:
            s, i = s[-i:], 0
        fx[i:i + len(s)] += s[:max(0, n - i)]
    mix = fx + room_tone(n, 0.0015)
    os.makedirs(os.path.join(P, 'audio'), exist_ok=True)
    tmp = os.path.join(P, 'audio', 'mix_raw.wav')
    pcm = np.clip(mix / max(1.0, np.abs(mix).max()), -1, 1)
    import wave
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((pcm * 32767).astype(np.int16).tobytes())
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])
    gain = -14.0 - I
    out = os.path.join(P, 'audio', 'mix.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'volume={gain:.2f}dB,alimiter=limit=0.89:attack=3:release=50:level=disabled',
                    '-ar', '48000', '-ac', '2', out], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-b:a', '160k', os.path.join(P, 'audio', 'mix.mp3')], check=True)
    os.remove(tmp)
    print(f'mix ok (sound only)  dur={dur:.2f}s  measured {I:.1f} LUFS -> gain {gain:+.1f} dB  cues={len(proj.get("sfx", []))}')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        print(', '.join(sorted(n for n in SFX if n not in BANNED)))
        print('music tracks:', ', '.join(music_tracks()) or 'none (assets/music/ is empty)')
        print('recorded:', ', '.join(sorted(RECORDED)) if RECORDED else 'none (assets/sfx/ is empty or missing)')
    else:
        main()
