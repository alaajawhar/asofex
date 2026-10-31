# Notifex research  (updated 2026-09-11)

## Inputs received
- Source: `<local>/notifex/ios` (SwiftUI app, scheme `notifex`, iPhone-only per pbxproj, iOS 26.5, Debug points at production backend) and `<local>/notifex/claude` (planning docs, `appstore-metadata.md`, brand kit, prior captures).
- Landing page: https://notifexapp.com and /about. No live App Store page yet (Apple ID 6806766252, "Prepare for Submission", six placeholder screenshots uploaded).
- Brand: strict monochrome (bg `#0D0D0F`, surface `#1A1A1E`, text `#F2F2F2` / `#9A9A9E`), SF Pro in UI, Inter 800 wordmark, bell-with-dot mark, no mascot, no emoji, no green, success is never green. Assets in `claude/brand/`.
- User answers: audience is solo developers running Claude Code or similar agents; no proof exists; free, no pricing shown; hero moments are the tappable question card and the lock screen push; iPhone 6.9" only, 8 screenshots, en-US.
- Research sweep: 187 agent reads (171 reachable), 804 verbatim quotes, 54 competitor profiles. Raw data in `../research/findings-run1.json`, digest in `../research/digest-run1.md`. A compact gap-fill run is pending; its findings will be merged here.

