# Notifex screenshot copy and storyboard  (updated 2026-09-11)
Devices: iPhone 6.9" 1260x2736 (captured on iPhone 17 Pro Max at 1320x2868). Locales: en-US.
Direction chosen: A. Signal (user choice 2026-09-11; B and C not rendered)
Captures (2026-09-11, iPhone 17 Pro Max simulator, dark, 9:41): `captures/iphone-6.9/lockscreen-push.png`, `thread-pending.png`, `thread-answered.png`, `connect-credentials-redacted.png` (secret pixel-redacted with a fake value before rendering), `inbox.png`, `thread-batch.png`, `switcher.png`, `welcome.png`. Style reference approved: `renders/iphone-6.9/style-ref.png` (screenshot 1, attempt 1).
Seed content lives in the "Mobile app" project (agent key "Claude Code"), account e2e-owner. Agent names allowed: Claude Code, Codex, OpenClaw, Hermes.

## Storyboard

| # | Role | Headline | Subheadline | Proof | Capture | Layout |
|---|------|----------|-------------|-------|---------|--------|
| 1 | Hook | Leave the desk. Your agent will *find* you. | Push when it needs a decision. One tap to unblock. | none | `lockscreen-push.png`: locked phone, Notifex push "Run the database migration now?" | text-top, device bottom, screen cropped at bottom edge |
| 2 | Core outcome | It asks. You *tap*. | Real questions with real options, not just allow or deny. | none | `thread-pending.png`: thread "Run the database migration now?" with options Run it / Dry run first / Wait for backup and the composer | text-top, device bottom |
| 3 | Continues | It waits. Then it *keeps going*. | No timeouts. Your answer unblocks the agent the moment you send it. | none | `thread-answered.png`: answered card with your chip, agent bubbles "Running migration 0042 on production." and "Done. 3 rows backfilled, 0 errors." | text-bottom, device top, cropped at top edge |
| 4 | Objection: setup | One config entry. *Nothing* on your Mac. | No bridge, no daemon, no QR pairing. Works with Claude Code, Codex, OpenClaw, Hermes, any MCP client. | none | `connect-credentials-redacted.png`: Set Up MCP sheet with the secret key card (fake value), MCP JSON card, connector URL | text-top, device bottom |
| 5 | Breadth of signal | Pinged when it *matters*. | "Deploy finished." "Tests are green." "I need a decision." | none | `inbox.png`: inbox with 8 realistic threads, unread dots, mixed messages and questions, agents Claude Code, Codex, Hermes | text-top, device bottom |
| 6 | Feature: batches | Three decisions. *One* card. | A release checklist arrives as one notification you page through. | none | `thread-batch.png`: batch card "1 of 3" in a thread | text-bottom, device top |
| 7 | Projects and team | Every project, its own *inbox*. | Switch like mail. Invite a teammate. First answer wins. | none | `switcher.png`: project switcher with Mobile app, Data pipeline, Client site, member counts, needs-answer counts | text-top, device bottom |
| 8 | Close | Your agents ask. *You* answer. | Free on iPhone. Any MCP agent. Set up in a minute. | none | `welcome.png`: welcome screen, bell mark, "Notifex" | no-UI hero: large bell mark, headline, small phone or none |

Accent word is marked with *asterisks*; the renderer colors it in the direction's accent (gray `#9A9A9E` on dark, `#6E6E73` on light) or sets it in italic where the direction says so.

## Render status (2026-09-11)
All eight rendered with Codex image_gen in direction A, verified against the captures and copy, exported to `iphone-6.9/01.png` to `08.png` at 1260x2736 (finalize.py verify PASS). Attempt log: `renders/iphone-6.9/attempts.md`. Re-renders: 03 (subline weight), 05 (glyph glitch in 'errors'), 06 (empty screen area), 07 (leftover project rows, then headline alignment), 08 (phone crop). Contact sheet: `iphone-6.9/_contact-sheet.jpg`.

## Rationale per screenshot
1. Search results show screenshots 1 to 3. The lock screen is the only image in the category that shows the agent reaching the human instead of the human reaching a terminal. The headline grants permission ("leave the desk") and the image proves the mechanism.
2. The question card is the product. Options with real words ("Ship it", "Run the full suite first", "Hold until Monday") show this is a decision, not an allow/deny button, which is the gap every mirror app leaves open.
3. Answers the fear from the sweep: "I tapped Approve and the terminal never released", "any approval longer than 60 seconds is lost". The follow-up bubbles show the loop closing.
4. The number one objection in the category: mirror apps need a Mac app, daemon, Node bridge, or QR pairing. The JSON card is real UI and is the whole setup. Naming Codex, OpenClaw, Hermes answers "is it Claude-only".
5. Uses the landing page's own agent phrases as the subline. The inbox with mixed agents shows breadth without a feature list.
6. Batches are a real differentiator (nobody else pages a checklist), and the "1 of 3" card is visually distinct.
7. Projects plus first-answer-wins in one screen, late in the set where the team angle belongs for a solo-first audience.
8. Closes on the listing subtitle so the gallery and the store text say the same sentence. "Free" and "set up in a minute" are the last objections.

