# Rendering

Every screenshot is one AI-generated image produced from a prompt plus input images (Image 1 = the real capture, Image 2 = the approved style-ref.png). Claude writes the prompt, runs the engine unattended, inspects the result, and regenerates until it is right.

## Engines (chosen in intake, recorded in copy.md and `output/<app>/renders/engine.txt`)

| Engine | Needs | Output | Notes |
|---|---|---|---|
| `codex` (default) | Codex CLI logged in (`npm i -g @openai/codex && codex login`) | ~1.5 MP at the requested ratio (measured 851x1848 iPhone, 1086x1448 iPad) | No API key. Upscaled by finalize.py. Each run 1.5 to 3 min. |
| `openai` | `OPENAI_API_KEY` | exact 1760x3824 (iPhone) or 2064x2752 (iPad) | Sharpest text. Model `OPENAI_IMAGE_MODEL` (default `gpt-image-2`). |
| `gemini` | `GEMINI_API_KEY` | 9:16 or 3:4 at 4K, center-cropped to the iPhone ratio | Model `GEMINI_IMAGE_MODEL` (default `gemini-3-pro-image-preview`). The script tells the model which central band survives the crop. |
| `higgsfield` | Higgsfield MCP connector, credits | model-dependent | Not scriptable: Claude drives the MCP tools (below). |

Write the choice once: `echo codex > output/<app>/renders/engine.txt`. `render.sh` reads it (or `$ASOFEX_ENGINE`). If an engine fails mid-run (quota, outage), switch engines by editing engine.txt and re-render only the failing screens; keep style-ref.png so the set stays consistent.

## Scripts (use these, do not rewrite them per run)
- `scripts/make_prompts.py spec.json <render_dir>` writes engine-neutral `NN.prompt.txt` for every screen from a JSON spec: one `direction` paragraph (palette hex, background system, typography, accent, device treatment, ground shapes, full mascot description), `character: true`, `aspect` (`1320:2868` iPhone, `2064:2752` iPad), and per screen `nn, layout, h1, h2, accent, sub, pose, screen_notes, proof`. Layout keys: `top_cw` (text top, phone tilted clockwise, cropped bottom right), `top_ccw` (mirrored), `bottom` (device top, text bottom, phone cropped hard at the top), `top_straight` (straight phone with a hairline; use with a peeking mascot, as in the ideafex gallery set). Screenshot 1 gets `"first": true` so it carries the direction instead of a style-reference line. Save the spec next to the prompts as `spec.json`. Real examples: `gallery/*/*/prompts/spec.json`.
- `scripts/render.sh <render_dir> <NN> <capture.png|none> [vN]` renders with the chosen engine: capture as Image 1, `style-ref.png` as Image 2 when present, stdin closed, versioned outputs as `NN.rawvN.png`. Run up to 3 in parallel with `run_in_background`.
- `scripts/gen_image.py` is the OpenAI and Gemini backend that render.sh calls; run it directly only to debug.
- After screenshot 1 is approved: `cp 01.raw.png style-ref.png`, then generate and render the rest.

Engine-specific gotchas:
- codex: render.sh wraps the prompt with "Use your built-in image_gen tool" and the copy-to-`./NN.raw.png` instruction. Codex saves originals under `~/.codex/generated_images/<session>/`. Always redirect stdin from /dev/null when backgrounded (render.sh does).
- codex: never send a capture that contains a live secret (API key, token, connector URL with a key): the permission classifier blocks it as data exfiltration. Pixel-redact the value first with Pillow (paint over the text in the surface color, write a fake value of the same length in Menlo), save as `<name>-redacted.png`, delete the unredacted capture from the deliverables, and tell the prompt the values are placeholders. Do this for every engine anyway: captures leave the machine.
- gemini: check the uncropped image (`NN.raw.uncropped.png`) when the headline or phone is clipped; tighten the layout or shorten the headline.
- Save every prompt as NN.prompt.txt next to the render for reproducibility. Rerenders get NN.prompt.v2.txt / NNv2.prompt.txt and NN.rawv2.png.

## Higgsfield (MCP)
1. Load the tools: ToolSearch `higgsfield generate_image media_upload`.
2. Upload the capture and style-ref.png (`media_upload`, PUT the bytes with curl, `media_confirm`) to get media ids.
3. If unsure of the model, `models_explore` with action `recommend` for "text-heavy marketing image with reference images". Call `generate_image` with the prompt text from NN.prompt.txt, both images as references in order, the closest portrait aspect ratio, and the highest resolution offered. If the ratio is not 1320:2868, append the same "Canvas note" gen_image.py uses (keep content in the central band).
4. `jobs_wait`, download the result to `renders/<device>/NN.raw.png`, and finalize with `finalize.py --max-drift 0.25` when it needs a center crop.

