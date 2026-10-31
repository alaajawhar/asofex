# Inspiration library: ../gallery

Three shipped mascot-led sets made with this skill. Never copy them. Look at their contact sheets before writing the direction so the bar is calibrated, then read `docs/copy.md` and `prompts/spec.json` of the closest one to see how the decisions became prompts.

| Set | Devices | Mascot | Look |
|---|---|---|---|
| `gallery/alarmifex` | iPhone 6.9" (8), iPad 13" (8) | Clock Buddy: alarm clock with headphones, purple-blue, 3D-soft | Light lavender ground waves, bold black headline with one purple accent word, phone tilted and alternating, buddy acts out each headline with one prop (scissors, waves surfboard, nightcap) |
| `gallery/ideafex` | iPhone 6.9" (9), iPad 13" (9) | Tilly: a small white tile-ghost | Dark masonry tile backdrop echoing the logo, condensed ALL CAPS headline with blue accent, straight phone cropped at an edge, Tilly peeking from behind the phone |
| `gallery/notifex` | iPhone 6.9" (8) | Bell buddy: the bell mark as a one-eyed ghost | Monochrome near-black, two flat gray hills, white headline with gray accent word, phone tilted about 10 degrees alternating, pose arc away / point / thumbs up / cable / juggle / cards / envelope / wave |

The gallery PNGs are 1260x2736, made before App Store Connect started rejecting that size; new runs export 1320x2868 (apple-specs.md).

## What all three do
- One idea per screenshot. Headline of 2 to 5 words, huge, at the top or bottom, never both. One accent word in a second color.
- Headline is a benefit or an identity claim, not a feature name ("Any sound. Your alarm.", "Leave the desk.").
- Brand color owns the background. One dominant hue and one or two accents; every screenshot stays in that family, the mascot included.
- Real UI from a real capture on every screen that shows a phone. The mascot never covers UI text.
- The mascot carries the emotion: one pose per screen, at most one prop, acting out that screen's headline.
- Composition rhythm: text top / device bottom, then text bottom / device top; tilt direction alternates so the gallery reads as one scroll.
- Consistent margins, headline position, and ground shapes across the set, locked by the approved screenshot 1 passed as Image 2.

## Patterns to reuse (adapted, never verbatim)
- Hook + promise, then 3 to 5 benefit screens, then 1 trust or breadth screen, then a closing CTA screen with the mascot waving or resting.
- Headline at the bottom for screens whose UI is the hero (device-top layout cropped hard at the top).
- When there is no third-party proof, specificity in the subline does the job ("Through Focus, offline, app closed.").

## Lessons from producing them
- All eight notifex screens passed first try once the character, ground, tilt, and type were fixed by an approved screenshot 1 used as Image 2.
- The model drifts on headline vertical position and phone scale; state them as fractions of the canvas (render.md).
- A monochrome brand stays monochrome: color only the accent word, never the mascot.
