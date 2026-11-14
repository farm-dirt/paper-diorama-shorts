---
name: "paper-diorama-shorts"
description: "Personal animation studio for vertical YouTube Shorts in a handmade paper-diorama style (cut-paper miniature sets, original cast). Use when the user wants to make, script, preview or render a paper-style animated Short."
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
Do NOT list categories or ask. The paper channel's niche (user's choice, 13 Nov 2026) is **Greek
mythology retold as stories**: gods, monsters and heroes (Zeus, Polyphemus, Hercules, Medusa,
Sisyphus, Midas…) told as a dramatic mini-story with a twist ending. It replaces "Where Myths Came
From" (real origins of myths). The user knows retellings are crowded and chose them anyway: the
paper look, clear storytelling and a fresh angle are how this channel stands out. Famous myths are
welcome (user rule, 14 Nov 2026: "they're famous for a reason" - people already search for them).
Philippine creatures/legends belong to the pastel channel, so don't pitch them here.
Say in one line "Category: Greek mythology stories" and go to Phase 3. Use another category only
if the user names one.

### Phase 3 — 10 ideas  ⛔
10 original ideas (avoid topics the user already made shorts about, in this or the pastel
series), each with **title, 1-2 line description, the hook (first 2 seconds), storytelling
potential (★1-5 + why), why it suits the paper look (which set, light, what folds/glows/moves),
format (Object card 20-30 s or Story 40-55 s), audience fit (teen/adult tone)**. Flag your top 2.
Facts must be true: search the web for every idea before pitching it, check the main numbers on a
primary or reputable source (museum, government, encyclopedia), and flag anything disputed ("accounts
differ") instead of pitching it as fact.
**What wins in this niche:** frame 0 shows the god, monster or hero mid-moment (a Cyclops in his
cave, Zeus with a thunderbolt, Death in chains), with stakes clear with the sound off. **Mix famous and lesser-known (user rule, 14 Nov 2026):** every list of 10 has about 5
FAMOUS myths (Medusa, Icarus, Pandora, Prometheus, the Trojan Horse, Orpheus, Persephone,
Hercules's labours, King Midas's gold touch, the Minotaur, Narcissus, Arachne…) and about 5
lesser-known stories (Arion, Perdix, Melampus, Salmoneus…). Why: famous myths have built-in search
demand and viewers who already care; lesser-known ones have less competition. A famous myth must
still bring ONE thing most viewers don't know, taken from the ancient source (a skipped part, a
surprising detail, what happened next, a different version), stated in the idea card as "Fresh
angle:". Never pitch a famous myth told exactly the usual way. The twist ending is a detail
taken from the ancient source itself (Homer, Hesiod, Ovid, Apollodorus, Pausanias…), never
invented. Mix the types in every list: monsters, gods behaving badly, clever mortals tricking
gods, transformations, love stories gone wrong, punishments. Greek myths have many versions:
name the source you follow ("in Ovid's version…") and say "accounts differ" when they do; never
present one version as the only one. Avoid repeating the shape of the last short (e.g. two
"punished by a god" endings in a row). The paper style shines here: big cut-paper monsters and
gods, sea, caves, temples, storm light and lantern light, transformations as folds and tears.
Every idea must fit the series name.
**Entertaining first (user rule, 14 Nov 2026):** pitch the FUN myths, not the dry or purely sad
ones. Favour stories with a con, a trick, an absurd detail, a god acting petty or silly, a
ridiculous punishment, a clever escape or a gross/shocking twist (Prometheus's bone trick, Salmoneus
faking thunder with pots, Melampus warned by gossiping woodworms, Midas's donkey ears). Each idea
card gets **Entertainment ★1-5 + why** (would a teen laugh, gasp or say "wait, what?"). Pitch at most
1-2 serious/tragic myths per list, and only with a strange hook. Skip ideas that are mainly a
definition, a family tree or a lesson. The top 2 must be among the most entertaining ideas.
**Crowded-topic check (user rule, Nov 2026):** before pitching, search each idea on YouTube Shorts
with web search. **Never use vidIQ (user rule).** Almost every Greek myth already has Shorts, so
don't drop ideas just for being covered: say plainly how recent the latest Short you found is. For
lesser-known stories, favour ones with no Short in the last 6 months; for famous myths, recent Shorts
are expected, so judge them by how fresh the angle is instead. Flag the top 2 with at least one
famous myth among them when a strong fresh angle exists, both high on Entertainment. Wait for the
user to pick.

### Phase 4 — Script + voice-over (ONE checkpoint)  ⛔
**Single-narrator script rules (research Nov 2026; one voice carries everything, so the script and
the picture must do the work).** Why: the first 2-3 s decide "viewed vs swiped away" (the only gate
YouTube shows you); after that, retention comes from structure, not the voice. YouTube publishes no
weights for loops, shares or CTAs, so those are extras, never the plan.

*Clarity first (user rule, 14 Nov 2026 — the Cyclops script was too compressed to follow).* The
story is about PEOPLE and what happened to them. A viewer who has never heard this myth must be able
to retell it after ONE watch: who was there, what each one wanted, what they did, why, and how it
ended. Clarity beats speed: never cut a word that explains who someone is or why they act.
- **Introduce every person** the first time they appear, in one plain sentence: name + what they
  are + why they matter ("His name was Polyphemus, a one-eyed giant who kept sheep on Sicily.").
  Define every myth word in passing ("a sea nymph, a goddess who lives in the sea"). Max 3 named people.
- **Every action has its reason** said aloud ("He wanted to look handsome for her, so he combed his
  hair… with a rake."). A weird detail without its reason is a riddle, not a joke.
- **Tell what happened in order, with no missing steps.** Who did what to whom, what it caused, and
  what happened to each person at the end. Name the event plainly ("He threw the rock at Acis. Acis
  was crushed."), never only hint at it.
- **No riddle lines.** Every sentence must make sense the moment it is heard, without knowing the
  myth: no cryptic teasers ("Spoiler: someone ends up as a river."), no poetic contrasts that hide
  the fact ("The mountains felt it. Galatea didn't." → "His music shook the mountains. But Galatea
  didn't care.").
- **Eyes-closed test:** the narration alone tells the full story. The picture adds jokes, reactions
  and mood, but never carries a plot fact the narration skips.
- **Twist ending explained:** if it's a real-world fact, say the link plainly ("Towns on that coast
  are still named after him."), not as a puzzle.

*Format.* Shortest length that tells the story CLEARLY: Story 40-60 s, Creature card 20-30 s. If the
clear version needs more words, take the extra seconds; never squeeze it into fragments.
Word budget ≈ 2.5 words/s minus silent beats: 30 s ≈ 65-70 words, 45 s ≈ 95-105, 55 s ≈ 120-130, 60 s ≈ 135-145.
Write the script as numbered beats: `[time] VO line | VISUAL | TAG/ON-SCREEN TEXT (≤5 words or none) |
SFX/MUSIC`. Template sections from `content-playbook.md` still apply.

*Write in this order:* first a plain 4-6 sentence summary of what happened (who, wanted what, did
what, why, how it ended) → last line → hook → foreshadow → body. Every step of the summary must be
spoken in the body. One main character, one goal, one problem; others only as needed.

*Hook (0-3 s).* Line 1 = a specific, absurd or scary subject + stakes, said in ≤ 2.5 s (6-10
words), starting mid-moment. No greeting, no "Did you know", no "Long ago in a village…". Plan the
FIRST FRAME before the words: it must sell the premise with the sound off. Frame, 2-4 word hook tag
and spoken line use the SAME key nouns. Concrete beats vague: a year, a number, a name.

*Foreshadow (3-6 s).* Line 2 promises the payoff or asks the question the story answers ("And the
only thing that died… was the pig." / "So why do lolas still avoid that tree?"). It must be clear on
its own, not a riddle. The ending must pay off exactly this — a hollow promise loses viewers and
YouTube's satisfaction surveys.

*Body.* Chain every beat with "But…" or "So… / Which meant… / That's when…", never "and then";
cut any beat the previous one didn't cause. A re-hook every 5-10 s (reversal, stakes jump, withheld
answer, "But that wasn't the weird part."), each marked for a camera move + sound hit. Max two new
names/facts before the next story beat; 5th-grade words; define any Filipino/old term in passing.
Sentences mostly 8-15 words, full sentences that say who did what, easy to say aloud; at most 2-3
short punch lines in the whole short, and only where the sentence before already explained the
situation. No stacked clauses. Never signal the end ("finally", "so that's the story") before the payoff.

*Memorable lines (cinematic, but clear first; user rule, 14 Nov 2026).* Goal: tell what happened, and make the
viewer feel why it mattered.
- 2 memorable lines per script, 3 at most: one at the biggest turning point or climax, one as the
  last line. These ARE the "2-3 short punch lines" allowed above, not extra ones.
- Fact first, feeling second. A memorable line comes right AFTER the plain sentence that says what
  happened; it never replaces it. ("The wax melted, and Icarus fell into the sea." → "That sea still
  carries his name.") It must make sense the moment it is heard by someone who doesn't know the
  myth. The no-riddle rule always wins.
- The hook stays concrete (subject + stakes). Never make line 1 poetic.
- Find the line by answering first, in one line each: what did the main character want, what did it
  cost, what did they get wrong? Build it from contrast, irony (what they wanted vs what they got)
  or a reversal.
- Plain words, 15 words or fewer, easy for an AI voice: no rare words, no stacked metaphors. One run
  of three short sentences is allowed, at the climax only.
- True to the source. Never state a feeling, thought or quote the source doesn't give as if it were
  fact. Use what the source says, or mark your reading ("Maybe…", "Ovid never says what he felt.").
- Ending = the last shot of a film. The second-to-last line states the foreshadowed payoff as a plain,
  true fact from the source ("But Zeus hid fire from humans."). **The LAST line is an original,
  quotable aphorism (user rule, 14 Nov 2026)** in the style of famous lines ("So it goes.", "Hell is
  other people.", "To be, or not to be…"): a short universal truth that grows out of what just
  happened and also applies to the viewer's life ("Some wins are just punishments… that haven't
  arrived yet."). Rules: ≤ 12 words; plain words an AI voice says easily; built on contrast, reversal
  or a balanced two-part shape; one "…" pause allowed; never copy or paraphrase a real famous quote;
  never say "the lesson is" or preach (it states a truth, it doesn't give advice to the viewer); true to
  the story's events. In the script message, offer 4-5 last-line options with your pick and why;
  the user chooses. No "and that is the story of…".

*Narrator persona (pick one per short, by the story's mood; say which in the script message).* Talk like telling a friend: deadpan understatement
for weird/funny legends, low conspiratorial storyteller for scary ones, calm and serious for tragic myths (Icarus, Orpheus:
slower pace, no jokes in the narration, the feeling comes from the memorable lines and the silences). Jokes come from timing,
contrast and the picture — AI voices test as less funny than humans, so never rely on the voice
"acting" a joke.

*Show, don't narrate (for jokes and feelings, never for plot).* The narrator gives who, what, why,
stakes and reported speech ("The ferryman said one word. No."); the picture adds the joke or scare on
top. Mark at least 2 beats where the picture adds a joke or reaction the narration doesn't (never a
plot fact), and write a 0.5-1 s
VO silence ("…" or a line break) after each setup line for the reaction shot + foley hit. Before
the big reveal: music drops out → silence beat → reveal line → sting.
- **Narration is the ONLY voice (user rule).** Never ask the user to record character lines or use a
  second voice, and never set `talk` on an actor. To keep the cast alive, write 1-3 short in-character
  lines (1-5 words, e.g. Ilaw's "Lolo?", Mang Oso's "Huwag.") as **silent torn-paper tags** on screen
  (a project `overlays` list drawn in `custom.py` with the same `caption_img` paper label, placed near
  the speaker and below the caption band), timed to the matching narration beat. Mark them in the
  script as "Tag:" so the user knows they are text, not audio.
- **Ending.** Deliver the foreshadowed payoff + a twist as plain fact, then the aphorism last line
  (see Memorable lines), then STOP: no recap, no outro, no spoken CTA. A loop (last line incomplete or a question that line 1 answers, last frame matching frame 0)
  only if it doesn't weaken the twist. The CTA stays the silent mid-video paper subscribe tag.
- **Tone for teens/adults** (witty or spooky, "folklore explained"); frame folklore as "the legend
  says…" and note regional versions; every factual claim checked on the web.
- **Variety (YouTube "inauthentic content" policy names narrated stories that differ only on the
  surface):** change the hook type, twist type and structure from the previous short, not just names.
- **Self-check before sending:** (1) Retell test: read only the narration as a stranger who never
  heard the myth: can you say who each person is, what they wanted, what happened and why? Any gap →
  add the missing sentence. (2) Every person introduced; every myth word defined; every action has
  its reason. (3) No line that only makes sense later. (4) Word count fits the length; line 1 ≤ 10
  words; a re-hook in every 10 s window; no "and then"; 2+ picture-only joke/reaction beats; 1-3
  tags; last line is an original aphorism ≤ 12 words, right after the plain payoff fact. (5) 2-3 memorable lines, each right after its plain fact. (6) Delete each
  memorable line in your head: the story must still be complete, and the feeling must drop; if
  nothing drops, the line is decoration, so cut it. (7) Any feeling or quote not in the source is
  marked as interpretation. Fix, then send. Send the 4-6 sentence summary above the script so the
  user can check the story at a glance.
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
   - **YouTube Shorts safe zone (user rule, Nov 2026).** The Shorts app draws its buttons and text
     ON TOP of the video, so anything important there is hidden. On the 1080×1920 screen (after the
     camera move), keep every face, the key creature/prop/clue, hook text, tags and the CTA inside the
     **safe box x 48-888, y 180-1500**. No-go areas: the **right 192 px** (x > 888: like, dislike,
     comment, share, remix buttons), the **bottom 420 px** (y > 1500: title, channel name, Subscribe,
     audio), the **top 180 px** (y < 180: search and menu icons). Treat y 1250-1500 as a caution strip
     (long titles grow into it): no faces or reveal objects there. Only set scenery, water, ground, feet
     and blurred foreground may run into the no-go areas. Practical: don't put the main speaker or the
     reveal object on mark R (x 830-860 spills past 888) unless the camera pans it back inside; for
     ground-level objects (a skull on the floor, a fossil in the dirt) raise them, zoom in or tilt the
     camera (`pan_y` positive) so they sit above y 1250.
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
3. **SFX & music** in `project.json` (`python3 ~/pds/tools/audio.py --list`).
   **Music: use a recorded track by default (user's library, 14 Nov 2026)** from `~/pds/assets/music/`:
   `"music": {"track": NAME, "start": S, "stops": [[a, b]]}` (short tracks loop; ducking + stops still
   apply). Pick by the story's mood: `greek_folk` (light/adventurous myths, default), `celtic_harp`
   (sad/tender), `calm_ambient` (neutral), `medieval_ambient` (kings, palaces), `dark_mystery_piano`
   (secrets, crimes), `cinematic_tension` (danger, plots, chases), `epic_action` (battles, gods
   fighting), `dark_fantasy_synth` (underworld, curses), `dark_ambient` (eerie night),
   `horror_atmosphere` (scary myths). Say which track and why in the shot plan. Use the synth bed
   (`bpm` 76-92, no `track`) only for comedy shorts or if the folder is missing.
   **Recorded sounds (user's own library, saved in the engine repo 14 Nov 2026)** live in
   `~/pds/assets/sfx/` (any WAV/MP3; used by file name; list them with `audio.py --list`):
   - Paper: `paper_rip` (tearing big things), `paper_tear` (short tear, reveals, gags), `paper_rustle`
     (paper movement, hands, rummaging - cut with `dur`), `page_flip` (scene or time change).
   - Hits & stings: `impact_hit` (big hit, reveal), `impact_boom` (short boom on a cut), `low_hit`
     (heavy cinematic thump), `deep_boom` (huge moment, god's power), `trailer_boom` (the single
     biggest moment - cut with `dur`), `suspense_sting` (before/at a scare or twist),
     `riser` (build-up into a reveal - start it so it ENDS on the reveal).
   - Whooshes: `whoosh_cinematic` (fast moves, camera swings, throws).
   - Magic: `magic_sparkle` (transformations, gods' magic - cut with `dur`), `sparkle_whoosh`
     (magic movement, a god arriving), `bell` (magic, transformation, reveal sting).
   - Comedy / UI: `falling_whistle` (cartoon fall - cut with `dur`), `pop` (recorded pop: CTA, signs,
     tags; the synth one is `pop_synth`).
   - Action: `sword_clash`, `rocks` (boulders, cliffs, rubble), `water_splash` (jumps, sea), `thunder`
     (Zeus, storms), `door_creak` (doors, curtains, secret reveals), `footsteps_gravel` (walking - cut with `dur`).
   - Creatures/body: `monster_growl`, `heartbeat` (tension - cut with `dur`).
   - Ambience (quiet: `gain` 0.3-0.5, always `dur` + `fadeIn`/`fadeOut`):
     `wind_howl` (storm, strong night wind), `fire_crackle` (lantern/hearth/campfire scenes),
     `night_ambience` (spooky night), `horror_drone` (dread under a scary scene).
   **Banned sounds (user rule, 14 Nov 2026): never cue `wind` or `dark_click`**, even though the
   files are still in `assets/sfx/`. The user found `wind` a low rumble and `dark_click` a tumbling
   sound (heard under the Icarus short's scene 2). Before the preview, check `project.json` and remove
   any cue with either name.
   Prefer recorded sounds over synth ones whenever they fit: they make
   the paper world feel real. Cue options: `{"t", "name", "gain", "dur", "fadeIn", "fadeOut"}`. If
   `--list` shows no recorded sounds, run `git -C ~/pds pull`; if still none, tell the user.
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
floating props, heads under captions, muddy night scenes, anything that doesn't read as paper,
and any face, key object or text outside the safe box (x 48-888, y 180-1500; halve the numbers on
a `--k 0.5` strip). Fix by moving the actor/prop or the camera, then re-check.
**Audience-eye review** before the preview: (1) Would a stranger swiping fast stop at frame 0?
(2) Any stretch > 1.5 s where nothing changes? (3) Any shot that only illustrates the narration
literally? (4) Same face held too long? (5) Does the end cut cleanly back into the start? (6) Would
the YouTube buttons or title cover a face, the reveal or any text in any shot? Fix, re-check.

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
Tell the user: press ▶ (it loops like a Short), ⛶ Full screen (or double-click / F), "Play this scene"
to loop one scene. The video stays still while the scene list scrolls; click any scene card to jump the
video there. While watching, press **⏱ Mark** (or the M key; it also works in full screen) at any moment
that needs a fix: marks show as red ticks on the timeline and as chips on their scene card (click a chip
to go back to it, ✕ to remove) and are sent with the notes. Type change requests in the boxes, then press **Send notes to Claude** or
**✓ Approve** and just type **"check"** in the chat. A page cannot message the chat by itself, so
never promise that the buttons process on their own.
**When the user says "check"** (or "done", "sent"): read `feedback/latest` with db_get on the
preview's slug and act on its `text`: kind `notes` → do the revisions; kind `approve` → Phase 8
(with the thumbnail they named, or ask A/B in the same reply). If it is missing or older than their
last message, the page fell back to copying: ask them to paste the text instead.
**Marks in the feedback** look like `Scene 5 (…) [marked at 12.34 s]: note`. Render a still at each
marked time and LOOK at it before changing that scene. A mark with no note ("marked, no note yet")
means "something is off here": look at that exact moment, say in one line what you think is wrong,
fix it if it's clear, otherwise ask.
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
- Thumbnails follow the same safe box: main subject inside x 48-888, nothing important below y 1500
  (the Shorts shelf and feed draw the title over the bottom).
- Scale each to ~200 px wide and LOOK: the idea must read in under a second; the title (top third,
  never over a face) must make someone curious, not repeat the full title.
Ask together with the preview link: "Which thumbnail, A or B? (or tell me what to change)".
Send both thumbnails with SendUserFile together with the preview link.
Revisions: change only the scenes named → lint → build_preview → republish the same artifact. For a
quick moving check of one scene you may also render just that range:
`render.py <dir> --from S --to E --preview --out /tmp/<slug>-scene<N>-tinylore.mp4` and send it with SendUserFile.
**Every MP4 sent to the user carries the channel tag `-tinylore` (user rule)**: finals, test clips, re-renders.

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
**Name the final video `<slug>-tinylore.mp4` (user rule, every short):** once QA passes, run
`mv ~/shorts/<slug>/final/<slug>.mp4 ~/shorts/<slug>/final/<slug>-tinylore.mp4`. That is the file you
send and copy. (If you re-render later, the engine writes `<slug>.mp4` again: re-QA it, then rename again.)
Deliver: send `final/<slug>-tinylore.mp4` AND the thumbnail(s) with SendUserFile; one line on how to use it (YouTube
app → when uploading the Short, tap the cover → add from gallery). If a folder on their computer is
connected, copy the whole project there (`<folder>/<slug>/final/<slug>-tinylore.mp4`).
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
  honestly). Altered/synthetic content = No (fully animated). Music/SFX come from the engine's
  synth or the user's own library in assets/ (the user downloaded these themselves; if YouTube ever
  flags a track, tell the user which track it was and swap it).
- **Cross-post:** also Facebook Reels (monetization is open in the Philippines; TikTok's Creator
  Rewards is not).
Put each title and the description in its own code block.
**Growth notes (one or two lines, only when useful):** after every 8-10 Shorts, offer a
long-form compilation with new linking narration (not a raw stitch). Why: from 1 Feb 2027 YouTube
pays Shorts ad revenue only to channels with 10M qualified Shorts views per 90 days, so Shorts are
the shop window and long-form + Facebook Reels are where this channel earns. At the start of a new short, ask
once for the last one's "Stayed to watch" % (YouTube Studio → the Short → Analytics) and compare it
with their own earlier Shorts, not a universal target.
One line of notes + offer the next idea. Update nothing in this skill unless the user asks.

## Series identity (set: "Tiny Olympus")
Working series name **Tiny Olympus** (13 Nov 2026; replaces "Where Myths Came From" — change it if
the user picks another). Keep it in every short: as the title end-tag only if the title stays ≤ 60
characters, otherwise as a line in the description ("Tiny Olympus — Greek myths in paper."); same
torn-paper hook-tag style and thumbnail look (cream title with dark outline, one yellow word) every
time. Hashtags: #shorts #greekmythology #mythology plus the main character (e.g. #zeus #cyclops).

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
7. **Engine changes must reach GitHub in the same session (user rule, 14 Nov 2026).** Every new short
   downloads the engine fresh from GitHub, so a change made only in this session's copy (preview page,
   tools, assets) is lost next time ("it always goes back to the old version"). After any engine change:
   commit as farm-dirt, attach the repo with add_repo (access: push), push, then verify with a fresh
   `git clone --depth 1` that the change is there. Edits to this SKILL.md go through propose_skills.