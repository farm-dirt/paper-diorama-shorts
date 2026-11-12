#!/usr/bin/env python3
"""Render a project to MP4 with the paper engine.

usage: python3 render.py PROJECT_DIR [--preview] [--from S] [--to E] [--out FILE] [--workers N] [--noaudio]
  --preview   half resolution (540x960), fast encode -> preview/preview.mp4
  default     1080x1920, 24 fps, H.264 CRF 16 yuv420p, AAC 192k, +faststart -> final/<slug>.mp4
Frames are split into contiguous chunks across CPU workers; each worker builds the
sets once and reuses cached paper layers, then the chunks are joined and the audio
mix (audio/mix.wav, else the raw voice-over) is added.
"""
import json
import math
import multiprocessing as mp
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))


def work(args):
    pdir, k, fps, f0, f1, seg, preview = args
    import paperkit
    paperkit.set_res(k)
    from director import Director
    D = Director(pdir)
    w, h = int(math.ceil(1080 * k)), int(math.ceil(1920 * k))
    enc = ['-c:v', 'libx264', '-preset', 'veryfast' if preview else 'medium', '-crf', '28' if preview else '19',
           '-pix_fmt', 'yuv420p', '-g', str(fps)]
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}',
                           '-r', str(fps), '-i', '-', *enc, seg], stdin=subprocess.PIPE)
    t0 = time.time()
    for f in range(f0, f1):
        ff.stdin.write(D.frame(f / fps, f).tobytes())
        if (f - f0) % 48 == 0 and f > f0:
            print(f'  worker {f0}: {f - f0}/{f1 - f0} frames, {(time.time() - t0) / (f - f0):.2f} s/frame', flush=True)
    ff.stdin.close()
    ff.wait()
    return seg


def main():
    a = sys.argv[1:]
    pdir = os.path.abspath(a[0])
    preview = '--preview' in a

    def opt(name, default=None, cast=float):
        return cast(a[a.index(name) + 1]) if name in a else default
    proj = json.load(open(os.path.join(pdir, 'project-files', 'project.json')))
    tp = os.path.join(pdir, 'project-files', 'timing.json')
    dur = json.load(open(tp))['dur'] if os.path.exists(tp) else proj['scenes'][-1]['end']
    fps = proj.get('fps', 24)
    t_from, t_to = opt('--from', 0.0), opt('--to', dur)
    f0, f1 = int(round(t_from * fps)), int(round(t_to * fps))
    k = 0.5 if preview else 1.0
    nw = int(opt('--workers', os.cpu_count() or 2, int))
    out = opt('--out', None, str) or (os.path.join(pdir, 'preview', 'preview.mp4') if preview
                                      else os.path.join(pdir, 'final', f"{proj['slug']}.mp4"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = os.path.join(pdir, 'project-files', '_segs')
    os.makedirs(tmp, exist_ok=True)
    n = f1 - f0
    chunks = [(pdir, k, fps, f0 + i * n // nw, f0 + (i + 1) * n // nw, os.path.join(tmp, f'seg{i}.mp4'), preview)
              for i in range(nw) if (i + 1) * n // nw > i * n // nw]
    t0 = time.time()
    print(f'rendering {n} frames ({t_from:.2f}-{t_to:.2f} s) at {int(1080 * k)}x{int(1920 * k)} with {len(chunks)} workers')
    if len(chunks) == 1:
        segs = [work(chunks[0])]
    else:
        with mp.get_context('fork').Pool(len(chunks)) as pool:
            segs = pool.map(work, chunks)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
    joined = os.path.join(tmp, 'joined.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', joined], check=True)
    mixp = os.path.join(pdir, 'audio', 'mix.wav')
    voice = os.path.join(pdir, 'voice-over', proj.get('voice', 'voice.mp3'))
    audio = mixp if os.path.exists(mixp) else (voice if os.path.exists(voice) else None)
    if audio and '--noaudio' not in a:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', joined, '-ss', f'{t_from:.3f}', '-t', f'{t_to - t_from:.3f}',
                        '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'apad', '-c:a', 'aac', '-b:a', '192k',
                        '-ar', '48000', '-t', f'{(f1 - f0) / fps:.3f}', '-movflags', '+faststart', out], check=True)
    else:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', joined, '-c', 'copy', '-movflags', '+faststart', out], check=True)
    for s in segs + [joined, lst]:
        os.remove(s)
    el = time.time() - t0
    print(f'done: {out}  ({el:.0f} s, {el / max(1, n):.2f} s/frame wall)')


if __name__ == '__main__':
    main()
