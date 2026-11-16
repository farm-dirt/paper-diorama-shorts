# Characters — original cast (designed for this skill)

## Greek cast (Tiny Olympus starter kit, `engine/greek.py`) — use these for the paper channel
Same human bones and poses as Ilaw/Mang Oso (every pose in the pose library works, and they can walk).
Default scales: zeus 0.84, hera 0.80, aphrodite 0.80, ares 0.84, mortal_man 0.80, mortal_woman 0.78.

| who | look | good for |
|---|---|---|
| zeus | white robe, blue drape, long white beard, gold laurel | the cheater, the cover-up artist (`"prop": "bolt"`) |
| hera | teal robe, plum drape, dark bun, gold diadem | the detective / revenge |
| aphrodite | blush-pink robe, cream drape, long copper hair | love chaos, vanity feuds (`"prop": "apple"`) |
| ares | short red tunic, bronze helmet with red crest, short black beard | the hothead (`"prop": "spear"`) |
| mortal_man | short sand tunic, brown drape, short hair | heroes, kings, shepherds, the punished guard |
| mortal_woman | lilac robe, cream veil | nymphs, princesses, priestesses |
Props on any of them: `"pose": {"prop": "bolt" | "trident" | "spear" | "goblet" | "apple" | "scroll"}`.
New gods with the SAME look: `greek.add_figure(...)` in custom.py (options in `engine/greek.py`'s
header). If a god will appear in more than one short, add it to `FIGURES` in greek.py and push, so it
looks identical every time.
Model sheet: `python3 tools/model_sheet.py OUT.png zeus hera aphrodite ares mortal_man mortal_woman`.

## Folklore cast (from the first version of this channel)
Ilaw, Mang Oso and Kupas were designed for Philippine folklore. They are NOT used in Greek shorts
(a girl in a raincoat at a Greek temple breaks the story); keep them for a one-off only if the user asks.

Model sheet: `python3 tools/model_sheet.py OUT.png`. Characters keep their colours and
proportions in every shot. Default scales: Ilaw 0.86, Mang Oso 0.82, Kupas 0.72.

| | Ilaw | Mang Oso | Kupas |
|---|---|---|---|
| Who | 9-year-old girl, curious, brave-ish | old ferryman, gruff, secretly soft | dog folded from old newspaper |
| Build | small, A-line folded mustard raincoat, hood up | tall, boxy, cardboard-box head with a side facet | boat-shaped body, triangle face |
| Face | 12-sided paper face, black zigzag bob, dot eyes, blush | folded white paper mustache + brows, big triangle nose | dot eyes, flop ears, ink nose |
| Colours | mustard, navy, terracotta boots, lantern red | deep teal striped sweater, brown trousers, rust cap | newsprint with faint print lines |
| Prop | red paper lantern (always glows) | oar (`"prop": "oar"`) | — |
| Role | eyes of the audience: discovers, reacts | the one who knows the old stories / warns | comic reactions, senses danger first |

## Adding a new character or creature
Write it in `project-files/custom.py` → `register()` using the `Rig` class from `cast.py`:
bones (parent, offset, rest angle) + parts (paper polygons in the bone's local space).
Design rules: one silhouette idea you can read in 0.5 s · faceted polygons, no outlines ·
3-5 colours from the palette (or one new accent) · painted eyes · at least one fold crease or
printed pattern · a part that can move for acting (head, arm, tail, wings).
Creatures and monsters: make the ONE weird trait huge (the Cyclops's single eye, Medusa's snakes,
Cerberus's three heads, the Minotaur's horns), keep everything else simple. Never copy a design from a
film, game or book; never draw a real person.
