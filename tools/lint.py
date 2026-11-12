#!/usr/bin/env python3
"""Check a project's scene plan before rendering. usage: python3 lint.py PROJECT_DIR
Prints one line per problem, or OK. Fix every line, then re-run."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
from cast import CAST
import director as DR
import sets as SETS


def main():
    P = sys.argv[1]
    pf = os.path.join(P, 'project-files')
    proj = json.load(open(os.path.join(pf, 'project.json')))
    tp = os.path.join(pf, 'timing.json')
    dur = json.load(open(tp))['dur'] if os.path.exists(tp) else proj['scenes'][-1]['end']
    probs = []
    sc = proj.get('scenes', [])
    if not sc:
        print('no scenes'); sys.exit(1)
    if abs(sc[0]['start']) > 0.01: probs.append('scene 1 must start at 0.0 (frame 0 is the hook)')
    if abs(sc[-1]['end'] - dur) > 0.06: probs.append(f'last scene ends at {sc[-1]["end"]} but the voice is {dur:.2f} s')
    cp = os.path.join(pf, 'custom.py')
    if os.path.exists(cp):  # project characters/creatures (e.g. a new officer) must not be flagged as unknown
        import importlib.util
        spec = importlib.util.spec_from_file_location('custom', cp)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        if hasattr(mod, 'register'):
            mod.register(CAST, {}, DR.POSES, SETS.SETS)
    rigs = {k: f() for k, f in CAST.items()}
    capY = proj.get('captionY', 420)
    for i, s in enumerate(sc, 1):
        L = s['end'] - s['start']
        if i > 1 and abs(s['start'] - sc[i - 2]['end']) > 0.01: probs.append(f'scene {i}: gap/overlap with scene {i-1}')
        if L < 1.0: probs.append(f'scene {i}: only {L:.2f} s (min ~1.2 s unless it is a deliberate flash cut)')
        if L > 4.0: probs.append(f'scene {i}: {L:.2f} s long - split it or add a camera move/key every 1.5 s')
        if not s.get('desc'): probs.append(f'scene {i}: add "desc" (what happens + why this camera)')
        if s['set'] not in SETS.SETS: probs.append(f'scene {i}: unknown set {s["set"]} (have {list(SETS.SETS)})'); continue
        if s.get('variant') and s['variant'] not in SETS.VARIANTS[s['set']]:
            probs.append(f'scene {i}: unknown variant {s["variant"]} for {s["set"]}')
        marks = {'L': 290, 'CL': 450, 'C': 560, 'CR': 680, 'R': 830}
        floor = {'harbor': 1660, 'room': 1700, 'forest': 1690, 'village': 1640}.get(s['set'], 1660)
        cam = s.get('cam', {})
        for c in [cam.get('from', [0, 0, 1]), cam.get('to', cam.get('from', [0, 0, 1]))]:
            zz = 1 + (c[2] - 1) * 1.0
            for a in s.get('actors', []):
                if a['who'] not in rigs: probs.append(f'scene {i}: unknown actor {a["who"]}'); continue
                for p in [a.get('pose', 'idle')] + [k['pose'] for k in a.get('keys', [])]:
                    if isinstance(p, str) and p not in DR.POSES.get(a['who'], DR.HUMAN):
                        probs.append(f'scene {i}: {a["who"]} has no pose "{p}" (have {sorted(DR.POSES.get(a["who"], DR.HUMAN))})')
                xs = [a.get('mark', a.get('x', 'C'))] + ([a['walk']['to']] if a.get('walk') else [])
                for xv in xs:
                    x = marks.get(xv, 560) if isinstance(xv, str) else xv
                    sx = zz * x + (1 - zz) * 540 - c[0]
                    if not 70 < sx < 1010: probs.append(f'scene {i}: {a["who"]} off screen (x={sx:.0f}) with camera {c}')
                scale = a.get('scale', 0.8)
                head = a.get('y', floor) - rigs[a['who']].height * scale * 0.95
                sy = zz * head + (1 - zz) * 960 - c[1]
                if a['who'] != 'kupas' and sy < capY + 90 and proj.get('captions'):
                    probs.append(f'scene {i}: {a["who"]} head (y={sy:.0f}) runs into the caption band (y={capY}) - zoom less / lower captionY')
                if L > 2.5 and not a.get('keys') and not a.get('walk') and not a.get('talk'):
                    probs.append(f'scene {i}: {a["who"]} holds one pose for {L:.1f} s - add a key (reaction)')
    if not proj.get('hook'): probs.append('add "hook": {"text": "2-4 words", "s": 0, "e": 2}')
    cta = proj.get('cta')
    if cta:
        if cta['s'] < 3 or cta['e'] > dur - 3: probs.append('cta must not be in the first or last 3 s')
        if not (0.4 * dur <= cta['s'] <= 0.65 * dur): probs.append(f'cta start {cta["s"]} should be ~45-60 % of {dur:.1f} s')
    for c in proj.get('captions', []):
        if len(c['text'].replace('*', '')) > 26: probs.append(f'caption too long (max ~26 chars): "{c["text"]}"')
    if probs:
        print('\n'.join(probs)); sys.exit(1)
    print('OK')


if __name__ == '__main__':
    main()
