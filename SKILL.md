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
Do NOT list categories or ask. The paper channel's niche is **Things People Actually Invented**:
weird-but-true history — strange real inventions, plans, laws, wars, stunts and events people
actually made or did (e.g. the 1859 Pig War). Philippine legends belong to the pastel channel, so
don't pitch them here. Say in one line "Category: Things People Actually Invented" and go to
Phase 3. Use another category only if the user names one.

### Phase 3 — 10 ideas  ⛔
10 original ideas (avoid topics the user already made shorts about, in this or the pastel
series), each with **title, 1-2 line description, the hook (first 2 seconds), storytelling
potential (★1-5 + why), why it suits the paper look (which set, light, what folds/glows/moves),
format (Object card 20-30 s or Story 40-55 s), audience fit (teen/adult tone)**. Flag your top 2.
Facts must be true: search the web for every idea before pitching it, check the main numbers on a
primary or reputable source (museum, government, encyclopedia), and flag anything disputed ("accounts
differ") instead of pitching it as fact.
**What wins in this niche:** one absurd, instantly readable thing that can fill frame 0 (a pig vs
warships, a spy cat, a bucket two cities fought over) + a specific number or date + a twist the
viewer doesn't see coming. Mix the types in every list: at least 3 real inventions/devices, 3
events/wars/plans gone wrong, and a few "the famous story is a myth" reveals. Avoid repeating the
shape of the last short (e.g. "army loses to animals" twice in a row) and anything already made in
the pastel series (Emu War etc.). Avoid tragedies with real deaths as comedy; give those a respectful
tone or skip them. The paper style shines on tiny machines, maps, night scenes, lantern light,
things that unfold or tear, and reveals by rack focus. Every idea must fit the series name. Wait
for the user to pick.

### Phase 4 — Script + voice-over (ONE checkpoint)  ⛔
**Single-narrator script rules (research Nov 2026; one voice carries everything, so the script and
the picture must do the work).** Why: the first 2-3 s decide "viewed vs swiped away" (the only gate
YouTube shows you); after that, retention comes from structure, not the voice. YouTube publishes no
weights for loops, shares or CTAs, so those are extras, never the plan.

*Format.* Shortest length that tells the story with zero slack: Story 30-55 s, Creature card 20-30 s.
Word budget ≈ 2.5 words/s minus silent beats: 30 s ≈ 65-70 words, 45 s ≈ 95-105, 55 s ≈ 120-130.
Write the script as numbered beats: `[time] VO line | VISUAL | TAG/ON-SCREEN TEXT (≤5 words or none) |
SFX/MUSIC`. Template sections from `content-playbook.md` still apply.

*Write in this order:* last line → hook → foreshadow → body. One character, one goal, one problem.

*Hook (0-3 s).* Line 1 = a specific, absurd or scary subject + stakes, said in ≤ 2.5 s (6-10
words), starting mid-moment. No greeting, no "Did you know", no "Long ago in a village…". Plan the
FIRST FRAME before the words: it must sell the premise with the sound off. Frame, 2-4 word hook tag
and spoken line use the SAME key nouns. Concrete beats vague: a year, a number, a name.

*Foreshadow (3-6 s).* Line 2 promises the payoff or asks the question the story answers ("And the
only thing that died… was the pig." / "So why do lolas still avoid that tree?"). The ending must pay
off exactly this — a hollow promise loses viewers and YouTube's satisfaction surveys.

*Body.* Chain every beat with "But…" or "So… / Which meant… / That's when…", never "and then";
cut any beat the previous one didn't cause. A re-hook every 5-10 s (reversal, stakes jump, withheld
answer, "But that wasn't the weird part."), each marked for a camera move + sound hit. Max two new
names/facts before the next story beat; 5th-grade words; define any Filipino/old term in passing.
Sentences mostly 6-12 words, easy to say aloud; 2-4 word punch lines on reversals; no stacked
clauses. Never signal the end ("finally", "so that's the story") before the payoff.

*Narrator persona (pick one per series, keep it).* Talk like telling a friend: deadpan understatement
for weird/funny legends, low conspiratorial storyteller for scary ones. Jokes come from timing,
contrast and the picture — AI voices test as less funny than humans, so never rely on the voice
"acting" a joke.

*Show, don't narrate.* The narrator gives cause, stakes and reported speech ("The ferryman said
one word. No."); the picture delivers the joke or scare. Never narrate an emotion the face shows.
Mark at least 2 beats where the picture says something the narration doesn't, and write a 0.5-1 s
VO silence ("…" or a line break) after each setup line for the reaction shot + foley hit. Before
the big reveal: music drops out → silence beat → reveal line → sting.
- **Narration is the ONLY voice (user rule).** Never ask the user to record character lines or use a
  second voice, and never set `talk` on an actor. To keep the cast alive, write 1-3 short in-character
  lines (1-5 words, e.g. Ilaw's "Lolo?", Mang Oso's "Huwag.") as **silent torn-paper tags** on screen
  (a project `overlays` list drawn in `custom.py` with the same `caption_img` paper label, placed near
  the speaker and below the caption band), timed to the matching narration beat. Mark them in the
  script as "Tag:" so the user knows they are text, not audio.
- **Ending.** Deliver the foreshadowed payoff + a twist, then STOP: last line ≤ 15 words, carries a
  surprising, quotable, true fact (that's what gets shared), no recap, no moral, no outro, no spoken
  CTA. A loop (last line incomplete or a question that line 1 answers, last frame matching frame 0)
  only if it doesn't weaken the twist. The CTA stays the silent mid-video paper subscribe tag.
- **Tone for teens/adults** (witty or spooky, "folklore explained"); frame folklore as "the legend
  says…" and note regional versions; every factual claim checked on the web.
- **Variety (YouTube "inauthentic content" policy names narrated stories that differ only on the
  surface):** change the hook type, twist type and structure from the previous short, not just names.
- **Self-check before sending:** word count fits the length; line 1 ≤ 10 words; a re-hook in every
  10 s window; no "and then"; 2+ picture-only beats; 1-3 tags; last line ≤ 15 words. Fix, then send.
**Voice-over direction (ElevenLabs; v4 preferred, v3 syntax works):** choose a voice whose natural
range fits the series persona (it matters more than any setting); on v3 use stability Natural or
Creative. No SSML `<break>` tags: use "…" for a weighted pause, a line break between beats, commas
for breath, CAPS on at most 1-2 words per short. At most ONE audio tag per beat ([whispers],
[sighs], [short pause], [long pause], [curious], [sarcastic]); describe the quality if needed
("[low, conspiratorial voice]"). Respell hard Filipino/Spanish names in script.txt (or IPA on v4)
and list pronunciations under the script. Tell the user to regenerate any line that sounds flat and
keep the best take. Suggest once that their own voice would stand out.
Save `script/script.md` (full) and `script/script.txt` (narration only, exactly as spoken). Send
ONE message: the script, the narration in a code block ready to copy, short voice-over
instructions (MP3/WAV, read exactly, small pauses between sentences). End with:
"Record it and upload the file, or tell me what to change in the script."
Uploading the voice-over counts as approving the script. The voice-over is ONE file with only the
narrator; never ask for extra voice clips. If they changed words while recording,
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

### Phase 7 — Browser preview  ⛔ approval required
```bash
python3 ~/pds/tools/build_preview.py ~/shorts/<slug>   # renders final/<slug>.mp4 at full 1080x1920 + preview/ page (light web copy, thumbs), ~11 min for 60 s
```
The preview IS the final render at full size (the user found the old half-size preview blurry), so
run it in the background and poll until it finishes, and never show a `--half` render as the preview.
Copy the preview folder into the working directory (the publisher only attaches files from there),
then publish it with the Artifact tool's publish-from-files: `index.html`, `data.js`, `preview.mp4`,
every `thumbs/scene_NN.jpg`, `assets/Fraunces-Black.woff` (same paths). **Right after the FIRST
publish**, read the declaration and declare `{"db": {}, "user": {}}` on it: that is what lets the
page's buttons save. Republish the SAME artifact (slug + base_version, mode "replace") on every
revision, so the link never changes. Also copy the preview folder to the user's computer if a
folder is connected (opening `index.html` works offline).
Tell the user: press ▶ (it loops like a Short), ⛶ Full screen (or double-click / F), "Play this
scene" to loop one scene, type change requests in the boxes, then press **Send notes to Claude** or
**✓ Approve** and just type **"check"** in the chat. A page cannot message the chat by itself, so
never promise that the buttons process on their own.
**When the user says "check"** (or "done", "sent"): read `feedback/latest` with db_get on the
preview's slug and act on its `text`: kind `notes` → do the revisions; kind `approve` → Phase 8
(with the thumbnail they named, or ask A/B in the same reply). If it is missing or older than their
last message, the page fell back to copying: ask them to paste the text instead.
The preview video is the final render (full size, lighter web copy): never fake it with stills.
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
Ask together with the preview link: "Which thumbnail, A or B? (or tell me what to change)".
Send both thumbnails with SendUserFile together with the preview link.
Revisions: change only the scenes named → lint → build_preview → republish the same artifact. For a
quick moving check of one scene you may also render just that range:
`render.py <dir> --from S --to E --preview --out /tmp/clip.mp4` and send it with SendUserFile.

### Phase 8 — Final video (only after explicit approval)
If the approved preview was built after the last change, `final/<slug>.mp4` is already the final:
go straight to Phase 9. Only if something changed after the last build_preview, re-run
`python3 ~/pds/tools/render.py ~/shorts/<slug>` (background + poll, ~0.45 s per frame).
1080×1920, 24 fps, H.264 CRF 19 yuv420p, AAC 192k, -14 LUFS.

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

## Series identity (set: "Things People Actually Invented")
The user chose the series name **Things People Actually Invented** (Nov 2026). Keep it in every
short: as the title end-tag only if the title stays ≤ 60 characters, otherwise as a line in the
description ("Things People Actually Invented — weird things people actually did."); same torn-paper
hook-tag style and thumbnail look (cream title with dark outline, one yellow word) every time.

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