## Prompt template (what make_prompts.py emits)

```
Use case: ads-marketing
Asset type: Apple App Store screenshot, portrait, aspect ratio <W>:<H>, full-bleed, no outer border, no device outside the canvas
Direction: <mascot direction paragraph: palette, ground shapes, typography, device treatment, mascot description>
Background: <system, exact hex colors>
Layout: <text-top device-bottom | text-bottom device-top | full-bleed UI | no-UI hero | badge wall>; headline block occupies the top <N>% of the canvas; keep the top 6% and bottom 6% free of text
Headline (verbatim, render exactly, spell-checked): "<headline>" in <face style>, <weight>, <color>, size about <N>% of canvas width; emphasize the word "<accent>" in <accent color>
Subheadline (verbatim): "<sub>" in <color>, about 45% of the headline size
Proof element: <none | laurel with "4.8 stars, 12K ratings" | press logos: list | "Join 250K+ users">
Device: <iPhone 17 Pro Max | iPad Pro 13> in <color>, <straight | tilted 8 degrees | cropped at bottom edge>, thin bezels, subtle shadow
Screen content: reproduce Image 1 exactly as the phone's screen. Keep every UI element, label, number, icon, and color identical to Image 1. Do not add, remove, or restyle any UI element. Status bar shows 9:41.
Style reference: Image 2 is an approved screenshot from this set; match its palette, typography, margins, lighting, and decoration style exactly so both look like one gallery.
Decoration: <mascot, shapes, glow, none>
Avoid: any text other than the headline, subheadline, and proof; watermarks; extra logos; other brand names; misspellings; cut-off text; a second device; hands; people unless requested
```
For screenshot 1 of each direction there is no style reference; describe the direction fully instead. Once the user approves one screenshot 1, it becomes style-ref.png for every other render in that set.

## Consistency gotchas seen in practice
- The model drifts on headline vertical position and phone scale between screens. State them as absolute fractions of the canvas ("first line starts at 7% of the canvas height", "phone top at the same height as Image 2") and check the contact sheet before finalizing.
- Threads with a lot of empty screen below the card look hollow in a device-top layout. Crop the phone hard at the top so the first element sits within the top 4% of the canvas.
- A trailing period after a gray accent word renders gray; accept it consistently across the set rather than fighting it per screen.

## Verification loop (strict, unlimited)

After every render, Read the raw PNG and check, in this order:
1. Text: headline and subheadline verbatim, no misspelling, nothing cut off, no stray text. Any fault means regenerate.
2. UI fidelity: open the source capture side by side. Every visible label, number, icon, layout region must match. Small blur is fine, wrong or invented content is not. Regenerate with a stronger invariant line ("Image 1 must be copied pixel for pixel onto the screen; changing any UI text is a failure").
3. Composition: headline inside safe zone, device not clipped in an unintended way, nothing important in the bottom 6%.
4. Consistency: palette, type, margins match style-ref.png. If it drifts, add "match Image 2 more strictly" and regenerate.
5. Aspect: within 2% of the target ratio (finalize.py enforces this).
Log each attempt in renders/<device>/attempts.md: screenshot, attempt number, what failed, what changed in the prompt. Keep going until all five pass. No attempt cap. If the same fault repeats 4 times, change strategy: simplify the layout, shorten the headline, or split the proof element out, then continue.

## Upscale and finalize

codex output must be enlarged 1.5x to 1.9x. Options, best first:
1. Higgsfield `upscale_image` MCP tool if connected and the user accepts the credit cost (ask once). Upload the raw, upscale 2x, download, then finalize.
2. `scripts/finalize.py` LANCZOS resize. Acceptable for backgrounds and device renders; text edges soften slightly. This is the default.
openai output is 1760x3824 and downscaled, which sharpens; or 2064x2752 exact for iPad. gemini output is cropped to ratio at 4K and downscaled.

Final step for each device:
```bash
python3 .claude/skills/asofex-ios-screenshots/scripts/finalize.py --size 1320x2868 --out-dir output/<app>/iphone-6.9 renders/iphone-6.9/01.raw.png ... renders/iphone-6.9/08.raw.png
python3 .claude/skills/asofex-ios-screenshots/scripts/finalize.py --verify output/<app>/iphone-6.9 --size 1320x2868
python3 .claude/skills/asofex-ios-screenshots/scripts/finalize.py --contact-sheet output/<app>/iphone-6.9
```
Read the contact sheet and judge the gallery as a whole: rhythm, consistency, story. Fix any outlier before presenting.

## iPad sets
Same storyboard and copy. Re-capture on iPad Pro 13 so the UI is native. Re-render with iPad ratio and the iPad device. Layouts shift: iPad is 3:4, so headlines sit beside or above a larger device with less vertical room; prefer text-top device-bottom with the device cropped at the bottom edge.
