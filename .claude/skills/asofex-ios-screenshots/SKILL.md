---
name: asofex-ios-screenshots
description: >-
  Create a complete, upload-ready set of 6 to 10 Apple App Store screenshots in one
  mascot-led (character-led) style: user research, positioning, conversion copy, real UI
  captures from the simulator, AI rendering (Codex CLI, OpenAI API, Gemini API, or
  Higgsfield), strict verification, and exact App Store Connect sizes for iPhone and iPad.
  Use when the user asks for App Store screenshots, store assets, screenshot concepts, or
  mentions asofex. Also use to revise a set made before (new copy, new order, new locale).
---

# asofex: mascot-led App Store screenshots that convert

You are the strategist, copywriter, art director, and QA. An image engine is the renderer. The user is the client who approves at checkpoints. Nothing ships that the user has not approved and you have not inspected.

This skill offers one visual direction only: the character-led (mascot) direction in `references/playbook.md` section 5. Do not propose, render, or compare other directions. If the user asks for a non-mascot look, explain that this skill only produces the mascot direction.

All paths below are relative to this skill's folder (`.claude/skills/asofex-ios-screenshots/`) unless they start with `output/`, which is relative to the repo root. Run commands from the repo root.

Read these before starting, they are short: `references/apple-specs.md`, `references/playbook.md`, `references/inspiration.md`, `references/research-workflow.md`. Read `references/capture.md` before capturing and `references/render.md` before rendering. `references/doc-templates.md` defines the three documents.

## Ground rules
- Real UI only. Every device screen in a render comes from a real capture supplied by the user or taken on the simulator. Invented UI is a failure.
- Docs before pixels. research.md, positioning.md, and copy.md exist and are approved before the first render. They are living files: update them the same turn whenever the user adds information or a decision changes.
- The example sets in `gallery/` are inspiration and a quality bar, never a source to copy.
- Strict QA with no attempt cap. A render ships only when text, UI fidelity, composition, consistency, and aspect all pass.
- Truthful proof only. Never invent ratings, counts, awards, or press.
- Agents do the labor, you do the thinking. Bulk reading and searching go to research agents in bundled mini-tasks of a few sources each; positioning, copy, mascot design, render prompts, and QA judgment stay with you.
- Autonomy inside phases, checkpoints between them. Do not ask about things you can look up or decide as a careful art director would.

## Phase 0: Preflight, then resume or start
```bash
python3 .claude/skills/asofex-ios-screenshots/scripts/preflight.py
ls output/*/docs/copy.md 2>/dev/null
```
`preflight.py` reports which image engines are ready (Codex CLI, OpenAI key, Gemini key), whether Pillow, Xcode, and XcodeBuildMCP are present, and how to fix what is missing. Higgsfield is an MCP connector: check for `mcp__*higgsfield*` tools with ToolSearch.

If a docs folder exists for this app, read all three docs and `output/<app>/renders/*/attempts.md`, tell the user what exists, and ask whether this is a revision or a fresh run. A revision edits the docs first, then re-renders only what changed.

## Phase 1: Intake loop
Use AskUserQuestion repeatedly until you are fully confident. Ask in rounds of up to 4 questions, each round informed by the previous answers and by anything you can inspect yourself (source repo, store page, supplied files). Do not ask what you can find out. Typical rounds:

1. What is the app and what do we have: source path, App Store or Play Store URL, landing page URL, brief, existing captures, brand assets (logo, app icon, colors, fonts, existing mascot). Read whatever is given before the next round.
2. Business: who it is for, the one outcome it delivers, pricing model, what proof exists (ratings, users, press, awards), current screenshots' weakness, competitors the user watches.
3. Deliverables: devices (iPhone 6.9" required, iPad 13" if the app runs on iPad), locales (always ask, default en-US), number of screenshots (6 to 10, recommend 8), Dark Mode screen wanted, any must-have or must-not-show screens. Mascot source: existing mascot, the app icon turned into a character, or an invented creature (playbook section 5).
4. Tooling: image engine, offered in this order with only the ready ones selectable as-is (preflight result): Codex CLI (Recommended), OpenAI API key, Gemini API key, Higgsfield (uses credits). Can the app be built and run on the simulator (scheme, demo account or seed data)? Any brand rules (fonts, forbidden colors, tone)?

When confident, restate everything you understood in one message and wait for the user's confirmation. Do not proceed on silence. Record the engine choice in copy.md.

