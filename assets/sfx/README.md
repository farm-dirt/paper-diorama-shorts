# Recorded sound effects

Put the user's own recorded sounds here (WAV, MP3, FLAC or OGG). Each one is usable in
`project.json` by its file name, e.g. `paper_rip.wav` -> `{"t": 3.2, "name": "paper_rip"}`.

Expected library: `paper_rip`, `paper_tear`, `paper_rustle`, `wind`, `bell`, `pop`.
A recorded `pop` replaces the synth one, which stays available as `pop_synth`.

Cue options: `gain`, `dur` (cut length in seconds), `fadeIn`, `fadeOut` (seconds).
Check what's loaded with: `python3 tools/audio.py --list`
