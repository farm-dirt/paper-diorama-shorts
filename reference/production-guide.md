# Production guide — stack, audio, render, QA

## Why this stack (explain in plain words if asked)
- **One renderer** (`engine/`, Python + numpy + OpenCV) draws any moment `t` of the video as
  layers of cut paper. Preview and final come from the same code, so what you approve is what renders.
- Static set pieces are built and blurred once, then reused for every frame (fast). Characters
  are redrawn 12 times a second (stop-motion feel).
- The **browser preview** (`build_preview.py`) is a web page: the FULL-size final render (light web copy) with sound, a timeline,
  one card per scene (thumbnail, what is said, notes box, Play this scene), loop, full screen, and
  Send notes / Approve buttons that save to the page's db at `feedback/latest`.
- `render.py` splits the frames across the CPU cores and pipes them into **FFmpeg** (H.264).
- `timing.py` + `audio.py` analyse the voice and mix music/SFX: synthesised ones, or the user's own recorded library in `assets/sfx/` and `assets/music/` (see the READMEs there).
- Not used: Blender/real 3D (much bigger install and learning curve), Whisper (model download blocked).

## Commands (Claude runs them; the user never types commands)
```bash
python3 ~/pds/tools/new_project.py ~/shorts <slug> "<Title>"
python3 ~/pds/tools/timing.py VOICE ~/shorts/<slug>/project-files/timing.json --script ~/shorts/<slug>/script/script.txt
python3 ~/pds/tools/lint.py ~/shorts/<slug>                       # must say OK
python3 ~/pds/tools/audio.py ~/shorts/<slug>                      # audio/mix.wav + mix.mp3
python3 ~/pds/tools/stills.py ~/shorts/<slug> 0.0 4.2 9.8 --out /tmp/check.jpg   # spot check
python3 ~/pds/tools/build_preview.py ~/shorts/<slug>             # renders final/<slug>.mp4 (1080x1920) + preview/ page (web copy, thumbs, index.html); --half = quick blurry check
python3 ~/pds/tools/render.py ~/shorts/<slug> --from 4.9 --to 7.3 --preview --out /tmp/clip.mp4
python3 ~/pds/tools/render.py ~/shorts/<slug>                     # final/<slug>.mp4
python3 ~/pds/tools/qa.py ~/shorts/<slug> ~/shorts/<slug>/final/<slug>.mp4
python3 ~/pds/tools/stills.py ~/shorts/<slug> --thumb thumb_A.json --title "TEXT" --hl WORD --out ~/shorts/<slug>/final/thumbnail_A.png
python3 ~/pds/tools/model_sheet.py ~/shorts/<slug>/characters/model_sheet.png
```
Needs: python3 with numpy, opencv-python (cv2), Pillow; ffmpeg. Check with
`python3 -c "import numpy, cv2, PIL"` and `ffmpeg -version`.

## Speed (2 CPUs)
Preview = final render ≈ 0.45 s/frame wall (60 s short ≈ 11 min; run it in the background and poll).
Only re-render after preview changes; an approved preview needs no extra final render. `--half` ≈ 0.1 s/frame.
Rack focus and many actors are the slowest shots. Render the final in the background only if the
session will stay open; otherwise render in the foreground with a long timeout.

## Audio levels (user preference — the voice must always be clearly heard)
Music bed 8 % of the voice level while speaking, 14 % in pauses ≥ 0.6 s; SFX peak at 35 % of
the voice peak; final −14 LUFS, true peak ≤ −1 dBFS, AAC 192k 48 kHz. Music `bpm` 76-92 suits this
calmer, handmade style. `music.stops` = a silence beat before a scare/punchline.
SFX list: `python3 ~/pds/tools/audio.py --list`.

## Export
1080×1920, 24 fps (stop-motion feel), H.264 CRF 16, yuv420p, GOP 24, +faststart, AAC 192k.

## QA — must all PASS
resolution, fps 24, frame count = round(dur×24), duration = voice ±0.1 s, H.264/yuv420p, AAC,
−14 LUFS ±1.5, true peak ≤ −1 dBFS, no black frames, no frozen stretch > 1.5 s. Then LOOK at
`scenes/contact_sheet.jpg`: same character designs every shot, captions readable and not on faces,
nothing cut off, no empty frames.

## Project folder
```
<slug>/ script/ voice-over/ characters/ assets/ scenes/ audio/ preview/ final/ project-files/
```
`project-files/`: project.json, timing.json, custom.py (optional). Copy the whole folder to the
user's connected computer folder at the end.

## New sounds for every short (user rule, 24 Nov 2026)
The user heard the same library sounds (fire crackle, steam hiss, sparkle) in every short. So each short gets its
OWN foley, made by `tools/foley.py` from a `"foley"` block in project.json (seeded by slug + name, so takes differ
every short) into `project-files/sfx/`, which audio.py loads before the shared library. Rules:
- one sound per visible action, on its exact frame; footsteps on every walk step (vary 3-4 takes);
- a different quiet bed per place (`bed_*` kinds), crossfading ~0.5 s across each transition;
- every transition has its own sound (dive = rising swoosh, fog = breath hiss, gust = blown snow, dark = soft whoomp);
- no low rumbles: beds are high-passed at 150 Hz; sound-only shorts (`"voice": null`) are mixed to -14 LUFS.
Use the shared assets/sfx library only when foley.py has no kind for the action (then add a kind next time).
