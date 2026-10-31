#!/usr/bin/env python3
"""Write NN.prompt.txt files for a screenshot set from a JSON spec.

usage: make_prompts.py spec.json out_dir

spec.json:
{
  "aspect": "1320:2868",
  "direction": "<one paragraph: palette with hex, background system, typography, accent color, device treatment, decoration, character description if any>",
  "character": true,                      // false for a clean set: pose lines are omitted
  "layouts": {"top_cw": "...", "top_ccw": "...", "bottom": "..."},   // optional overrides of the defaults below
  "screens": [
    {"nn": "02", "layout": "top_cw", "h1": "It asks.", "h2": "You tap.", "accent": "tap",
     "sub": "Real questions with real options, not just allow or deny.",
     "pose": "standing beside the phone, pointing at the first option, eye wide.",
     "screen_notes": "The screen shows ... exactly as in Image 1."}
  ]
}
Prompts are engine-neutral: render.sh adds the engine-specific wrapper (Codex instructions, output path).
Screenshot 1 has no style reference, so give it its own hand-written prompt or set "first": true on that screen to
drop the Image 2 line. Every other screen gets Image 2 = the approved style-ref.png.
"""
import json, sys, pathlib

DEFAULT_LAYOUTS = {
    "top_cw": "Layout: headline block in the top 30% of the canvas (top 6% free of text), left-aligned at a 7% margin; then the phone tilted about 10 degrees clockwise, large, its lower right corner running off the right edge and bottom of the canvas{ground}; {char_pos_left}",
    "top_ccw": "Layout: mirrored: headline block in the top 30% of the canvas (top 6% free of text), left-aligned at a 7% margin; then the phone tilted about 8 degrees counter-clockwise, large, its lower left corner running off the left edge and bottom of the canvas{ground}; {char_pos_right}",
    "bottom": "Layout: device-top: the phone tilted about 8 degrees counter-clockwise occupies the top 62% of the canvas with its top edge running off the top of the canvas (status bar and Dynamic Island not visible), cropped so the first visible UI element sits within the top 4% of the canvas; {char_pos_bottom}the headline block and subheadline sit in the bottom 30% of the canvas, left-aligned at the 7% margin, bottom 6% free of text.",
    "top_straight": "Layout: text-top, device-bottom: headline block in the top 28% of the canvas (top 6% free of text, first line starts at 7% of the canvas height), left-aligned at a 7% margin; a 1px hairline across the text column below the subheadline; the phone straight and centered below it, its bottom edge running off the bottom of the canvas so the phone appears large.",
}
CHAR = {
    "ground": ", standing on the ground shapes",
    "char_pos_left": "the character in the lower left in front of the phone's bottom left edge, about 22% of the canvas height tall.",
    "char_pos_right": "the character in the lower right in front of the phone's bottom right edge, about 22% of the canvas height tall.",
    "char_pos_bottom": "the character sits beside the phone's bottom corner on the ground shapes; ",
}
NOCHAR = {"ground": "", "char_pos_left": "", "char_pos_right": "", "char_pos_bottom": ""}

TEMPLATE = """Use case: ads-marketing
Asset type: Apple App Store screenshot, portrait, aspect ratio {aspect}, full-bleed, no outer border, nothing outside the canvas.
{style_line}
{layout}
{pose_line}Headline (verbatim, render exactly, spell-checked, two lines): "{h1}" on line one and "{h2}" on line two. Render only the word "{accent}" in the accent color named in the direction; every other headline word stays in the headline color.
Subheadline (verbatim): "{sub}" Set it in one consistent weight and width; wrap to two lines when it does not fit the text column, never squeeze it.
Proof element: {proof}
Screen content: reproduce Image 1 exactly as the phone's screen. Keep every UI element, label, number, icon, spacing, and color identical to Image 1: the status bar with 9:41, the Dynamic Island, all text with the same line breaks, using real Latin glyphs only. Do not add, remove, restyle, or reword any UI element. {screen_notes}
Avoid: any text other than the headline, subheadline, proof, and the app UI's own text; watermarks; logos outside the phone; other brand names; misspellings; cut-off headline; a second device; a second character; hands; people; colors outside the direction's palette; glow.
"""

def main(spec_path, out_dir):
    spec = json.load(open(spec_path)); out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    layouts = dict(DEFAULT_LAYOUTS); layouts.update(spec.get("layouts", {}))
    fill = CHAR if spec.get("character") else NOCHAR
    for s in spec["screens"]:
        style = ("Direction: " + spec["direction"]) if s.get("first") else (
            "Style reference: Image 2 is the approved first screenshot of this set. Match it exactly: same background system, palette, typography, headline size and position, margins, device treatment, decoration, and character. Direction for reference: " + spec["direction"])
        layout = layouts[s["layout"]].format(**fill)
        pose = f"Character pose for this screen: {s['pose']}\n" if spec.get("character") and s.get("pose") else ""
        txt = TEMPLATE.format(aspect=spec.get("aspect", "1320:2868"), style_line=style, layout=layout, pose_line=pose,
                              h1=s["h1"], h2=s["h2"], accent=s["accent"], sub=s["sub"], proof=s.get("proof", "none."),
                              screen_notes=s.get("screen_notes", ""))
        (out / f"{s['nn']}.prompt.txt").write_text(txt); print("wrote", out / f"{s['nn']}.prompt.txt")

if __name__ == "__main__":
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2])
