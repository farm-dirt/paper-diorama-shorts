#!/usr/bin/env python3
"""Build PROJECT_DIR/preview/ : the web page you watch and comment on before the final render.

usage: python3 build_preview.py PROJECT_DIR [--skip-video] [--half]
  1. renders the FINAL video at full size (1080x1920 Shorts, or the project's "frame", e.g. 1920x1080) (final/<slug>.mp4) and a lighter web copy preview/preview.mp4
     (--half = old quick half-size preview only; blurry, use for rough checks)
  2. renders one thumbnail per scene -> preview/thumbs/scene_NN.jpg
  3. writes preview/data.js (scenes + what is said in each) and preview/index.html
Publish the folder with the Artifact tool (index.html, data.js, preview.mp4, thumbs/*, assets/*),
then declare {"db": {}, "user": {}} once so "Send notes" / "Approve" save to feedback/latest.
Opened from disk the buttons fall back to copying the text.
"""
import json, os, shutil, subprocess, sys
import cv2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))


def main():
    P = os.path.abspath(sys.argv[1])
    out = os.path.join(P, 'preview')
    os.makedirs(os.path.join(out, 'thumbs'), exist_ok=True)
    os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
    if '--skip-video' not in sys.argv or not os.path.exists(os.path.join(out, 'preview.mp4')):
        if '--half' in sys.argv:   # quick, blurry half-size check only
            subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'render.py'), P, '--preview'], check=True)
        else:                      # default: render the FINAL at full size once; approve it = already done
            slug = json.load(open(os.path.join(P, 'project-files', 'project.json')))['slug']
            final = os.path.join(P, 'final', f'{slug}.mp4')
            subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'render.py'), P], check=True)
            # web copy: same 1080x1920 picture, lighter file (the Artifact publisher caps files at 20 MB)
            # long-form: keep the web copy under ~30 MB (publisher limit) by lowering bitrate and size to 720p
            pj = json.load(open(os.path.join(P, 'project-files', 'project.json')))
            dur_ = json.load(open(os.path.join(P, 'project-files', 'timing.json')))['dur']
            rate = max(250, min(2600, int(30 * 8 * 1024 / dur_) - 100))
            scale = ['-vf', 'scale=-2:720' if pj.get('frame', [1080, 1920])[0] > pj.get('frame', [1080, 1920])[1] else 'scale=720:-2'] if rate < 2600 else []
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', final, *scale, '-c:v', 'libx264', '-preset', 'medium', '-crf', '25',
                            '-maxrate', f'{rate}k', '-bufsize', f'{2 * rate}k', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                            '-b:a', '128k' if rate >= 2600 else '64k', '-movflags', '+faststart', os.path.join(out, 'preview.mp4')], check=True)
    import paperkit
    paperkit.set_res(0.25)
    from director import Director
    D = Director(P)
    for f in os.listdir(os.path.join(out, 'thumbs')):
        os.remove(os.path.join(out, 'thumbs', f))
    sents = D.tim.get('sentences', [])
    scenes = []
    for i, s in enumerate(D.proj['scenes']):
        mid = s['start'] + (s['end'] - s['start']) * 0.6
        cv2.imwrite(os.path.join(out, 'thumbs', f'scene_{i + 1:02d}.jpg'),
                    cv2.cvtColor(D.frame(mid, i), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
        say = ' '.join(x['text'] for x in sents if x['s'] < s['end'] - 0.05 and x['e'] > s['start'] + 0.05)
        scenes.append(dict(start=s['start'], end=s['end'], set=s['set'], variant=s.get('variant', ''),
                           desc=s.get('desc', ''), say=say))
    data = dict(title=D.proj.get('title', ''), slug=D.proj.get('slug', ''), fps=D.fps, dur=D.dur, scenes=scenes)
    open(os.path.join(out, 'data.js'), 'w').write('window.PROJECT = ' + json.dumps(data) + ';\n')
    body = open(os.path.join(ROOT, 'engine', 'preview.html'), encoding='utf-8').read().replace('__TITLE__', data['title'] or 'Preview')
    FW, FH = D.FW, D.FH
    if FW > FH:  # landscape long-form: wide player, wide scene thumbnails
        body = (body.replace('aspect-ratio:9/16', 'aspect-ratio:16/9').replace('* 9 / 16', '* 16 / 9')
                .replace('grid-template-columns:minmax(260px,440px) minmax(0,1fr)', 'grid-template-columns:minmax(0,1fr) minmax(300px,400px)')
                .replace('.stage{max-width:420px;margin:0 auto}', '.stage{max-width:100%;margin:0 auto}')
                .replace('.scene img{width:64px;height:114px', '.scene img{width:114px;height:64px')
                .replace('full size 1080×1920', f'full size {FW}×{FH}'))
    head, rest = body.split('<header>', 1)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + head + '</head><body>\n<header>' + rest + '\n</body></html>\n')
    shutil.copy(os.path.join(ROOT, 'assets', 'Fraunces-Black.woff'), os.path.join(out, 'assets'))
    print('preview ready:', os.path.join(out, 'index.html'), f'({len(scenes)} scenes, {D.dur:.2f}s)')


if __name__ == '__main__':
    main()
