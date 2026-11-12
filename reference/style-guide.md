# Style guide — "paper diorama" look

Analysed once from two references: a stop-motion origami sequence and the short film *GRUFF*
(Righteous Robot). We took only their shared **technique**: a handmade miniature world of
paper and card, filmed like a real tiny set. **Never copy their characters, creatures, costumes,
sets or story beats.** Nothing here comes from the user's pastel-toon-shorts skill either
(no bean heads, no pastel palette, no thick outlines, no shared code).

## The 6 rules that make it read as paper
1. **Material first.** Every shape is a piece of cut paper: rough edges (`rough`), grain, a light
   cut-edge on the lit side and a darker edge on the shadow side (`rim`), a soft drop shadow on the
   paper under it (`shadow`). Big shapes get a fold `crease` or a printed `pat` (stripes, check,
   dots, news, planks). Painted marks (eyes, mouths, blush) use `paint=True` — flat, no edges.
2. **No outlines.** Shapes are separated by value and shadow, never by a drawn line.
3. **Faceted, simple shapes.** Faces are 10-14-sided polygons, heads can be boxes, animals are
   folded triangles. Fewer, bolder pieces beat many small ones.
4. **Depth = layers.** 8-14 layers per set at distinct z. Each layer floats (`lift`) and casts a
   shadow on the one behind. Far layers are cooler/darker and lower contrast.
5. **One key light.** Light always comes from upper-left (shadows fall lower-right). Warm key
   (sun, lamp, lantern) + cool fill. Practical lights (lanterns, windows, fireflies) are `glows`.
6. **Shallow focus.** Actors at z=2 are sharp; background softens with distance; anything in
   front of the actors (z<1.5) is heavily blurred. Rack focus is a storytelling tool.

## Palette (earthy, saturated, never pastel)
| Name | Hex | Use |
|---|---|---|
| Mustard | #E0A33A | Ilaw's raincoat, thatch |
| Terracotta | #C8553D | boots, boats, walls |
| Deep teal | #2F6F73 | Mang Oso's sweater, water |
| Lantern red | #D2453A | lanterns, caption highlight, danger accents |
| Rust | #8C3B2E | cap, curtains |
| Newsprint | #ECE2CB | Kupas, paper props |
| Dusk plum | #6A4560 | far hills |
| Ink | #241C1E | hair, eyes |
Location colour comes from the set + time of day (`light`: dusk, day, night, lamp, storm), not
from recolouring characters. Characters keep their colours in every shot.

## Time-of-day colour script
- **dusk** warm orange key, plum shadows — default, safe/curious beats.
- **day** neutral, bright — comedy, explanations.
- **night** blue tint, lanterns/windows/fireflies glow — mystery, creature reveals.
- **lamp** warm interior — family, cosy, "lola tells the story".
- **storm** cold grey — danger. Add `flash` (lantern red) for a scare frame.

## Camera language (borrowed from miniature film-making)
- Slow push-ins (zoom 1.0 → 1.15) for tension; pull-outs for reveals.
- Low camera = heroic/creepy; `cam` pan_y negative looks up the set.
- Rack focus from actor (z 2) to a foreground clue (z 0.7-1.2) or back.
- Short shake (`shake`) for thuds/impacts only.
- Letterbox (`letterbox: 140`) for one cinematic beat, not the whole short.

## Captions & text
Captions are torn cream paper labels (Fraunces Black, ink colour), key word in lantern red
(`*word*`). Hook text is a bigger tilted label at 0-2 s. Thumbnail titles: cream + thick dark
outline, one word in yellow.

## Motion
Everything moves smoothly at 24 fps by default (the user found stepped "on twos" walking choppy).
`"steps": 12` in project.json gives a stop-motion feel for poses only; walks and positions always
stay smooth. Snappy pose changes use the `back` ease (slight overshoot).
Every actor breathes, drifts and blinks automatically; never leave a face unchanged > 2.5 s.
