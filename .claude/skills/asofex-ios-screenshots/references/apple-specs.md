# Apple App Store screenshot specs (verified 2026-10-31)

Re-verify at the start of every run, Apple changes this page:
`WebFetch https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications/`
If the fetched sizes differ from this table, use the fetched ones and propose a skill update.

## Sizes to offer in intake (portrait)

| Label | Exact export size | Required? | OpenAI CLI generation size |
|---|---|---|---|
| iPhone 6.9" | 1320 x 2868 | Required if app runs on iPhone | 1760 x 3824 (same ratio, downscale) |
| iPhone 6.5" | 1284 x 2778 or 1242 x 2688 | Only if 6.9" not provided | 1760 x 3808 (ratio 2.164, downscale to either) |
| iPad 13" | 2064 x 2752 or 2048 x 2732 | Required if app runs on iPad | 2064 x 2752 (exact, no resize) |

Use 1320 x 2868 for 6.9". App Store Connect rejected 1260 x 2736 in practice even though the spec page lists it; both share the same ratio, so a 1260 x 2736 set can be re-exported with `finalize.py --size 1320x2868`. The gallery sets are 1260 x 2736 because they predate this finding.

OpenAI image API constraints: both edges multiples of 16, max edge 3840, ratio <= 3:1, 655,360 to 8,294,400 total pixels.
Codex CLI's built-in `image_gen` tool ignores size requests and returns about 1.5 MP at the requested aspect ratio (measured: 851x1848 for iPhone ratio, 1086x1448 for iPad ratio). Gemini only accepts fixed aspect ratios (9:16 for iPhone, 3:4 for iPad) and is center-cropped to the iPhone ratio. See render.md for both.

## Hard rules
- PNG or JPEG. RGB. No alpha channel. Max 10 per device, we ship 6 to 10.
- All screenshots for one device must share one size and orientation.
- Portrait only for this skill unless the app is landscape-first.
- Screenshots 1 to 3 show in search results; on the product page only the first 1.5 are visible without scrolling. Screenshot 1 does most of the selling.
- Apple review: screenshots must show the app as it works. No misleading UI, no features that do not exist, no pricing that differs from the store, no "free" claims for paid features, no Apple trademarks misused, no other platforms' devices. Device frames are fine and common.
- Dark Mode: if the app supports it, at least one screenshot should show it.
- Text safe zone: keep headline text inside the central 88% width and away from the top 6% and bottom 6% of the canvas. Store UI never covers screenshots, but thumbnails in search are small: headline must be readable at 25% scale.
