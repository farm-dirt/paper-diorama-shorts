# paper-diorama-shorts

Personal engine for vertical (1080x1920) animated YouTube Shorts in a **handmade paper-diorama**
style: cut-paper characters and sets with paper grain, cut edges, fold creases, drop shadows
between layers, shallow depth of field, warm practical lights, and stop-motion "on twos" acting.
Channel: **Tiny Olympus** (Greek gods behaving badly). Greek starter kit in `engine/greek.py`: cast zeus,
hera, aphrodite, ares, mortal_man, mortal_woman (+ `greek.add_figure` for more) and sets temple, olympus,
sea_cliff, cave. The first-version folklore cast (Ilaw, Mang Oso, Kupas) and sets (harbor, room, forest,
village) are still in `cast.py` / `sets.py`.

Used by the Claude skill `paper-diorama-shorts` (script -> voice-over -> preview -> final MP4).
Separate from, and shares no art with, `pastel-toon-shorts`. The general tools `timing.py`,
`audio.py`, `new_project.py` and `qa.py` started as copies from that engine and were adapted.

```
engine/     preview.html (preview page), paperkit.py (paper renderer), cast.py (characters), sets.py (locations), greek.py (Greek cast + sets), director.py (project -> frames)
tools/      new_project, timing, audio (music floor + room tone: never dead air), lint (safe box, CTA, banned sounds), stills (+ thumbnails), render, build_preview (web page), qa (incl. dead-air check), model_sheet
reference/  style-guide, animation-guide (project.json schema), characters, production-guide, content-playbook
assets/     Fraunces Black font (SIL Open Font License, see Fraunces-OFL.txt); music/ and sfx/ = the user's own downloaded library (sources: see their READMEs)
examples/   olympus/project.json - a Greek example (temple + olympus); test5/project.json - the first folklore example
```
Requirements: python3, numpy, opencv-python, Pillow, ffmpeg.
