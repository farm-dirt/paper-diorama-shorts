#!/usr/bin/env python3
"""Cast line-up on a paper backdrop. usage: python3 model_sheet.py OUT.png [who1 who2 ...]"""
import os, sys
import cv2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from paperkit import Scene, Layer, grade
from cast import CAST


def main():
    out = sys.argv[1]
    who = sys.argv[2:] or list(CAST)
    W = 380 * len(who) + 120
    S = Scene(W, 1180, bg='#E7D9BD')
    bg = Layer(W, 1180, seed=300, grain=0.08)
    bg.rect(0, 0, W, 1180, '#E7D9BD', rim=0, shadow=0, rough=0)
    S.add(bg, 3, lift=0)
    sh = Layer(W, 1180, seed=301)
    sh.rect(-20, 1010, W + 20, 1200, '#C9A777', pat='planks', pat_period=90)
    S.add(sh, 2.2, lift=0.6)
    for i, w in enumerate(who):
        L, fx, fy = CAST[w]().render(pose={'face': -1} if w == 'kupas' else {}, scale=1.0, seed=31 + i)
        S.add(L, 2.0, lift=1.0, x=120 + 380 * i + 150 - fx, y=1030 - fy)
    img = grade(S.render(focus=2, dof=0), vignette=0.25)
    cv2.imwrite(out, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    print(out)


if __name__ == '__main__':
    main()
