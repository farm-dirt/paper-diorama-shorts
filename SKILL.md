---
name: paper-diorama-shorts
description: Personal animation studio for vertical YouTube Shorts in a handmade paper-diorama style (cut-paper miniature sets, original cast). Use when the user wants to make, script, preview or render a paper-style animated Short.
---

# paper-diorama-shorts — script → voice-over → preview → final MP4

A reusable production workflow, separate from `pastel-toon-shorts` (never edit that skill or
reuse its art). The look was analysed once from two references (a stop-motion origami sequence and
the short film *GRUFF*): a handmade miniature world of paper and card, filmed like a tiny real
set. Only the technique was taken: **never copy the references' characters, creatures, sets or
story beats**. Use the original cast in `reference/characters.md`, or new original characters
built with the same rig.

## 0. Setup (silent, every time)
1. Get the engine: `git clone --depth 1 https://github.com/farm-dirt/paper-diorama-shorts ~/pds`
   (if the folder exists: `git -C ~/pds pull`). If GitHub is unreachable, ask the user to attach
   `paper-diorama-shorts.zip` and unzip it so the engine is at `~/pds`.
2. Check tools, never assume: `python3 -c "import numpy, cv2, PIL"`, `ffmpeg -version`.
   If something is missing, explain in one plain sentence what it is and why it's needed, and ask
   before installing (pip/official sources only).
3. Read `~/pds/reference/style-guide.md`, `animation-guide.md`, `characters.md` before planning
   scenes; `production-guide.md` before audio/render steps; `content-playbook.md` for ideas and scripts.

The user is a beginner: simple words, define terms, say WHY, push back honestly on weak ideas,
warn before anything that deletes/overwrites. Keep each checkpoint message short.

## The workflow — phases in order, never skip a ⛔ checkpoint

### Phase 1 — Start (automatic, no question)
Do NOT ask "What would you like to create?". Assume **"I want a new script"** and go to Phase 2.
Exception: if the user's message already includes a script, use it and go to Phase 4
(review/tighten it, keep their voice).

### Phase 2 — Category (automatic, no question)
Do NOT list categories or ask. The category is **Local culture & legends of the Philippines**
(folklore, myths, creatures, traditions, local history). Say in one line
"Category: Philippine culture & legends" and go to Phase 3. Use another category only if the
user names one.

### Phase 3 — 10 ideas  ⛔
10 original ideas (avoid topics the user already made shorts about, in this or the pastel
series), each with **title, 1-2 line description, the hook (first 2 seconds), storytelling
potential (★1-5 + why), why it suits the paper look (which set, light, what folds/glows/moves),
format (Creature card 20-30 s or Story 40-55 s), audience fit (teen/adult tone, not a kids' moral
lesson)**. Flag your top 2. Facts must be true: search the web for anything factual before
pitching it, and note when a legend has regional versions.
**What wins in this niche (research, Nov 2026):** creature Shorts break out even on tiny channels
when they open on one creature with one weird, instantly readable trait (manananggal, aswang,
tiyanak, kapre, tikbalang, sigbin, batibat rank above moral-lesson alamat). Include at least 4
creature ideas, plus a few funny/twisted legends. The paper style shines on night scenes,
lantern light, things that unfold or tear, and reveals by rack focus. Every idea must fit the
series name (see "Series identity"). Wait for the user to pick.

### Phase 4 — Script + voice-over (ONE checkpoint)  ⛔
Write the script with the template in `content-playbook.md`: hook (0-2 s), setup, escalation,
twist/payoff, button ending. Per section: narration, est. duration (~2.6 words/s), visuals,
character actions, transition. Target 30-55 s (≈ 80-140 words) for a Story, 20-30 s
(≈ 50-75 words) for a Creature card.
**Retention rules (check every script before sending):**
- **Write the ending first**, then build backwards. One character, one goal, one problem.
- **Hook = first spoken line + first image together**: start in the middle of the strangest
  moment (never "Long ago in a village…", never a greeting). 2-4 word on-screen hook text for 0-2 s.
- **Link beats with "but" / "therefore", never "and then"**.
- **Re-hook every ~8-10 s**: a new question, reveal or reversal.
- **Show, don't narrate**: the narrator sets up, the picture delivers the joke or scare. Mark at
  least 2 moments where the picture says something the narration doesn't.
- **1-3 short in-character lines** (1-5 words, e.g. Ilaw's "Lolo?", Mang Oso's "Huwag.") recorded
  as separate clips or labelled ElevenLabs speakers in a different voice.
- **No "like and subscribe" outro.** End on the twist or a line that loops into the first line;
  the CTA is the silent mid-video paper subscribe tag (Phase 6 step 3).
