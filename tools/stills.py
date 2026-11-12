#!/usr/bin/env python3
"""Spot-check stills and thumbnails.

stills:    python3 stills.py PROJECT_DIR T1 T2 ... [--out strip.jpg] [--k 0.5]
           renders those moments side by side -> strip (always include 0.0)
thumbnail: python3 stills.py PROJECT_DIR --thumb thumb_scene.json --title "NEVER FOLLOW IT" --hl FOLLOW --out final/thumbnail_A.png
           thumb_scene.json = ONE scene object (same schema as project scenes, start 0, end 1),
           rendered at 1080x1920 with no captions, then a big title in the top third.
"""
import json, os, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import paperkit


def main():
    a = sys.argv[1:]
    pdir = a[0]
    def opt(n, d=None):
        return a[a.index(n) + 1] if n in a else d
    out = opt('--out')
    if '--thumb' in a:
        paperkit.set_res(1.0)
        from director import Director
        D = Director(pdir)
        D.life = False
        sc = json.load(open(opt('--thumb')))
        sc.update(start=0, end=1)
        D.proj = dict(D.proj, scenes=[sc], captions=[], hook=None, cta=None)
        img = Image.fromarray(D.frame(0.5))
        title = opt('--title', '')
        if title:
            hl = (opt('--hl') or '').upper()
            d = ImageDraw.Draw(img)
            size = 150
            f = ImageFont.truetype(os.path.join(ROOT, 'assets', 'Fraunces-Black.woff'), size)
            while f.getlength(title.upper()) > 1000 and size > 90:
                size -= 6
                f = ImageFont.truetype(os.path.join(ROOT, 'assets', 'Fraunces-Black.woff'), size)
            words, lines, cur = title.upper().split(), [], ''
            for w in words:
                if f.getlength((cur + ' ' + w).strip()) > 980:
                    lines.append(cur); cur = w
                else:
                    cur = (cur + ' ' + w).strip()
            lines.append(cur)
            y = 230
            for ln in lines:
                x = (1080 - f.getlength(ln)) / 2
                for w in ln.split():
                    col = (255, 205, 80) if w.strip('.,!?…') == hl else (250, 244, 232)
                    d.text((x, y), w, font=f, fill=col, stroke_width=10, stroke_fill=(30, 20, 22))
                    x += f.getlength(w + ' ')
                y += int(size * 1.08)
        img.save(out or os.path.join(pdir, 'final', 'thumbnail.png'))
        print(out)
        return
    k = float(opt('--k', 0.5))
    paperkit.set_res(k)
    from director import Director
    D = Director(pdir)
    ts = [float(x) for x in a[1:] if not x.startswith('--') and x not in (out, opt('--k'))]
    frames = [D.frame(t, i) for i, t in enumerate(ts)]
    strip = np.hstack(frames)
    out = out or '/tmp/stills.jpg'
    cv2.imwrite(out, cv2.cvtColor(strip, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(out)


if __name__ == '__main__':
    main()
