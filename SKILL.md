---
name: "paper-diorama-shorts"
description: "Personal animation studio for vertical YouTube Shorts in a handmade paper-diorama style (cut-paper miniature sets, original cast). Use when the user wants to make, script, preview or render a paper-style animated Short."
---
<!-- Copy of the live skill as saved in the user's Claude account on 23 Nov 2026. If this file and the
     account version ever differ, the account version wins: copy it here again and push. -->


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
   before installing (pip/official sources only). Exception: the free narrator is pre-approved (user,
   23 Nov 2026): `pip install --break-system-packages kokoro-onnx soundfile` then
   `python3 ~/pds/tools/voice.py --check` (downloads its ~350 MB model once) without asking.
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
Do NOT list categories or ask. The paper channel's niche (user's choice, 23 Nov 2026, modelled on
the *format* of the Facebook page "Mini Philosophy") is **Mini Philosophy: one thinker, one idea,
one everyday problem.** Each Short takes a problem the viewer really has (being insulted,
overthinking, comparing yourself to others, chasing approval, fear of failing, regret, being
ignored, procrastinating, anger, envy…) and answers it with ONE idea from ONE real thinker, told as
a short paper-diorama story. It replaces the Greek-myth niches ("Olympus Drama", "Greek mythology
retold", "Where Myths Came From") and the 18 Nov lawsuit test.
**Why this works (and how it must differ from Mini Philosophy):** that page wins with a real teacher's
face; this channel is faceless, so the STORY and the paper picture do the work instead. Never copy
their reels, titles, topic-thinker pairs or wording: before pitching, check the idea against their
reels (web search "Mini Philosophy [thinker]") and drop exact matches. Avoid the crowded end of the
niche: Stoic-quote slideshows, "Marcus Aurelius said…" over sad music, fake motivational quotes.
**Shape of every short:** (1) hook = the viewer's problem or the thinker doing something that looks
crazy (Diogenes searching with a lamp in daylight) → (2) rewind into the thinker's real moment, told
as a scene in their world (ancient Athens, a Chinese court, a Paris café, a prison cell — the paper
sets shine here) → (3) the idea shown with an everyday object or thought experiment → (4) the turn
back to the viewer's life in one or two plain lines → (5) quotable aphorism last line. Ilaw, Mang Oso
and Kupas play the modern people living the problem; thinkers are new paper characters.
**Accuracy is the selling point:** the idea must be what the thinker actually argued, with the work
named ("in his Letters, Seneca says…"). Quotes said aloud must be verified on a primary or reputable
source (Stanford Encyclopedia of Philosophy, the text itself); many viral philosophy quotes are fake,
so when in doubt paraphrase and say "the story goes" for legends (Diogenes, Thales). Never put words in
a real thinker's mouth.
**Wherever this skill says "myth" or "god", read "the thinker's story and idea" / "the thinker".**
The Clarity, Mystery formula, House voice, Retention playbook and Ending rules all still apply; the
myth-only parts (old-world wording, "Tell the drama" rules, Greek-name respelling) do not, except
respelling hard names (Epictetus as ep-ik-TEE-tus).
**Model script (present tense, ~115 words, ~45 s; Plutarch, *Life of Alexander* 14 / Diogenes
Laertius 6.38; accounts differ):**
```
The most powerful man alive offers him anything. He asks him to move.
It all begins when Alexander the Great, king of half the known world, visits Corinth.
Everyone rushes to impress him. Except one man.
Diogenes, a philosopher who lives in a big clay jar and owns almost nothing, is lying in the sun.
Alexander stands over him. "Ask me for anything you want."
Gold. Land. Power.
Diogenes looks up and says: "Stand a little out of my sunlight."
Alexander's men laugh. Alexander doesn't.
Because Diogenes isn't being rude. You can't buy a man who already has what he needs.
The story goes that Alexander says: "If I weren't Alexander, I'd want to be Diogenes."
The richest man in the room… is the one who needs nothing.
```
Music default for this niche: `calm_ambient` (reflective) or `dark_mystery_piano` (heavier ideas);
`greek_folk` only for ancient-Greek thinkers.
Philippine creatures/legends belong to the pastel channel, so don't pitch them here.
Say in one line "Category: Mini Philosophy (one thinker vs one everyday problem)" and go to Phase 3.
Use another category only if the user names one.

### Phase 3 — 10 ideas  ⛔
**Problem first, thinker second (user rule, 23 Nov 2026).** Every idea card opens with the viewer's
everyday problem in their own words ("Someone insulted you and you can't stop replaying it."), then
the thinker + the ONE idea that answers it + the real story moment that shows it.
Rules: (1) **Mix famous and lesser-known:** about 5 famous thinkers people already search for
(Socrates, Diogenes, Seneca, Epictetus, Marcus Aurelius, the Buddha, Confucius, Laozi, Nietzsche,
Camus, Kierkegaard, Plato…) and about 5 lesser-known ones (Zhuangzi, Montaigne, Simone Weil,
Epicurus, Hypatia, Boethius, Mencius, Hannah Arendt, Iris Murdoch…); a famous thinker still needs a
**Fresh angle:** (an idea or story most viewers don't know, not "memento mori" again); (2) the
problem must be one a US teen or adult has THIS WEEK (school, work, phones, friends, family, money,
self-worth), never an abstract "what is truth?"; (3) the idea must come with a real story moment or
a concrete thought experiment the paper world can show (Diogenes and Alexander, Socrates drinking the
hemlock, Zhuangzi's butterfly dream, Epictetus's broken leg, Boethius writing in prison) — an idea
with nothing to SHOW is not pitched; (4) **Relatable ★1-5** (would a viewer think "that's me"?) and
**Surprise ★1-5** (does the answer flip what they expected?); drop any idea under ★4 on either; (5)
never a list of quotes, never preaching: the story answers the problem, the viewer draws the lesson;
(6) mix problem types in every list (people, self, work, fear, loss, success) and avoid repeating the
last short's thinker or problem. The top 2 must have the highest Relatable + Surprise totals.
10 original ideas (avoid topics the user already made shorts about, in this or the pastel
series), each with **the problem, thinker + idea + source work, title, 1-2 line description, the hook
(first 2 seconds), the story moment or object that SHOWS the idea, why it suits the paper look (which
set, light, what folds/glows/moves), length (Story 40-60 s), mystery shape** (the looks-wrong opening,
who doubts or mocks the thinker, and the reversal, a few words each; see "Mystery formula" in Phase 4),
**Relatable ★ / Surprise ★**, and the Mini Philosophy overlap check ("no matching reel found" or what
was found). Flag your top 2.
Facts must be true: search the web for every idea before pitching it, check the main numbers on a
primary or reputable source (museum, government, encyclopedia), and flag anything disputed ("accounts
differ") instead of pitching it as fact.
**Channel data:** the old myth Shorts showed that conflict wins (Trojan Horse 55.5 % stayed to watch,
the town-origin legend lowest at 42.2 %). Carry that over: every philosophy story needs a clash (a
thinker vs a king, a crowd, a judge, their own fear) and a reversal, never a calm lecture. The new
niche starts a fresh baseline: compare its first 3 Shorts with each other, not with the myth Shorts.
**What wins in this niche:** frame 0 shows the thinker or the modern character mid-moment with the
problem readable with the sound off (Diogenes in his jar with a king's shadow over him; Ilaw staring
at a phone full of likes). The paper style shines with lamplight, prison cells, marketplaces,
courts, shadows on a cave wall, ideas shown as folding/unfolding paper.
**Entertaining first:** favour thinkers who did something strange, funny or brave (Diogenes's lamp,
Socrates annoying all of Athens, Thales falling into a well while stargazing, Zhuangzi drumming at
his wife's funeral) over dry theory. At most 1-2 heavy topics (death, grief) per list, and only with
a strong hook.
**Crowded-topic check (user rule, Nov 2026):** before pitching, search each idea on YouTube Shorts
with web search, and check the Mini Philosophy page for the same thinker + idea. **Never use vidIQ
(user rule).** Famous thinkers will have Shorts already: say how recent the latest one is and judge
the idea by how fresh the problem + story pairing is. For lesser-known thinkers, favour ones with no
Short in the last 6 months. Flag the top 2 (at least one famous thinker when a strong fresh angle
exists). Wait for the user to pick.

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
  are + why they matter ("His name is Polyphemus, a one-eyed giant who keeps sheep on Sicily.").
  Define every myth word in passing ("a sea nymph, a goddess who lives in the sea"). Max 3 named people.
- **Every action has its reason** said aloud ("He wants to look handsome for her, so he combs his
  hair… with a rake."). A weird detail without its reason is a riddle, not a joke.
- **Tell what happened in order, with no missing steps.** Who did what to whom, what it caused, and
  what happened to each person at the end. Name the event plainly ("He throws the rock at Acis. Acis
  is crushed."), never only hint at it.
- **No riddle lines.** Every sentence must make sense the moment it is heard, without knowing the
  myth: no cryptic teasers ("Spoiler: someone ends up as a river."), no poetic contrasts that hide
  the fact ("The mountains felt it. Galatea didn't." → "His music shakes the mountains. But Galatea
  doesn't care.").
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

*Mystery formula for Stories (from two viral reference Shorts, user request 15 Nov 2026).* Shape every
Story as a mystery the viewer solves with the narrator, inside the clarity rules above (clarity always wins):
1. **Looks-wrong hook:** line 1 shows a god or mortal doing something that looks crazy, or states something
   that sounds impossible ("Zeus just turned a young woman into a cow." / "King Midas wears a giant hat. Every.
   Single. Day."). It still follows the Hook rules below (concrete, ≤ 10 words, subject + stakes).
2. **Rewind:** line 2 jumps back with "It all begins when…" (present tense; "See, …" also works) and introduces the people involved.
   With a looks-wrong hook, the viewer's "why?" IS the foreshadow; the ending must answer exactly that why.
3. **Stakes**, plain and big, said by ~10 s.
4. **Doubter or detective:** someone suspects, mocks or tries to catch the main character (Hera is the
   natural one). Their words are reported speech or a silent tag, never a second voice.
5. **Low point:** the main character seems to get away with it, or seems doomed.
6. **Clue shown with everyday things:** show the trick or secret in concrete steps a viewer can picture (a
   guard with a hundred eyes, a few always awake; reeds that whisper the secret; a net finer than a
   spider's web). Then say it plainly: the eyes-closed test still applies.
7. **Reversal:** the trick backfires or the doubter is proven right, shown as the most visual moment of the
   short; then the plain payoff fact and the aphorism last line (see Memorable lines), then STOP.
Open each new stretch with a turn line ("But Hera isn't fooled." / "Meanwhile…" / "So what does Zeus do?");
these count as the re-hooks in Body. Creature cards keep their simpler shape.

*Hook (0-3 s).* **Open on the absurd act or bold claim itself, never on setup (channel data, 16 Nov
2026: 45-58 % of viewers swipe away in the first seconds).** Line 1 is the weirdest thing that happens
or its price ("Zeus turns his girlfriend into a cow to hide her from his wife."), not who someone is or
where we are; background comes in line 2's rewind. No slow voice-over build-up. Line 1 = a specific, absurd or scary subject + stakes, said in ≤ 2.5 s (6-10
words), starting mid-moment. No greeting, no "Long ago in a village…". The idea's "Did you know…?" fact IS line 1, but
spoken as a flat statement without the words "Did you know" ("Zeus only became king… because his dad
threw up."). Why: those three words delay the shocking part by about a second, which is when viewers
swipe. "Did you know" may still be used in the idea card, the title or the thumbnail text. Plan the
FIRST FRAME before the words: it must sell the premise with the sound off. Frame, 2-4 word hook tag
and spoken line use the SAME key nouns. Concrete beats vague: a year, a number, a name.

*Foreshadow (3-6 s).* Line 2 promises the payoff or asks the question the story answers ("And the
only thing that died… was the pig." / "So why does King Midas never take off his hat?"). It must be clear on
its own, not a riddle. The ending must pay off exactly this — a hollow promise loses viewers and
YouTube's satisfaction surveys.

*Body.* Chain every beat with "But…" or "So… / Which means… / That's when…", never "and then";
cut any beat the previous one didn't cause. A re-hook every 5-10 s (reversal, stakes jump, withheld
answer, "But that isn't the weird part."), each marked for a camera move + sound hit. Max two new
names/facts before the next story beat; 5th-grade words; define any Greek or old-world term in passing.
Sentences mostly 8-15 words, full sentences that say who did what, easy to say aloud. Short beat
lines (2-5 words: "There's just one problem." / "The gods laugh." / "One job.") are welcome as rhythm, up
to 4-5 per short, but only where the sentence before or after already explained the situation (see
House voice). No stacked clauses. Never signal the end ("finally", "so that's the story") before the payoff.

*Memorable lines (cinematic, but clear first; user rule, 14 Nov 2026).* Goal: tell what happened, and make the
viewer feel why it mattered.
- 2 memorable lines per script, 3 at most: one at the biggest turning point or climax, one as the
  last line. These ARE the "2-3 short punch lines" allowed above, not extra ones.
- Fact first, feeling second. A memorable line comes right AFTER the plain sentence that says what
  happened; it never replaces it. ("The wax melts, and Icarus falls into the sea." → "That sea still
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
  true fact from the source ("But Zeus hides fire from humans."). **The last story line (right before the hard loop cut, see Ending) is an original,
  quotable aphorism (user rule, 14 Nov 2026)** in the style of famous lines ("So it goes.", "Hell is
  other people.", "To be, or not to be…"): a short universal truth that grows out of what just
  happened and also applies to the viewer's life ("Some wins are just punishments… that haven't
  arrived yet."). Rules: ≤ 12 words; plain words an AI voice says easily; built on contrast, reversal
  or a balanced two-part shape; one "…" pause allowed; never copy or paraphrase a real famous quote;
  never say "the lesson is" or preach (it states a truth, it doesn't give advice to the viewer); true to
  the story's events. In the script message, offer 4-5 last-line options with your pick and why;
  the user chooses. No "and that is the story of…".

*Plain modern wording (Mini Philosophy niche, 23 Nov 2026; replaces the old-world wording rule).*
The thinker's story can sound old, but the problem and the turn back to the viewer use everyday
modern words (phone, group chat, boss, likes, test). No philosophy jargon unless defined in passing
in plain words ("Stoics, thinkers who said: control what you can, let go of the rest"). Never say "the
lesson is", "you should" or "this teaches us": the story shows it, the aphorism lands it.

*Present tense (user rule, 15 Nov 2026).* Tell the main action as if it is happening right now ("Zeus sees
her. Then he hears Hera coming. He panics."). Why: it feels live, like watching the gossip unfold, not a
history lesson. Real-world facts after the story keep their real tense ("That sea still carries his
name."); the aphorism last line is timeless. Never switch tense in the middle of a scene. Clarity rules
still win.

*House voice (user's model script, 16 Nov 2026 — write EVERY script in this style).* The narrator is a
witty friend telling gossip, not a teacher. Copy these moves:
- **3-part hook, price first:** the huge lifelong price / the one small mistake / who he was ("He's
  cursed to scream at every sunrise. Because he fell asleep just ONCE. He was once a warrior.").
  Line 1 ≤ 10 words and never a who-he-is setup line (the old "He was once a warrior." opener is
  retired: setup first loses viewers, channel data 16 Nov 2026).
- **Rewind** with "It all begins when…"; introduce each god as name + plain role ("Ares, god of war").
- **Stack problems:** "There's just one problem." then "And [someone] sees everything…" — each new
  problem is a new re-hook.
- **Dry asides** that add personality, never new plot: "…and isn't exactly good at keeping secrets." /
  "…but his anger needs somewhere to go."
- **Short beat lines** between full sentences: "One job." / "But he falls asleep." / "The gods laugh."
- **Reframe before the end:** "Not to [obvious reason]… but to [the real reason from the source]."
- **Last line** in a punchy two-part shape, often with one modern, funny word: "One nap. An eternity of
  alarm clocks." It still follows the aphorism rules (≤ 12 words, original, true to the story).
- Present tense for the story; the hook may use past for who he WAS and present for the curse NOW.
Model script (present tense, ~175 words, ~65-70 s):
```
He's cursed to scream at every sunrise. Because he fell asleep just ONCE. He was once a warrior.
It all begins when Ares, god of war, starts secretly visiting Aphrodite, goddess of love.
There's just one problem. She's married to Hephaestus, god of the forge.
And Helios, the Sun god, sees everything... and isn't exactly good at keeping secrets.
So Ares stations a young soldier, Alektryon, outside the chamber.
One job: stay awake and warn Ares before sunrise.
But Alektryon falls asleep.
At dawn, Helios spots them and tells Hephaestus everything.
Enraged, Hephaestus forges a net finer than a spider's web, traps the two, and calls the gods to look.
The gods laugh.
Ares escapes... but his anger needs somewhere to go. So he blames the guard.
He turns Alektryon into a rooster. In Lucian's version, even his helmet crest stays on his head.
So every morning, he crows before the Sun rises.
Not to welcome the day... but to make sure Ares never gets caught again.
One nap. An eternity of alarm clocks.
```
All clarity rules, the word budget and the self-check still apply on top of this voice.

*Narrator persona (pick one per short, by the story's mood; say which in the script message).* Talk like telling a friend: deadpan understatement
for weird/funny legends, low conspiratorial storyteller for scary ones, calm and serious for tragic myths (Icarus, Orpheus:
slower pace, no jokes in the narration, the feeling comes from the memorable lines and the silences). Jokes come from timing,
contrast and the picture — AI voices test as less funny than humans, so never rely on the voice
"acting" a joke.

*Show, don't narrate (for jokes and feelings, never for plot).* The narrator gives who, what, why,
stakes and reported speech ("The ferryman says one word. No."); the picture adds the joke or scare on
top. Mark at least 2 beats where the picture adds a joke or reaction the narration doesn't (never a
plot fact), and write a 0.5-1 s
VO silence ("…" or a line break) after each setup line for the reaction shot + foley hit. Before
the big reveal: music drops out → silence beat → reveal line → sting.
- **Narration is the ONLY voice (user rule).** Never ask the user to record character lines or use a
  second voice, and never set `talk` on an actor. To keep the cast alive, write 1-3 short in-character
  lines (1-5 words, e.g. Hera's "Nice cow.", Zeus's "What cow?") as **silent torn-paper tags** on screen
  (a project `overlays` list drawn in `custom.py` with the same `caption_img` paper label, placed near
  the speaker and below the caption band), timed to the matching narration beat. Mark them in the
  script as "Tag:" so the user knows they are text, not audio.
- **Ending.** Deliver the foreshadowed payoff + a twist as plain fact, then the aphorism last line
  (see Memorable lines) over the spectacle shot, then a hard cut within 0.3 s that loops into frame 0
  (Retention playbook #10; replaces the spoken comment question, 16 Nov 2026). Then STOP: no recap, no outro, no
  subscribe ask. **No end-question tag in the video (user rule, 23 Nov 2026):** never put the pick-a-side
  question, a "Team X or Team Y?" line or any "Tell me below" ask on screen; the last shot shows only the
  picture and its caption. The comment question lives in the description and pinned comment only (see Comment
  driver). Leave ~0.4 s of silence after the aphorism so it still lands. A loop (last line incomplete or a question that line 1 answers, last frame matching frame 0)
  only if it doesn't weaken the twist. The CTA stays the silent mid-video paper subscribe tag.
- **Tone for teens/adults** (witty celebrity-gossip tone, never crude); frame the story as "the myth
  says…" or "in Ovid's version…" and say when accounts differ; every factual claim checked on the web.
- **Variety (YouTube "inauthentic content" policy names narrated stories that differ only on the
  surface):** change the hook type, twist type and structure from the previous short, not just names.
- **Self-check before sending:** (1) Retell test: read only the narration as a stranger who never
  heard the myth: can you say who each person is, what they wanted, what happened and why? Any gap →
  add the missing sentence. (2) Every person introduced; every myth word defined; every action has
  its reason. (3) No line that only makes sense later. (4) Word count fits the length; line 1 ≤ 10
  words; a re-hook in every 10 s window; no "and then"; 2+ picture-only joke/reaction beats; 1-3
  tags; aphorism ≤ 12 words right after the plain payoff fact, then the hard loop cut (no spoken question).
  (10) Retention playbook self-check passes. (5) 2-3 memorable lines, each right after its plain fact. (6) Delete each
  memorable line in your head: the story must still be complete, and the feeling must drop; if
  nothing drops, the line is decoration, so cut it. (7) Any feeling or quote not in the source is
  marked as interpretation. (8) Stories: point to the looks-wrong hook, the doubter, the
  everyday-thing clue and the reversal; if one is missing, fix it or say why this story doesn't need it.
  (9) Main action in present tense, no tense switch mid-scene.
  Fix, then send. Send the 4-6 sentence summary above the script so the
  user can check the story at a glance.
**Voice-over: Claude makes it by default (user rule, 23 Nov 2026).** The engine's free narrator
`tools/voice.py` (Kokoro, open-source, runs here, no credits) reads `script/script.txt` sentence by
sentence with exact pauses, so timing.py snaps cleanly. **Narrator voice: always af_heart** ("heart", a
soft, natural female narrator; user rule, 23 Nov 2026, replaces am_michael) at **Speed 1.0** (heart talks
faster than michael, so 1.0 already gives about 2.8-3 words/s). Use it on every short; never switch voice
unless the user asks. audio.py gives the voice a "narrator polish" automatically (warmth, clearer words,
softer S sounds, even level, a tiny studio room; `mix.voicePolish`, on by default), so never add other
effects to the voice file.
- Hard names: add a respelling to `~/pds/tools/pronounce.json` (engine-wide, commit + push) or
  `project-files/pronounce.json` (one short); test with `voice.py --phonemes "Thaylees"` and read the
  phonemes before rendering ("Thales" alone comes out as one syllable, so it is mapped to "Thaylees").
- Emotion comes from the writing only: "..." for a pause, a blank line between paragraphs, commas for
  breath. Kokoro is calmer than ElevenLabs and won't act a joke; timing and pictures carry the humour.
- Only if the user asks to try other voices: `voice.py --samples OUT_DIR "text" af_heart af_bella am_fenrir am_onyx`,
  send the MP3s, the user picks.
- If the user prefers to record in ElevenLabs instead, use the ElevenLabs notes below and wait for the upload.

**ElevenLabs (only when the user chooses to record; FREE plan, confirmed 15 Nov 2026):**
- **Voice:** one narrator voice on every short so viewers recognise the series. If no voice is named here
  yet, ask the user once which voice the paper channel uses, then keep it. A voice whose natural range
  fits the persona matters more than any setting.
- **Settings (free model sliders):** Speed ≈ 0.90 · Stability ≈ 40-45 % · Similarity ≈ 75 % · Style
  Exaggeration 0-10 % · Speaker Boost on if shown. Give these as a small table with a one-line "why" each.
- **No audio tags** ([whispers], [sighs]…) and no SSML `<break>` tags: free voices may read them aloud.
  Get emotion from the writing only: "…" for a weighted pause, a line break between beats, commas for
  breath, CAPS on at most 1-2 words per short.
- Respell hard Greek names in script.txt ("Persephone" as "per-SEF-oh-nee") and list pronunciations
  under the script.
- Keep the narration short enough to regenerate 2-3 times on free credits; the user can regenerate just
  one bad sentence and upload both files (you splice it in). If takes sound flat, nudge Stability down
  5 %; if they sound weird or random, nudge it up 5 %.
- Suggest once that their own voice would stand out.
Save `script/script.md` (full) and `script/script.txt` (narration only, exactly as spoken). Send
ONE message: the script and the narration in a code block. End with:
"Say OK and I'll make the voice-over, or tell me what to change in the script."
The user saying OK (or uploading their own recording) counts as approving the script. The voice-over is
ONE file with only the narrator; never ask for extra voice clips. If the user records it themselves and
changes words, update `script/script.txt` to match.

### Phase 5 — Make / process the voice-over (starts as soon as the script is approved)
Never build animation before the voice-over exists. Then, without asking:
```bash
python3 ~/pds/tools/new_project.py ~/shorts <slug> "<Title>"
# default: Claude's free narrator
python3 ~/pds/tools/voice.py ~/shorts/<slug>/script/script.txt ~/shorts/<slug>/voice-over/voice.wav --voice af_heart --speed 1.0
# or, if the user recorded it: cp <upload> ~/shorts/<slug>/voice-over/voice.<ext>
# set "voice" in project.json
python3 ~/pds/tools/timing.py ~/shorts/<slug>/voice-over/voice.<ext> ~/shorts/<slug>/project-files/timing.json --script ~/shorts/<slug>/script/script.txt
```
Report in 3-4 lines: duration, sentences matched to pauses, any sentence whose length looks off
(≥ 40 % different from the word-count estimate = misread/skipped line → tell the user).
With Claude's narrator, send `voice-over/voice.mp3` with SendUserFile so the user can hear it, and
keep going with the animation (they can ask for a re-take: another voice, speed, or a name fix).
The voice-over is the master clock: cuts go on real pauses.

### Phase 6 — Build the animation
1. **Shot plan** in `project-files/project.json` (schema + pose library + sets in
   `animation-guide.md`). One scene per phrase/sentence, cut on pauses, 1.2-3.5 s per shot.
   - **Frame 0 is the hook**: the strangest image is already on screen at t = 0.
   - **Hook text in the first 1-3 s (user rule, 23 Nov 2026):** every short gets an on-screen hook label
     (`hook` in project.json) from t = 0 until about 3 s (never shorter than 1 s), so the promise is readable
     even with the sound off. 2-5 words, big tilted torn-paper label in the top third inside the safe box,
     never over a face, using the same key nouns as spoken line 1 and the frame-0 picture (spoken "This rice
     only cooks if nobody makes a sound" + a steaming bowl = hook "*Silent* rice"). It says the strange
     promise, never a title card, greeting or channel name. The spoken hook line must also finish by 3 s.
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
   - Something visibly changes about every 1 s (key pose, camera move, rack focus, glow, new shot
     type); rotate the 5 shot types and plan proof inserts + text props (see Retention playbook).
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
1080×1920, 24 fps, H.264 CRF 19 `-tune animation`, keyframe every 10 s, yuv420p, AAC 192k, -14 LUFS.
(These settings are in render.py: about half the file size of the old 1-s-keyframe setting with the same
or better measured quality; the moving film grain is what makes these files big.)

### Phase 9 — QA, then deliver
```bash
python3 ~/pds/tools/qa.py ~/shorts/<slug> ~/shorts/<slug>/final/<slug>.mp4
```
All lines must PASS. Open `scenes/contact_sheet.jpg` and check: same character designs in every
shot, captions readable and not on faces, nothing cut off, no empty/odd frames. Fix → re-render → re-QA.
Re-render the chosen thumbnail from its JSON (in case anything changed) as
`final/<slug>_thumbnail.png` (vertical 1080×1920 only; no landscape 16:9 version, user rule 14 Nov 2026).
**Name the final video `<slug>-tinylore.mp4` (user rule, every short):** once QA passes, run
`mv ~/shorts/<slug>/final/<slug>.mp4 ~/shorts/<slug>/final/<slug>-tinylore.mp4`. That is the file you
send and copy. (If you re-render later, the engine writes `<slug>.mp4` again: re-QA it, then rename again.)
Deliver: send `final/<slug>-tinylore.mp4` AND the thumbnail(s) with SendUserFile; one line on how to use it (YouTube
app → when uploading the Short, tap the cover → add from gallery). If a folder on their computer is
connected, copy the whole project there (`<folder>/<slug>/final/<slug>-tinylore.mp4`).
**Upload text (ready to copy, also saved to `final/<slug>_upload.txt`):**
- **Title = a hook.** Lead with the strangest/scariest/funniest idea in the first 3-5 words; never
  start with the series name, "The Legend of…", a greeting or a date. ≤ 45 characters (60 max); the
  searchable word (the thinker's name, or the problem: "insult", "overthinking") in the first 40 when it doesn't spoil the twist.
  Write 5 options using at least 3 patterns: Warning · Wrong assumption · Second person · Impossible
  fact · Mini-story · Precise question. Title, thumbnail text and first line make the SAME promise
  with DIFFERENT words; never reveal the twist. Max one CAPS word, max one emoji (at the end), no "!!!".
  Score each /10 on: stops the scroll · clear in 1 second · makes you need the answer · honest to the
  video. Show a small table, mark your pick, say why in one line.
- **Description:** first 1-2 lines are the hook, then 2-3 short lines of true context (checked on
  the web; mention the source), then the pick-a-side question (see Comment driver), then 3-5
  hashtags (always #shorts, plus topic tags like #philosophy #wisdom and the thinker, e.g. #diogenes #stoicism).
- **Comment driver (every short; user rule, 14 Nov 2026):** write one **pick-a-side question**, a
  two-option verdict on the thinker's choice or idea ("Diogenes: genius or just rude?", "Would you
  rather be Alexander or Diogenes?"). Two named options, under 12 words, never an open
  "thoughts?" question. Use it as the description's comment question AND as a **pinned comment** the
  user posts right after upload (its own code block, labelled "Pinned comment"). Never show it in the
  video and never word it as "Team X or Team Y?" (user rule, 23 Nov 2026). Never bait comments with a
  deliberate mistake (accuracy is the channel's selling point). Remind in one line: reply to the
  first comments within the first hour.
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
with their own earlier Shorts, not a universal target. Baseline (first 14 h, 16 Nov 2026): stayed to
watch 42-55 %, average viewed 50-71 %; best = Trojan Horse 55.5 % / 71 %. Above 55 % stayed-to-watch is
a win; below 45 %, check the first 2 seconds before anything else.
One line of notes + offer the next idea. Update nothing in this skill unless the user asks.

## Retention playbook (studied 16 Nov 2026 from two Rick's Clips Shorts; user wants every short "10/10, watched to the end")
Technique only: never copy their characters, stories or art. Both references run ~63-65 s and hold
viewers with the same moves. Apply ALL of them in Phases 4 and 6:
1. **Frame 0 = the weird act + a looming threat in the same shot.** The main character is already
   DOING the strange thing (sawing a rail / holding two "garbage" tickets), and a danger or stake is
   visible behind them (a train coming down the track). Line 1 says that exact act in ≤ 8 words.
2. **"You see," explainer turn by ~3 s.** Right after the hook, the narrator starts explaining like
   a friend ("You see, …" / "Here's the thing: …"). Use it as the rewind line.
3. **Expert vs authority conflict.** A confident person in charge (boss, king, god) says the hero
   is wrong ("You're wrecking my railroad!" / "Impossible, sir."). The hero is quietly right. Early on the
   authority seems to win (a headline, a feast, a triumph), then a time-skip insert ("Then summer
   comes.") and step-by-step proof that the hero was right. This fits the doubter step of the Mystery formula.
4. **Proof inserts: show the mechanism, never only say it.** Every "how it works" step gets a
   macro close-up of a real object with colour highlights: numbers lighting up in colours, a rail
   glowing yellow → pink as it heats, a map with red route lines, a calendar page flipping May → July, a
   thermometer rising. In paper: cut-paper diagrams, glowing ink, a scroll or map on the table, a
   clay tablet. One insert per step, 1-2 s each.
5. **In-world text props carry information:** a newspaper headline, banner, sign or box label
   ("FIRST LINE IN GETS IT ALL!", "DESK STUFF") readable at phone size, ≤ 5 words, inside the safe box.
   In this style: a torn-paper scroll, decree, temple sign or wax tablet.
6. **Visual change about every 1 s; rotate 5 shot types** and never use the same type twice in a
   row: wide set → medium character → extreme close-up face (the face fills ~60 % of the frame) →
   macro insert of the object → POV or fly-through camera move (whip pan with motion blur between places).
   The camera never sits still. It is always pushing in, dollying or panning.
7. **A new face on every sentence:** smug, suspicious, sweat drop, huge round eyes, deadpan. At peak
   anger the antagonist's face changes colour (purple or red) and steam puffs appear. Punch in on the reaction.
8. **Fast, dense narration with no dead air:** ~2.8 words/s, about 170-185 words for 60-65 s.
   Silence beats stay ≤ 0.5 s and only before the reveal. Suggest ElevenLabs Speed 1.0 (not 0.90);
   the voice stays the same.
9. **Captions 1-3 words per chunk** (timing.py already drafts these). Use ONE word per chunk on
   punch words, and highlight the key noun.
10. **Ending = the biggest spectacle, then an instant cut back to the start.** The payoff is the most
    visual moment of the short (the rail buckles and the train flies sideways into an explosion; the
    game is pulled from every store). Say the aphorism over or right after it, then cut within 0.3 s:
    no hold, no fade, no spoken question. When the story allows, end mid-sentence so the last words
    flow into line 1 (the replay finishes the sentence). The last shot's framing echoes frame 0.
Self-check: point to the frame-0 act + threat, the authority who says "wrong", 2+ proof inserts, 1+
text prop, the shot-type rotation, and the spectacle ending. If any is missing, fix it before sending.

## Target audience: US viewers (user rule, 16 Nov 2026)
The channel's main goal is US viewers. Apply this in every phase:
1. **Connection:** the user keeps their laptop and iPad on their normal connections (no VPN unless
   they need it for something else). If they ask about a VPN, say plainly that it does not change
   who YouTube shows the Short to. What reaches US viewers is the language, the topic and the packaging.
2. **Script:** write in natural American English: US spelling (color, favorite, theater),
   American words and idioms ("mom", "vacation", "a ton of"), and US units and references only when a
   comparison is needed (feet, miles, "the size of a school bus"). No British or Filipino phrasing.
3. **Voice-over:** American English narration and pronunciation. Pick an American-accent voice and
   give US pronunciations of hard names (e.g. "Hermes" as HER-meez).
4. **Title, description, hashtags, thumbnail text:** word them the way a US viewer would search and
   talk ("Greek mythology", not "Greek mythos"). Use hooks and references that land for a US teen or adult.
5. **Upload consistently:** in the growth notes, remind the user to keep a steady schedule (the same
   days each week) instead of bursts.
6. **Check it's working:** when asking for the last short's stats, also ask once for YouTube Studio →
   Analytics → Audience → Geography ("Top geographies") to see whether US viewers are actually
   watching. If the US share stays low after several shorts, say so and suggest what to change
   (hook, topic, title wording).

## Series identity (set: "Tiny Lore")
One series tag only: **Tiny Lore**, written `| Tiny Lore` at the end of titles (16 Nov 2026; matches the
channel name and replaces "Tiny Olympus" and "Where Myths Came From". Titles had mixed both names, and one
consistent tag lets returning viewers spot the series. Never use "Tiny Olympus" again — change it if
the user picks another). Keep it in every short: as the title end-tag only if the title stays ≤ 60
characters, otherwise as a line in the description ("Tiny Lore — Greek myths in paper."); same
torn-paper hook-tag style and thumbnail look (cream title with dark outline, one yellow word) every
time. Hashtags: #shorts #philosophy #wisdom plus the thinker (e.g. #diogenes #seneca). Description
line when the tag doesn't fit: "Tiny Lore — big ideas in paper."

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
6. No new installs without asking (except the pre-approved free narrator, see Setup). Keep it simple,
   buildable, testable.
7. **Engine changes must reach GitHub in the same session (user rule, 14 Nov 2026).** Every new short
   downloads the engine fresh from GitHub, so a change made only in this session's copy (preview page,
   tools, assets) is lost next time ("it always goes back to the old version"). After any engine change:
   commit as farm-dirt, attach the repo with add_repo (access: push), push, then verify with a fresh
   `git clone --depth 1` that the change is there. Edits to this SKILL.md go through propose_skills.