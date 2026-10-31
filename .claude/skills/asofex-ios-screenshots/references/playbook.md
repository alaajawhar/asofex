# Conversion playbook: research, positioning, copy, storyboard, design

Screenshots are an ad. The install decision happens in under 3 seconds on screenshot 1, and the next 2 confirm it. Everything here serves that.

## 1. Research (writes research.md)
Sources, in priority order:
1. What the user gave: brief, source code, captures, brand assets, URLs.
2. The app's own App Store page via WebFetch: subtitle, description, what's new, ratings, review excerpts. Reviews are the voice of the customer: copy their words.
3. Three to five competitor listings, same category. Note their headline patterns, proof used, color, and what they all say (so we can say something different).
4. Reddit, forums, and blogs for the audience's language about the problem. Search "[category] app" + "frustrated", "switched from", "best", "worth it".
5. A browser tool (claude-in-chrome or Playwright MCP, whichever is connected) when a page blocks fetch or when you need to view competitor screenshot galleries. Screenshot competitor sets into output/<app>/research/competitors/ for reference only.

Capture in research.md:
- Audience: who, when they search, what they type, what they are afraid of.
- Top 3 pains and top 3 desired outcomes, quoted in their words.
- Competitor matrix: name, headline on screenshot 1, proof used, visual style, weakness.
- Category conventions we must respect and one we will break.
- Proof inventory we can legitimately use: ratings, counts, awards, press, founder credibility. Never invent proof. If there is none, use product proof: specificity, before/after, guarantees.

## 2. Positioning (writes positioning.md)
- One sentence: For [audience] who [pain], [app] is the [category] that [unique outcome], unlike [alternative] which [weakness].
- The single promise screenshot 1 must make. Test: would the audience stop scrolling for it?
- Three supporting benefits, each mapped to a real screen in the app.
- Tone: three adjectives and three words we never use.
- Objections to pre-empt in the gallery: price, trust, effort, "does it work for me".

## 3. Copy (writes copy.md)
Per screenshot: headline, optional subheadline, optional proof line, and rationale.
Rules:
- Headline 2 to 5 words. Subheadline under 9 words. Sentence case unless brand is all caps.
- Lead with outcome, not feature. "Fall asleep in minutes" beats "Sleep sounds library".
- Specific beats vague: numbers, time frames, names. "Learn 30 words a day" beats "Learn faster".
- One accent word per headline is allowed for emphasis; mark it with *asterisks* in copy.md so the renderer colors it.
- No jargon, no "seamless", "powerful", "intuitive", "all-in-one". Ban list lives in positioning.md tone section.
- Readable at thumbnail size: if the headline needs more than two lines at 126px font on 1320 width, cut words.
- Write 3 headline options per screen, pick one, keep the others under "Alternates" for A/B tests.

## 4. Storyboard (also in copy.md)
Default arc for 6 to 10 screens, adapt per app:
1. Hook: the promise plus strongest proof. Logo small. Minimal UI.
2. Core outcome: hero screen of the app doing the main job.
3. Second benefit.
4. Third benefit or "how it works" in one glance.
5. Trust: press, ratings, reviews quote, privacy, or expert backing.
6. Breadth or personalization: library, integrations, widgets, watch, Dark Mode.
7. to 9. Optional: differentiator vs competitor, before/after, community, offline, family sharing.
Last. Close: restate the promise, CTA verb ("Start sleeping better tonight"), free trial or price truth if relevant.
For each screen record: which real capture is used, layout type (text-top device-bottom, text-bottom device-top, full-bleed UI, no-UI hero, badge wall), and proof element if any.
Present the storyboard to the user with AskUserQuestion before rendering. Edit until approved.

## 5. The mascot direction (the only direction this skill produces)
Write it into copy.md under "Direction": name, one-line vibe, background system, palette (hex from brand assets or extracted from captures), typography (display face style, weight, case), device treatment, mascot description, ground shapes, proof style. There is no direction comparison: design the mascot direction well, render screenshot 1, get it approved, then render the set.

What it is: the app's brand turned into a small expressive character that acts out each screen's promise, next to a large phone tilted on layered flat ground shapes. Borrowed moves: big-type-plus-mascot warmth and layered hills, a tilted edge-cropped device, illustrated softness. Adapted, never copied. See `gallery/` for three shipped examples (alarmifex Clock Buddy, ideafex Tilly, notifex Bell buddy).
Where the character comes from, in this order:
1. The brand's existing mascot, used as is.
2. The app icon or mark turned into a character (a bell became a one-eyed rounded "bell buddy": the notification dot as its eye, a calm mouth, two stubby arms, no legs, flat and outline-free; a clock face became "Clock Buddy").
3. If the mark is abstract, an invented creature or object from the app's world, in the brand palette.
Composition rules that made it work: character about 22% of canvas height, overlapping a bottom corner of the phone, never covering UI text; phone tilted about 10 degrees, alternating clockwise and counter-clockwise across the set; two flat layered ground shapes in the two darkest surface tones; headline in a rounded or geometric bold, one accent word in the secondary text color; everything outside the phone stays inside the brand palette (a monochrome brand stays monochrome, the character included).
The pose story is written fresh per app from the storyboard: one pose per screen, one prop per screen at most, the pose acts out that screen's headline. Worked example (Notifex, 8 screens): away from the desk beside a lock screen push; pointing at the first option; thumbs up as the agent continues; offering a single cable ("nothing on your Mac"); juggling three pings; holding a fan of three cards ("one card"); peeking from behind the phone with an envelope ("its own inbox"); waving goodbye at the close. Record the arc in copy.md.
Variant seen in practice (ideafex): a straight, centered phone cropped at the bottom with a smaller mascot peeking from behind it, over a backdrop that echoes the logo. Use it when the brand mark suggests a backdrop pattern; the mascot still acts out each headline.
Consistency rule: after screenshot 1 is approved, every later render passes it as a style reference image (Image 2).