## Audience
- Who: developers who kick off long Claude Code (also Codex CLI, OpenCode, Cursor) tasks and step away: coffee, walk, couch, bed, plane, another project. Many run 4 to 8 sessions at once. They live on r/ClaudeAI, r/ClaudeCode (728K weekly visitors), Hacker News, GitHub issues.
- Search intent and phrases (from the sweep): "approve claude code from phone", "claude code push notification approval app", "babysitting claude code", "how to get push notification when claude code needs approval", "claude code stops for confirmation notification", "human in the loop ai agent notifications", "ask a human mcp tool", "claude code mobile app".
- Pains, in their words:
  1. "Step away for a few minutes and Claude just sits there waiting." (r/ClaudeAI) and "come back to find it's been sitting there waiting on a permission the whole time" (r/ClaudeAI, 1tvox1k).
  2. "The bottleneck increasingly isn't Claude's speed — it's the human noticing that Claude is waiting." (anthropics/claude-code #36885) and "I felt like I am the bottleneck and not the waiting times" (HN 44878650).
  3. "I am CONSTANTLY being asked to approve every individual step" so people go YOLO: "Meh I just Yolo it and turn on bypass permissions", "Skip permission and tell opus you're going to bed". Then: "Wiping the database to run tests", "found the credentials, and ran the script against it... 100% unprompted".
  4. "finish or get stuck asking a question, and I wouldn't notice until much later because I wasn't watching the terminal" (HN 46563672).
  5. Existing fixes are DIY and fragile: "Of course you can: Termux + SSH + tmux + Tailscale. And you will not get any notifications." Approver hooks time out ("Any approval that takes longer than 60 seconds to tap is lost"), public ntfy topics, Telegram bot tokens, Node servers, QR pairing.
  6. Mirror apps fail at the one moment that matters: "the happy permissions prompt ... clicking them is non responsive and so I have to use yolo modes", "there's no push notification when Claude finishes or needs permission approval", "session stuck at permission acquisition with no visible dialog".
- Desired outcomes, in their words: "Stop babysitting your terminal" (62 upvotes as a tagline), "I can finally leave my terminal knowing my agents are working", "approve permissions while getting coffee", "check in on things and clear blockers from the pub", "going for more walks throughout my work day, and just checking in on Claude", "only come back when needed", "persistence: if I miss the push notification, the request just sits there", "having a real UI for the approval means I can read the full tool input before deciding".

## App as it is today
- Store listing draft: name Notifex, subtitle "Your agents ask. You answer.", Developer Tools / Productivity, promo "AI agents shouldn't guess. Notifex turns their questions into push notifications you answer in one tap — from anywhere." Description opens "The pager and decision inbox for your AI agents."
- Landing page: eyebrow "The pager for your AI agents", H1 "Your agents can ask you anything — from anywhere.", features: Pushes when it matters ("Deploy finished." "Tests are green." "I need a decision."), Questions that wait for you, Real back-and-forth, First answer wins, Zero-integration MCP, Scoped revocable keys. Strip: "iPhone · works with any MCP client · first answer wins".
- Product truth from code: two MCP tools, `send_message` and `ask_question` (single select, multi select, free text, optional context, batches via `ask_questions`, follow-up rounds in the same thread). `ask_question` blocks until a human answers, no timeout. Every project member gets the push, first answer wins. Projects switch like inboxes. Search per project. Setup is one MCP JSON entry (URL plus bearer key), nothing runs on the Mac. Keys are per project, revocable. No paywall.
- Current screenshots: six raw-ish captures uploaded as placeholders. Weak: no headline story, no hero moment.
- Reviews: none yet.

## Competitors
Two clusters plus DIY. Full profiles in `../research/digest-run1.md`.

| App | Screenshot 1 headline | Proof used | Visual style | Weakness we exploit |
|---|---|---|---|---|
| Happy (Happy Coder) 4.9, 970+ ratings | "Code everything, everywhere, all at once" | ratings on landing page, open source, 22k GitHub stars | dark bg, white bold headline, phone with terminal/diff UI, feature-label per screen | Terminal mirror that needs your Mac awake and a relay; permission cards fail to render or respond ("forced into yolo mode"); no push on finish/needs-input in many reports; never shows the approval moment |
| Omnara 4.4, 36 ratings | "No Keyboard. No Desk." | PH #1 of the day, YC S25 | cinematic photo backdrops, small phone inset | Generic remote-monitoring headlines; daemon mirrors full session; Android users report no notifications when agents need input |
| Happier 4.4, 10 | "Start coding anywhere. Continue everywhere." | open source, E2E | dark, gradient orb, phone | 3 of 10 screenshots have no headline; heavy multi-account feature pitch; approval buried at screenshot 8 |
| CC Pocket 5.0, 6 | "Review it. Ship it." | none | dark, raw UI | Needs Node 20 bridge server and QR pairing; pitches diffs and media, not the approval moment |
| Forge Remote, no ratings | "INSTANT QR CODE PAIRING" | none | black with orange ember glow, all caps | 5 of 6 screens explain setup; RPG gamification undermines trust for a permissions tool |
| Claude Code Notifier Companion (TouchTap) 4.4, 7 | "Never Miss a Prompt. Never Lose Momentum." | none | white bg, black headline, phone | Requires a running Mac app and iTerm2; pays per response after 3; not self-contained |
| KittyLitter, Vicoa, ServerCC, Control, Tactic, Nimbalyst, Mobile for Claude Code | feature labels or none | thin or none | dark, raw UI, inconsistent | Same template, same words: "code from anywhere", "your terminal wherever you are"; none dramatizes a question being asked and answered |
| Pushover 4.8, 3.6K / ntfy 4.8, 430 / Pushcut 4.4, 537 | none, or "Push notifications via REST" | ratings only | bare UI captures, no headline | One-way alerts; cannot ask a question or wait for an answer; ntfy iOS delivery is unreliable per its own tracker; no AI agent framing |
| Anthropic /remote-control | first party | first party | n/a | Claude-only, Pro+ plans, mirrors sessions; not a cross-agent pager |
| DIY: claude-remote-approver, ccgram, Telegram bots, Garmin buzzer | "I made a tool to approve/deny Claude Code permission requests from your phone" | upvotes | none | npm installs, bot tokens, public topics, 60 second timeouts, silent permission loss, Claude-only |

## Category conventions
- Respect: dark near-black backgrounds; one short bold white headline per screen; real dark-mode UI in a phone; developer-honest tone; encryption and key scoping mentioned somewhere.
- Break: everyone writes feature labels ("Realtime Voice", "Review changes on the go"). We write the moment: the agent asked, you answered, it kept going. Everyone hides the approval flow; we make it screenshot 1 and 2. Everyone's set is inconsistent; ours is one continuous story in one visual system. Everyone sells "terminal in your pocket"; we sell "you are not the bottleneck anymore" and "nothing to run on your Mac".

## Proof inventory (only verified)
- None external. No ratings, press, counts, or awards. Do not invent.
- Product proof we can state truthfully: works with any MCP client (Claude Code, Codex CLI, custom agents); one config entry, nothing installed or running on the Mac; questions wait until answered with no timeout; three answer types plus free text; batches page as one card; first answer wins across a team; per-project revocable keys; free.
- Audience proof we may quote only if the user wants third-party voice: the pain quotes above are public and attributable, but they are not about Notifex, so they belong in research, not on screenshots.

## Open questions
- Whether the App Store listing will keep "Developer Tools" primary: affects the top-charts neighbors we get compared with (all the mirror apps).
- Whether the seeded demo content should show Claude Code explicitly by name in agent messages. Assumed yes, since the audience searches for it and it is a truthful integration.
- Gap-fill run (8 agents, 7 bundles, `../research/findings-run2.json`) returned 2026-09-11. It confirmed run 1 and added: Notifex has no press, forum, or Product Hunt footprint yet (zero hits for the name), so the gallery carries the whole first impression. Two more usable audience lines: "An agent that runs when nobody is watching needs the gate to survive you being away, which rules out anything resolving in a terminal." (pushary.com roundup) and "I've literally been able to step out, get a coffee, and still keep the session going from my phone." (r/ClaudeCode 1mwyzr3). Non-Claude communities (Cursor, OpenHands, Devin) and YouTube or X comments remain unread; low priority for this run.
