# Production guide — stack, audio, render, QA

## Why this stack (explain in plain words if asked)
- **One renderer** (`engine/`, Python + numpy + OpenCV) draws any moment `t` of the video as
  layers of cut paper. Preview and final come from the same code, so what you approve is what renders.
- Static set pieces are built and blurred once, then reused for every frame (fast). Characters
  are redrawn 12 times a second (stop-motion feel).
- `render.py` splits the frames across the CPU cores and pipes them into **FFmpeg** (H.264).
- `timing.py` + `audio.py` analyse the voice and synthesise music/SFX (no downloads, no copyright issues).
- Not used: Blender/real 3D (much bigger install and learning curve), Whisper (model download blocked).

## Commands (Claude runs them; the user never types commands)
```bash
python3 ~/pds/tools/new_project.py ~/shorts <slug> "<Title>"
python3 ~/pds/tools/timing.py VOICE ~/shorts/<slug>/project-files/timing.json --script ~/shorts/<slug>/script/script.txt
python3 ~/pds/tools/lint.py ~/shorts/<slug>                       # must say OK
python3 ~/pds/tools/audio.py ~/shorts/<slug>                      # audio/mix.wav + mix.mp3
python3 ~/pds/tools/stills.py ~/shorts/<slug> 0.0 4.2 9.8 --out /tmp/check.jpg   # spot check
python3 ~/pds/tools/render.py ~/shorts/<slug> --preview           # preview/preview.mp4 (540x960)
python3 ~/pds/tools/render.py ~/shorts/<slug> --from 4.9 --to 7.3 --preview --out /tmp/clip.mp4
python3 ~/pds/tools/render.py ~/shorts/<slug>                     # final/<slug>.mp4
python3 ~/pds/tools/qa.py ~/shorts/<slug> ~/shorts/<slug>/final/<slug>.mp4
python3 ~/pds/tools/stills.py ~/shorts/<slug> --thumb thumb_A.json --title "TEXT" --hl WORD --out ~/shorts/<slug>/final/thumbnail_A.png
python3 ~/pds/tools/model_sheet.py ~/shorts/<slug>/characters/model_sheet.png
```
Needs: python3 with numpy, opencv-python (cv2), Pillow; ffmpeg. Check with
`python3 -c "import numpy, cv2, PIL"` and `ffmpeg -version`.

## Speed (2 CPUs)
Preview ≈ 0.15 s/frame wall (45 s short ≈ 3 min). Final ≈ 0.7 s/frame wall (45 s ≈ 12-13 min).
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
