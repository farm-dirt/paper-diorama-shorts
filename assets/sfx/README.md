# Recorded sound effects

Put the user's own recorded sounds here (WAV, MP3, FLAC or OGG). Each one is usable in
`project.json` by its file name, e.g. `paper_rip.wav` -> `{"t": 3.2, "name": "paper_rip"}`.

Library (added 14 Nov 2026, user-supplied; leading silence trimmed, mono 48 kHz, long ambiences cut to 60 s):
- Hits & stings: `impact_hit`, `low_hit`, `deep_boom`, `suspense_sting`, `dark_click`, `riser`
- Magic: `magic_sparkle`, `sparkle_whoosh`
- Comedy: `falling_whistle`
- Action: `sword_clash`, `rocks`, `water_splash`, `thunder`, `door_creak`, `footsteps_gravel`
- Creatures/body: `monster_growl`, `heartbeat`
- Ambience (use `dur` + `fadeIn`/`fadeOut`, quiet `gain` 0.3-0.5): `wind_howl`, `fire_crackle`, `night_ambience`

Still missing (attach to add): `paper_rip`, `paper_tear`, `paper_rustle`, `bell`, `pop`.
A recorded file with the same name as a synth sound replaces it; the synth stays as `<name>_synth`.

Cue options: `gain`, `dur` (cut length in seconds), `fadeIn`, `fadeOut` (seconds).
Check what's loaded with: `python3 tools/audio.py --list`
