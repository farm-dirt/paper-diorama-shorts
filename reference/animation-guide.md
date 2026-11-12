# Animation guide — project.json schema + directing

The voice-over is the master clock. All times are **absolute seconds** in the video.

## project.json
```json
{
  "id": "slug", "slug": "slug", "title": "Title", "fps": 24, "voice": "voice.mp3",
  "captionY": 420,
  "hook": {"text": "She *followed* the light…", "s": 0, "e": 1.8, "y": 330},
  "captions": [{"s": 2.1, "e": 3.0, "text": "into the *balete* forest"}],
  "cta": {"s": 21.0, "e": 23.6, "tap": 0.95, "y": 1440},
  "music": {"on": true, "bpm": 84, "key": 0, "stops": [[30.2, 30.9]]},
  "mix": {"music": 0.08, "musicPause": 0.14, "sfx": 0.35},
  "sfx": [{"t": 4.0, "name": "thud", "gain": 1.0}],
  "scenes": [
    {"start": 0.0, "end": 2.4, "set": "harbor", "variant": "dusk",
     "desc": "what happens + WHY this camera",
     "cam": {"from": [0, 0, 1.0], "to": [40, -60, 1.18], "ease": "inOut"},
     "focus": 2.0, "dof": 0.85,
     "rack": {"t": 1.6, "to": 1.0, "dur": 0.5},
     "shake": {"t": 2.0, "dur": 0.4, "amp": 12},
     "flash": {"t": 2.1, "dur": 0.2, "color": "#D2453A"},
     "light": "night", "letterbox": 0,
     "actors": [
       {"who": "ilaw", "mark": "C", "scale": 0.86, "z": 2.0, "face": 1,
        "pose": "idle",
        "keys": [{"t": 1.1, "pose": "look_up", "dur": 0.3, "ease": "back"}],
        "walk": {"s": 0.4, "e": 1.6, "to": "R", "rate": 1.8},
        "talk": [[0.3, 1.2]]}
     ]}
  ]
}
```
- `cam` = [pan_x, pan_y, zoom] in px; parallax is automatic (near layers move/zoom more).
  Keep zoom 0.95-1.4. Positive pan_x moves the view right; negative pan_y looks up.
- `focus` default 2.0 (the actors). `rack` moves focus during the shot.
- `light` overrides the set's default time-of-day grade.
- Actor `mark`: L, CL, C, CR, R (set-specific x) or `"x": 640`. `y` defaults to the set floor.
  `z` 2.0 normal; 1.6-1.8 = a step closer to camera (slightly blurred - use for a looming reaction).
- `pose`: a name from the pose library or a dict of bone angles/face values.
  `keys`: pose changes at absolute times; `dur` is the blend time; `ease` back|out|inOut|linear.
- `walk`: moves from mark to `to` between `s` and `e` (ease inOut by default). Humans use a front-on
  puppet walk (feet lift in turn, body sways); Kupas trots side-on and turns to face the direction.
  Steps are timed to the distance, so a longer walk in the same time = faster steps. Keep walks
  slower than ~300 px/s so it doesn't look like running.
- `talk`: true (whole scene) or windows [[s,e]]; mouth follows the voice loudness. Only for the
  character who is actually speaking (in-character lines), never for the narrator.

## Pose library
Humans (ilaw, mang_oso): idle, wave, point, point_up, shock, scared, sad, happy, cheer, think,
angry, look_up, look_back, cower, shrug.  Dog (kupas): idle, wag, alert, bark, sad, scared, happy.
Face values usable in any pose dict: `eyes` (0.6 squint … 1.5 wide), `brow` (-1 worried … 1 angry),
`mouth` 0-1, `look` -1…1, `blink`, `bob` (px). Bones: root, torso, head, armR, armL, legL, legR
(+ lantern for Ilaw, oar for Mang Oso with `"prop": "oar"`; dog: head, tail, body, legFL/FR/BL/BR).

## Sets (locations) and variants
| set | variants | marks (x) | good for |
|---|---|---|---|
| harbor | dusk, night | L 290 · CL 450 · C 560 · CR 680 · R 830 | journeys, sea legends, goodbyes |
| room | lamp, day | L 280 … R 800 | storytelling at home, lola, reactions |
| forest | night | L 230 … R 860 | creatures, balete tree, fireflies, scares |
| village | day, dusk | L 250 … R 830 | daily life, crowds of rumours, comedy |
New locations / creatures / props for one short go in `project-files/custom.py` (below). If a
new location will be reused, add it to `engine/sets.py` instead (ask the user first).

## custom.py (per short, optional)
```python
from paperkit import Layer
def register(CAST, rigs, POSES, SETS):      # add new characters/creatures/poses
    pass
def draw(scene, S, t, ctx):                 # add paper layers to this frame
    if scene.get('id') == 'reveal':
        L = Layer(1080, 1920, seed=900)
        L.ellipse(540, 900, 120, 160, '#2B2240', n=14)         # cut-paper shape
        L.ellipse(500, 860, 14, 18, '#FFE58A', paint=True, glow=0.3)
        S.add(L, 3.0, lift=1.2)                                 # z, lift
    return [(500, 860, 60, '#FFE58A', 0.4)]                     # extra glows
```
Build creatures the same way as the cast (see `characters.md`): faceted cut paper, one
strange trait made huge, 3-5 colours, no outlines. Static creature layers can pass `key=` to be cached.

## Directing rules
- **Frame 0 is the hook**: the strangest image is already on screen at t = 0; hook text 0-2 s.
- Cut on voice pauses (`timing.sentences`/`pauses`); shots 1.2-3.5 s.
- Something visibly changes at least every 1.5 s (key pose, camera, rack, glow, prop).
- Hold a strong reaction ~0.3 s longer than feels natural; never snap straight back to idle.
- Every camera move has a reason (reveal, tension, comedy timing) — write it in `desc`.
- Gags and reactions land on the word: key time = word start − 0.08 s.
- Sound for every visible action (step, grab, flap, landing); a silence (`music.stops`) right
  before the scare/punchline.
- Variety: change set/variant or angle (zoom/pan) between consecutive scenes; reuse the cast as
  recurring witnesses so viewers recognise them across the series.
- Captions sit at `captionY` (~420); keep heads below ~520 on screen (lint checks this).