- **Tone for teens/adults** (witty or spooky, "folklore explained").
**Voice-over tips (ElevenLabs v3):** expressive voice, stability "Natural" or "Creative", audio
tags like [whispers] [gasps] sparingly, "…" for a pause, CAPS for one stressed word. A calm,
storyteller read suits this handmade style. Suggest once that their own voice stands out.
Save `script/script.md` (full) and `script/script.txt` (narration only, exactly as spoken). Send
ONE message: the script, the narration in a code block ready to copy, short voice-over
instructions (MP3/WAV, read exactly, small pauses between sentences). End with:
"Record it and upload the file, or tell me what to change in the script."
Uploading the voice-over counts as approving the script. If they changed words while recording,
update `script/script.txt` to match.

### Phase 5 — Process the voice-over (starts as soon as the upload arrives)
Never build animation before the voice-over arrives. Then, without asking:
```bash
python3 ~/pds/tools/new_project.py ~/shorts <slug> "<Title>"
cp <upload> ~/shorts/<slug>/voice-over/voice.<ext>               # set "voice" in project.json
python3 ~/pds/tools/timing.py ~/shorts/<slug>/voice-over/voice.<ext> ~/shorts/<slug>/project-files/timing.json --script ~/shorts/<slug>/script/script.txt
```
Report in 3-4 lines: duration, sentences matched to pauses, any sentence whose length looks off
(≥ 40 % different from the word-count estimate = misread/skipped line → tell the user).
The voice-over is the master clock: cuts go on real pauses.

### Phase 6 — Build the animation
1. **Shot plan** in `project-files/project.json` (schema + pose library + sets in
   `animation-guide.md`). One scene per phrase/sentence, cut on pauses, 1.2-3.5 s per shot.
   - **Frame 0 is the hook**: the strangest image is already on screen at t = 0. Hook text 0-2 s.
   - Something visibly changes at least every 1.5 s (key pose, camera move, rack focus, glow).
   - Hold key reactions ~0.3 s longer than feels natural; never snap straight back to idle.
   - Every camera move has a reason (reveal, tension, comedy timing): say it in the scene `desc`.
   - **Colour script**: plan it in one line first: set `variant`/`light` per story beat (dusk/day
     for safe or funny, night for mystery, storm + lantern-red `flash` for the scare).
   - **Sound for every visible action**; a silence beat (`music.stops`) before the punchline/scare.
   - Use Ilaw, Mang Oso and Kupas as recurring witnesses/reactors so viewers recognise them.
   - Creatures/props for this legend go in `project-files/custom.py` (see animation-guide),
     built as faceted cut paper with the ONE weird trait made huge. Render a still of each new
     creature and LOOK at it before using it in scenes.
2. **Captions**: start from `timing.captions`, fix names/casing, wrap 1-2 key words per sentence
   in `*stars*` (lantern-red highlight). Max ~26 characters each.
3. **SFX & music** in `project.json` (`python3 ~/pds/tools/audio.py --list`), music `bpm` 76-92.
   **Subscribe CTA (every short):** `"cta": {"s": S, "e": S + 2.6, "tap": 0.95}` with S at
   45-60 % of the video over a calm beat (never in the first 3 s, the payoff, or the last 3 s).
   Add sfx `pop` at S + 0.02 and `ding` at S + tap + 0.1.
4. Build & check:
```bash
python3 ~/pds/tools/lint.py ~/shorts/<slug>      # must say OK - fix every line, re-run
python3 ~/pds/tools/audio.py ~/shorts/<slug>     # mix.wav + mix.mp3
python3 ~/pds/tools/stills.py ~/shorts/<slug> 0.0 T2 T3 T4 --out /tmp/check.jpg
```
Read the stills strip yourself (always include t = 0.0). Look for: actors off their marks,
floating props, heads under captions, muddy night scenes, anything that doesn't read as paper.
**Audience-eye review** before the preview: (1) Would a stranger swiping fast stop at frame 0?
(2) Any stretch > 1.5 s where nothing changes? (3) Any shot that only illustrates the narration
literally? (4) Same face held too long? (5) Does the end cut cleanly back into the start? Fix, re-check.

