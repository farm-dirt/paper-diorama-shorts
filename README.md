# paper-diorama-shorts

Personal engine for vertical (1080x1920) animated YouTube Shorts in a **handmade paper-diorama**
style: cut-paper characters and sets with paper grain, cut edges, fold creases, drop shadows
between layers, shallow depth of field, warm practical lights, and stop-motion "on twos" acting.
Original cast (Ilaw, Mang Oso, Kupas) and original sets (harbor, room, forest, village).

Used by the Claude skill `paper-diorama-shorts` (script -> voice-over -> preview -> final MP4).
Separate from, and shares no art with, `pastel-toon-shorts`. The general tools `timing.py`,
`audio.py`, `new_project.py` and `qa.py` started as copies from that engine and were adapted.

```
engine/     paperkit.py (paper renderer), cast.py (characters), sets.py (locations), director.py (project -> frames)
tools/      new_project, timing, audio, lint, stills (+ thumbnails), render, qa, model_sheet
reference/  style-guide, animation-guide (project.json schema), characters, production-guide, content-playbook
assets/     Fraunces Black font (SIL Open Font License, see Fraunces-OFL.txt)
examples/   test5/project.json - a 5-second two-scene example
```
Requirements: python3, numpy, opencv-python, Pillow, ffmpeg.
