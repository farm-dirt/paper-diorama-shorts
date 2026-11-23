#!/usr/bin/env python3
"""Free AI narrator (Kokoro, open-source, runs here; no ElevenLabs credits needed).

usage:
  python3 voice.py SCRIPT.txt OUT.wav [--voice am_michael] [--speed 1.0] [--pronounce FILE.json]
  python3 voice.py --samples OUT_DIR "text to read" am_michael am_fenrir ...
  python3 voice.py --check            # install check + model download only

How it reads the script:
  * one sentence at a time, joined with a short pause (0.30 s) so timing.py
    can snap sentences to real pauses; a blank line = new paragraph (0.45 s).
  * "..." inside a sentence becomes the voice's own pause.
  * a line "[pause 3.2]" adds exactly that many seconds of silence (for sound-only
    beats, e.g. food/ASMR moments); it is never read aloud.
  * also writes OUT.sentences.json with the EXACT start/end of every sentence;
    timing.py uses it instead of guessing sentence edges from pauses.
  * hard names: pronounce.json maps a spelling to one the voice says right
    ({"Thales": "Thaylees"}). Engine-wide list: tools/pronounce.json;
    a project can add its own (project-files/pronounce.json, passed with --pronounce).
    Check a spelling with:  python3 voice.py --phonemes "Thaylees"
Writes OUT.wav (24 kHz mono) and OUT.mp3 next to it.

Needs: pip install kokoro-onnx soundfile (approved by the user, 23 Nov 2026).
Model files (~350 MB) download once into ~/.cache/pds-voice from the
kokoro-onnx GitHub release.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.expanduser('~/.cache/pds-voice')
REL = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
FILES = ['kokoro-v1.0.onnx', 'voices-v1.0.bin']
SENT_GAP, PARA_GAP = 0.30, 0.45
DEFAULT_VOICE = 'am_michael'


def ensure():
    try:
        import kokoro_onnx, soundfile  # noqa: F401
    except ImportError:
        sys.exit('Missing kokoro-onnx/soundfile. Run: pip install --break-system-packages kokoro-onnx soundfile')
    os.makedirs(CACHE, exist_ok=True)
    for f in FILES:
        p = os.path.join(CACHE, f)
        if not os.path.exists(p) or os.path.getsize(p) < 1_000_000:
            print('downloading', f, '...', flush=True)
            subprocess.run(['curl', '-sSL', '--fail', '-o', p, REL + f], check=True)
    from kokoro_onnx import Kokoro
    return Kokoro(os.path.join(CACHE, FILES[0]), os.path.join(CACHE, FILES[1]))


def load_map(extra):
    m = {}
    for p in [os.path.join(HERE, 'pronounce.json'), extra]:
        if p and os.path.exists(p):
            m.update(json.load(open(p)))
    return m


def respell(text, m):
    for k in sorted(m, key=len, reverse=True):
        text = re.sub(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', m[k], text, flags=re.I)
    return text


def sentences(par):
    # split after . ! ? (not after "..." mid-sentence pauses)
    parts = re.split(r'(?<=[^.][.!?])\s+(?=[A-Z"\'])', par.strip())
    return [p.strip() for p in parts if p.strip()]


def synth(k, text, voice, speed):
    a, sr = k.create(text, voice=voice, speed=speed, lang='en-us')
    return a, sr


def main():
    import numpy as np
    import soundfile as sf
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__); return
    if args[0] == '--check':
        ensure(); print('voice OK'); return
    k = ensure()
    if args[0] == '--phonemes':
        for w in args[1:]:
            print(w, '->', k.tokenizer.phonemize(w, 'en-us'))
        return
    if args[0] == '--samples':
        out, text, voices = args[1], args[2], args[3:] or [DEFAULT_VOICE]
        os.makedirs(out, exist_ok=True)
        text = respell(text, load_map(None))
        for v in voices:
            a, sr = synth(k, text, v, 1.0)
            w = os.path.join(out, v + '.wav'); sf.write(w, a, sr)
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', w, '-b:a', '128k', w[:-4] + '.mp3'], check=True)
            print(v, round(len(a) / sr, 1), 's')
        return
    script, out = args[0], args[1]
    opt = dict(zip(args[2::2], args[3::2]))
    voice = opt.get('--voice', DEFAULT_VOICE)
    speed = float(opt.get('--speed', 1.0))
    m = load_map(opt.get('--pronounce'))
    raw = open(script).read()
    PAUSE = re.compile(r'^\s*\[pause\s+([0-9.]+)\s*s?\]\s*$', re.I | re.M)
    # split into paragraphs; a [pause N] line is its own item
    items = []
    for par in re.split(r'\n\s*\n', raw):
        buf = []
        for line in par.split('\n'):
            mm = PAUSE.match(line)
            if mm:
                if buf: items.append(('text', ' '.join(buf))); buf = []
                items.append(('pause', float(mm.group(1))))
            elif line.strip():
                buf.append(line.strip())
        if buf: items.append(('text', ' '.join(buf)))
    chunks, sr, pos, stimes, last_gap = [], 24000, 0, [], 0
    for ii, (kind, val) in enumerate(items):
        if kind == 'pause':
            if last_gap:  # replace the normal gap after the previous sentence
                chunks.pop(); pos -= last_gap; last_gap = 0
            chunks.append(np.zeros(int(val * sr), dtype=np.float32)); pos += int(val * sr)
            continue
        sents = sentences(' '.join(val.split()))
        for si, s in enumerate(sents):
            a, sr = synth(k, respell(s, m), voice, speed)
            # trim the model's own leading/trailing silence so our gaps are exact
            nz = np.where(np.abs(a) > 0.01)[0]
            if len(nz):
                a = a[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.06 * sr)]
            chunks.append(a); last_gap = 0
            stimes.append({'s': round(pos / sr, 3), 'e': round((pos + len(a)) / sr, 3), 'text': s})
            pos += len(a)
            last = ii == len(items) - 1 and si == len(sents) - 1
            if not last:
                gap = PARA_GAP if si == len(sents) - 1 else SENT_GAP
                chunks.append(np.zeros(int(gap * sr), dtype=a.dtype)); pos += int(gap * sr); last_gap = int(gap * sr)
    pars = [v for kd, v in items if kd == 'text']
    audio = np.concatenate(chunks)
    audio = audio / max(1e-6, np.abs(audio).max()) * 0.89
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sf.write(out, audio, sr)
    json.dump(stimes, open(os.path.splitext(out)[0] + '.sentences.json', 'w'), indent=1)
    mp3 = os.path.splitext(out)[0] + '.mp3'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', out, '-b:a', '192k', mp3], check=True)
    print(f'{out}  {len(audio) / sr:.1f} s  voice={voice} speed={speed}  sentences={sum(len(sentences(" ".join(p.split()))) for p in pars)}')


if __name__ == '__main__':
    main()
