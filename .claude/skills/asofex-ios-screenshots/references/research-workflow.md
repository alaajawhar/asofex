# Research workflow (Phase 2)

The reading is done by a small fleet of Sonnet agents through the workflow bundled with this skill, `.claude/skills/asofex-ios-screenshots/workflows/asofex-research.js`. Each agent gets a bundle of 3 to 8 related sources or queries (one competitor group, all Reddit queries, the app's own pages) and returns one structured object. A run uses about 10 to 16 agents total, never one agent per link. Claude does no bulk reading itself; Claude synthesizes, decides, and writes the docs.

## Invoke
After intake is confirmed and you have read what the user supplied:

```
Workflow({
  scriptPath: ".claude/skills/asofex-ios-screenshots/workflows/asofex-research.js",   // always by path: invoking by name can run a stale cached copy of the script
  args: {
    app: "<App name>",
    category: "<category as a user would say it, e.g. sleep tracker>",
    storeUrl: "<https://apps.apple.com/...>",
    landingUrl: "<https://...>",
    sourcePath: "</abs/path/to/repo>",
    competitors: ["<name or App Store URL>", ...],
    audienceHints: "<short phrase, e.g. new parents, shift workers>",
    knownProof: "<what the user claims: rating, users, press>",
    extraSources: ["<any URLs the user gave>"],
    alreadyCovered: "<optional one-paragraph summary of a previous run's coverage, so the gap agent does not repeat it>",
    maxRounds: 3,
    maxAgents: 16
  }
})
```
Every arg except `app` is optional; supply everything you know. The workflow runs in the background and notifies you when done. Do not poll. While it runs, view the contact sheets in `gallery/` and, if the user supplied a repo, skim its screens list.

## Fallback when the Workflow tool is not available
Some Claude Code setups do not expose the Workflow tool. Then run the same plan with the Agent tool yourself:
1. Build the round-1 bundles listed under "How it runs" from the args (skip bundles with no inputs).
2. Launch one Agent per bundle in a single message so they run in parallel (`subagent_type: general-purpose`, `model: sonnet`, `effort: lower`). Give each the finder brief from `finderPrompt` in the workflow script, its bundle, and the FINDINGS JSON shape from the script; ask for that JSON only.
3. After the round, decide yourself whether a gap round is worth it (at most 4 new bundles, same rules), and stop after `maxRounds` or `maxAgents`.
4. Merge the JSON results into one object with `findings` (array) and `unread` (array) and save it as `findings.json`, then continue as below.

## How it runs
- Round 1 seeds about 8 bundles: the app's own pages (store, landing, extras), store reviews, source code, competitors in groups of 3, keywords plus top charts, all Reddit queries, all forum queries, all blog and press queries.
- Each finder may use WebFetch and WebSearch, and may open its own Chrome tab for blocked pages. It reads its whole bundle plus up to 3 closely related pages, and returns quotes with URLs, pains, outcomes, search phrases, proof with URLs, a competitor profile, conventions, and at most 3 leads.
- After each round one gap agent proposes at most 4 new bundles. Leads are grouped by type into bundles of up to 6. Everything is deduplicated against what was already read.
- The loop ends when two consecutive rounds add nothing new, at `maxRounds` (default 3), or at `maxAgents` (default 16). Anything unread is logged, never dropped silently.

## When it returns
Save the raw result: write it to `output/<app>/research/findings.json`. Then read it and write `docs/research.md` yourself following `doc-templates.md`:
- Prefer verbatim quotes with URLs. Keep the user's language, not yours.
- Proof goes into the proof inventory only with a URL you have opened yourself, or one the user confirmed.
- Competitor matrix from the competitor objects; fill weakness with your own judgment.
- Note unreachable and unread sources in "Open questions" so the user can supply them.
If the result is thin (few sources reached), tell the user which sources failed and ask for alternatives or direct material, then re-run with `extraSources`.

## Re-runs
When the user adds a competitor, a URL, or a new audience hint later, re-run the workflow with only the new items in args (`competitors`, `extraSources`, `audienceHints`) and merge the new findings into research.md the same turn.