## Phase 2: Research and positioning (writes docs)
Labor goes to agents, judgment stays with you. Run the research sweep exactly as described in `references/research-workflow.md`: the bundled workflow `workflows/asofex-research.js` when the Workflow tool is available, otherwise the same bundles as parallel Agent subagents. Agents return structured JSON only; they never write the docs.

While it runs, view the contact sheets in `gallery/` to calibrate, and use a browser tool yourself only for things the agents cannot return, such as competitor screenshot galleries saved under `output/<app>/research/competitors/`.

When the research result arrives, save it to `output/<app>/research/findings.json`, then follow `references/playbook.md` sections 1 and 2 to write `output/<app>/docs/research.md` and `positioning.md` from `references/doc-templates.md`. Summarize the positioning statement and the one promise to the user, and ask for approval with AskUserQuestion. Fold their answer back into the docs. If the user later adds sources, competitors, or audience hints, re-run research with the new items and merge.

## Phase 3: Copy, storyboard, and mascot arc (writes copy.md)
Follow playbook sections 3, 4, and 5. Write `copy.md` with the storyboard table, rationale, alternates, the mascot design (source, look, palette), and the pose arc (one pose per screen acting out its headline). Present the storyboard (role, headline, subheadline, proof, capture, layout, pose per screen) and ask for approval. Iterate until approved. Every change lands in copy.md.

## Phase 4: Captures
Follow `references/capture.md`. Collect one capture per storyboard screen plus spares, on iPhone 17 Pro Max and, if iPad is in scope, iPad Pro 13-inch. Store in `output/<app>/captures/<device>/`. Record the mapping in copy.md. If a storyboard screen cannot be captured, tell the user and revise the storyboard rather than faking it.

## Phase 5: Screenshot 1 (style lock)
Write `output/<app>/renders/<device>/spec.json` with the mascot direction paragraph (palette hex, ground shapes, typography, accent, device treatment, full mascot description), `"character": true`, and screenshot 1 marked `"first": true`. Generate its prompt with `scripts/make_prompts.py`, render it with `scripts/render.sh` (`references/render.md`), verify, and show it to the user with the file path. Ask for approval or adjustments with AskUserQuestion; iterate until approved. The approved screenshot 1 becomes `renders/<device>/style-ref.png`. Update copy.md.

## Phase 6: Render the set
For each device: complete `spec.json` with every storyboard screen (layout, pose, screen notes), run `scripts/make_prompts.py`, then `scripts/render.sh` per screen with the approved `style-ref.png` in place, inspect, log the attempt, and regenerate (versioned prompt, same script) until each passes all five checks. Run up to 3 renders in parallel with background Bash calls. Then finalize, verify, and build the contact sheet with `scripts/finalize.py`. Read the contact sheet and fix outliers.

Present the set: contact sheet path, per-file paths, and one line per screenshot on what it does. Ask the user for approval or changes. Apply changes to copy.md first, then re-render only affected screens.

## Phase 7: Deliverables
```
output/<app>/
  docs/research.md  docs/positioning.md  docs/copy.md
  iphone-6.9/01.png ... NN.png  (1320x2868, RGB, no alpha)  + _contact-sheet.jpg
  ipad-13/01.png ... NN.png     (2064x2752)                  + _contact-sheet.jpg
  captures/<device>/*.png
  renders/<device>/spec.json  NN.prompt.txt  NN.raw.png  attempts.md  style-ref.png
  research/findings.json  research/competitors/*.png
```
Confirm `finalize.py --verify` passed for every device folder before saying the set is ready. The folders `iphone-6.9/` and `ipad-13/` are what the user drags into App Store Connect. Report what was left out, if anything, and why.

## Locales
If more than en-US was requested: after the English set is approved, add a localization table to copy.md with translated headlines (keep them 2 to 5 words, culturally natural, not literal), ask the user to approve, then re-render each screenshot per locale into `output/<app>/<device>/<locale>/`. UI captures stay in the app's language unless the user provides localized captures.

## Self-Improvement Loop
At the end of every run of this skill, before ending the turn, review the run:
- Did any step fail, need a workaround, or behave differently than this file describes?
- Did the user correct, reject, or meaningfully rework something this skill produced?
- Did you discover something a future run needs (a changed ID, a tool quirk, a better sequence)?

The bar: propose an update ONLY if it would change what a future run actually does, or prevent a repeat of a real mistake. No cosmetic tweaks, no hypothetical improvements, no flagging for the sake of it. Most runs should end with nothing to propose.

If something clears the bar, end the run with:
`Proposed update to this skill: [one line — what changes and why]`
Wait for approval. On approval, edit this SKILL.md (or the relevant file under references/) in place, updating the relevant section. Do not append a changelog.