## Alternates (for A/B tests)
1. a) Stop babysitting your terminal. b) Go for the walk. It will ask if it needs you. c) The pager for your AI agents.
2. a) A real question. A real answer. b) Decisions, not just permissions. c) Tap the option. Skip the terminal.
3. a) Answer once. It continues. b) Your tap unblocks the run. c) Nothing is lost while you were away.
4. a) Paste one entry. Done. b) No bridge. No daemon. No pairing. c) Any MCP agent, one key.
5. a) Deploy finished. Tests green. Needs you. b) Only the pushes that matter. c) The agent's loudest moments, in one list.
6. a) A checklist in one push. b) Page through the release. c) Batch questions, one notification.
7. a) Inboxes, not channels. b) One project per inbox. c) Everyone gets the push. First answer wins.
8. a) The pager for your AI agents. b) Ask from the terminal. Answer from anywhere. c) Free. Calm. Yours.

## Seed content plan (what the captures will show)
Project "Mobile app". Threads, newest first:
1. Question (single select) from Claude Code: "Run the database migration now?" context "0042_users_plan_not_null. Adds NOT NULL DEFAULT 'free' to users.plan. 3 null rows in production will be backfilled." options: "Run it", "Dry run first", "Wait for backup". Answered "Run it" for screenshot 3, then agent messages "Running migration 0042 on production." and "Done. 3 rows backfilled, 0 errors." A second identical question is left pending for screenshots 1 and 2. (User chose this over the TestFlight scenario: higher stakes, echoes the "wiped the database" fear.)
2. Batch from Claude Code, 3 questions: "Which build should go to review?" (Latest release candidate / Current App Store build), "Who gets the release note?" (Beta testers / Everyone / Nobody yet), "When should rollout begin?" (Now / Tomorrow 9:00 / After the weekend). Pending, for screenshot 6.
3. Message from Codex: "Deploy finished." body "api v2.3.0 is live on eu-north-1. 0 errors in the first 5 minutes."
4. Message from Claude Code: "Tests are green." body "214 passed, 0 failed, 41s."
5. Question (free text) from Hermes: "What should the empty-state copy say when there are no invoices?" pending.
6. Message from Claude Code: "Migration needs a decision." body "users.plan has 3 null rows in production."
7. Question (multi select) from OpenClaw: "Which platforms for the beta?" options iOS / iPadOS / macOS. pending.
8. Message from Codex: "Nightly build failed." body "Xcode 26.6: missing entitlement for push. Fix pushed, re-running."
Other projects for the switcher: "Data pipeline" (agent Codex), "Client site" (agent Hermes), with 1 and 2 needs-answer counts.

## Directions
### A. Signal
Vibe: the brand itself, calm and precise. Background `#0D0D0F` with a faint radial lift (`#1A1A1E`) behind the device. Headline SF-style grotesk bold, white `#F2F2F2`, 2 lines, accent word in `#9A9A9E`. Subline `#9A9A9E`. Device: iPhone 17 Pro Max, black, straight, thin bezel, soft shadow. Decoration: a single hairline horizontal rule under the headline. Proof style: none. Risk: the category is dark, so it blends; wins on consistency and restraint.
### B. Paper
Vibe: the light side of the brand system, standing out in a dark category. Background `#F7F7F5`, headline `#1C1C1E`, accent word `#6E6E73`, subline `#6E6E73`. Device: black iPhone tilted 6 degrees with a soft long shadow, dark-mode UI inside so the screen pops against the paper. Decoration: none, generous margins. Proof style: none. Risk: less "developer night mode" feel, but every search neighbor is black, so it reads as premium and different.
### C. Pager
Vibe: developer-native, the "ping" made visible. Background `#0D0D0F` with two or three large concentric rings in `#1A1A1E` and `#232327` radiating from the device, a ghosted bell mark at 6 percent opacity top-right. Headline white, tighter and larger, accent word in italic white. A small monospaced eyebrow above the headline: "01 / NEEDS A DECISION", "02 / ONE TAP", "03 / UNBLOCKED" and so on. Device: cropped at the bottom edge, larger than in A. Proof style: none. Risk: rings and eyebrows must stay quiet or it breaks the calm rule; most distinctive of the three.

## Localization
en-US only for this run.

## Set 2 directions (requested 2026-09-11: characters, inclined screens, template-inspired)
Same copy, same captures, new look. User chose D (Bell buddy) with a story arc for the character: away, pointing at options, thumbs up, one cable, juggling pings, fan of three cards, peeking with an envelope, waving goodbye. Phone tilt alternates 10° clockwise / 8° counter-clockwise. Output in `set2-D/01.png` to `08.png` (1260x2736, verify PASS) plus `_contact-sheet.jpg`; all eight passed on the first attempt (`renders/set2-D/attempts.md`).
### D. Bell buddy
Vibe: Headspace's warmth in Notifex's monochrome. The bell mark becomes a soft, rounded character: the notification dot is its single eye, a small calm mouth, tiny arms. It leans, peeks, points, or naps next to the phone. White with soft gray shading on near-black `#0D0D0F`; large flat gray shapes (`#1A1A1E`, `#232327`) as ground and hills like Headspace's layered waves. Phone tilted 10 degrees, edge-cropped. Headline huge, two weights. Accent word in `#9A9A9E`.
### E. Agent and you
Vibe: Serenity's illustrated cards meet Parrot's bold type, in grainy monochrome with one muted emblem tone per screen (slate `#7C8797`, moss `#828C6C`, clay `#B98D74`, sand `#BBA57C`, steel `#6C8B97`, plum `#93789A`, pine `#5F8C7C`, stone `#928C84`) used only for the character. Two recurring characters: a small boxy agent with a blinking cursor face, and a relaxed developer on a couch, at a cafe, on a walk. Grainy texture, soft shadows. Phone tilted 8 degrees the other way on alternating screens. Headline bold grotesk, accent word in the screen's tone.