### Phase 7 — Preview  ⛔ approval required
```bash
python3 ~/pds/tools/render.py ~/shorts/<slug> --preview      # → preview/preview.mp4 (540x960, ~3 min)
```
Send `preview/preview.mp4` with SendUserFile (it plays in the chat). It is made by the same
renderer as the final, at half size. Ask the user to name changes by time or scene number
("at 0:12 make Kupas bark"), or say "approved". Also copy the preview to their computer folder
if one is connected.
**Thumbnails (made at the same time, so no extra waiting):** design 2 NEW thumbnail images.
NEVER use a frame captured from the video: each is its own composition made to sell this short
at phone size.
- A = the "impossible" image (the creature/transformation/weird object, huge);
  B = the strongest emotion (a character's big reaction + the key object). Never give away the twist.
- Compose with the engine so it stays on-model: write a one-scene JSON (`set`, `variant`, `cam`
  zoomed in 1.2-1.5, 1-2 actors with `scale` ~1.0 and an extreme pose, key prop large; creature
  layers via custom.py) and run
  `stills.py <dir> --thumb thumb_A.json --title "2-5 WORDS" --hl KEYWORD --out final/thumbnail_A.png`.
- Scale each to ~200 px wide and LOOK: the idea must read in under a second; the title (top third,
  never over a face) must make someone curious, not repeat the full title.
Send both with the preview and ask: "Which thumbnail, A or B? (or tell me what to change)".
Revisions: change only the scenes named → lint → re-render the preview (for a quick check of one
scene: `render.py <dir> --from S --to E --preview --out /tmp/clip.mp4`) → resend.

### Phase 8 — Final render (only after explicit approval)
```bash
python3 ~/pds/tools/render.py ~/shorts/<slug>      # → final/<slug>.mp4, ~0.7 s per frame (45 s ≈ 13 min)
```
1080×1920, 24 fps, H.264 yuv420p, AAC 192k, -14 LUFS. Run it in the foreground with a long timeout.

### Phase 9 — QA, then deliver
```bash
python3 ~/pds/tools/qa.py ~/shorts/<slug> ~/shorts/<slug>/final/<slug>.mp4
```
All lines must PASS. Open `scenes/contact_sheet.jpg` and check: same character designs in every
shot, captions readable and not on faces, nothing cut off, no empty/odd frames. Fix → re-render → re-QA.
Re-render the chosen thumbnail from its JSON (in case anything changed) as
`final/<slug>_thumbnail.png`, plus a 1280×720 version `final/<slug>_thumbnail_16x9.png` (same art,
title kept inside the frame).
Deliver: send the MP4 AND the thumbnail(s) with SendUserFile; one line on how to use it (YouTube
app → when uploading the Short, tap the cover → add from gallery). If a folder on their computer is
connected, copy the whole project there (`<folder>/<slug>/final/<slug>.mp4`).
**Upload text (ready to copy, also saved to `final/<slug>_upload.txt`):**
- **Title = a hook.** Lead with the strangest/scariest/funniest idea in the first 3-5 words; never
  start with the series name, "The Legend of…", a greeting or a date. ≤ 45 characters (60 max); the
  searchable word (creature name, "Filipino folklore") in the first 40 when it doesn't spoil the twist.
  Write 5 options using at least 3 patterns: Warning · Wrong assumption · Second person · Impossible
  fact · Mini-story · Precise question. Title, thumbnail text and first line make the SAME promise
  with DIFFERENT words; never reveal the twist. Max one CAPS word, max one emoji (at the end), no "!!!".
  Score each /10 on: stops the scroll · clear in 1 second · makes you need the answer · honest to the
  video. Show a small table, mark your pick, say why in one line.
- **Description:** first 1-2 lines are the hook, then 2-3 short lines of true context (checked on
  the web; mention a source or "versions differ by region"), a comment question that invites an
  answer, then 3-5 hashtags (always #shorts, plus topic tags like #philippines #folklore).
- **Series name** at the END of the title only if the total stays ≤ 60, otherwise in the first
  line of the description.
- **Upload settings:** Audience: normally "No, it's not made for kids" (teen/adult tone; answer
  honestly). Altered/synthetic content = No (fully animated). Use only the synthesized music.
- **Cross-post:** also Facebook Reels (monetization is open in the Philippines; TikTok's Creator
  Rewards is not).
Put each title and the description in its own code block.
**Growth notes (one or two lines, only when useful):** after every 8-10 Shorts, offer a
long-form compilation (long-form pays far better for PH viewers). At the start of a new short, ask
once for the last one's "Stayed to watch" % (YouTube Studio → the Short → Analytics) and compare it
with their own earlier Shorts, not a universal target.
One line of notes + offer the next idea. Update nothing in this skill unless the user asks.

## Series identity (set once, then reuse)
The first time, propose 2-3 series names that fit the paper/lantern look (different from the
pastel series) and let the user pick; then keep the same name, title end-tag, hook-text style and
thumbnail look for every short.

## Avoid "inauthentic / mass-produced" content (YouTube policy, July 2025)
Every short needs its own story shape, new scenes, at least one new creature/prop or location
change, and a fresh ending — never reuse a previous short's scene list with names swapped.
Vary formats (Creature card, Story, "Myth vs fact") and sets/variants.

## Hard rules
1. Phases in order; never skip ⛔ approvals; never animate before the voice-over; never
   final-render before preview approval.
2. Original characters and sets only; nothing from the reference films or from pastel-toon-shorts.
3. Preview and final come from the same renderer; never fake the preview with stills.
4. Music/SFX must never compete with the voice (levels in production-guide).
5. Automate: the user never types terminal commands.
6. No new installs without asking. Keep it simple, buildable, testable.
