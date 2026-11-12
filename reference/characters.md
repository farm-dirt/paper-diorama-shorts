# Characters — original cast (designed for this skill)

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
| Voice lines | short gasps, "Lolo?", "Ano 'yon?" | low "Hmm.", "Huwag." | barks, whimpers (SFX) |

## Adding a new character or creature
Write it in `project-files/custom.py` → `register()` using the `Rig` class from `cast.py`:
bones (parent, offset, rest angle) + parts (paper polygons in the bone's local space).
Design rules: one silhouette idea you can read in 0.5 s · faceted polygons, no outlines ·
3-5 colours from the palette (or one new accent) · painted eyes · at least one fold crease or
printed pattern · a part that can move for acting (head, arm, tail, wings).
Creatures from folklore: make the ONE weird trait huge (the manananggal's wings, the kapre's
cigar, the tikbalang's long horse head), keep everything else simple. Never copy a design from a
film, game or book; never draw a real person.
