# Getting real UI captures

Real captures are mandatory. Never render a screenshot whose UI is invented.

## Path A: user provides captures
Accept PNG or JPG at device resolution. Store copies in output/<app>/captures/ named by screen purpose (home.png, session.png, stats.png). Check each one: no personal data, no debug overlays, status bar clean (9:41, full battery, full signal). If status bar is dirty, ask the user for a re-capture or proceed with the simulator path.

## Path B: build from source and capture on the simulator
Needs Xcode with an iOS simulator runtime. `xcode-select -p` must point at a full Xcode (not CommandLineTools); if Xcode lives somewhere non-standard, export `DEVELOPER_DIR=<Xcode.app>/Contents/Developer` before every Bash command (preflight.py prints the value it found).

```bash
xcodebuild -list -project App.xcodeproj            # or -workspace App.xcworkspace
xcrun simctl list devices available | grep -E "iPhone 17 Pro Max|iPad Pro 13"
xcrun simctl boot "<UDID>"
xcodebuild -scheme <Scheme> -destination "platform=iOS Simulator,id=<UDID>" -configuration Debug -derivedDataPath build build
xcrun simctl install <UDID> build/Build/Products/Debug-iphonesimulator/<App>.app
xcrun simctl status_bar <UDID> override --time "9:41" --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
xcrun simctl launch <UDID> <bundle.id>
xcrun simctl io <UDID> screenshot output/<app>/captures/home.png
```

Use iPhone 17 Pro Max for iPhone captures and iPad Pro 13-inch for iPad captures so the UI is native to the target size.

## Navigating the app: XcodeBuildMCP
The XcodeBuildMCP server is declared in the repo root `.mcp.json` (runs through `npx -y xcodebuildmcp@latest`, so only Node.js is needed) (workflows: simulator, simulator-management, ui-automation, project-discovery, utilities). It loads when Claude Code starts in this directory; if its tools are missing, restart the session here and approve the project MCP server. Load its tools with ToolSearch, for example `select:mcp__xcodebuildmcp__snapshot_ui,mcp__xcodebuildmcp__tap,mcp__xcodebuildmcp__screenshot,mcp__xcodebuildmcp__type_text,mcp__xcodebuildmcp__swipe,mcp__xcodebuildmcp__build_run_sim,mcp__xcodebuildmcp__list_sims`. Exact tool prefix may differ, search "xcodebuildmcp" if select fails.

Fallback when the MCP tools are not loaded in the session (server added after start): the same tools exist as a CLI (`npx -y xcodebuildmcp@latest ...` if not installed globally), e.g. `xcodebuildmcp ui-automation snapshot-ui --simulator-id <UDID>`, `... tap --element-ref e12`, `... type-text --element-ref e21 --text "x" --replace-existing`, `... button --button-type lock`, `... gesture --preset swipe-from-bottom-edge`. Never store a multi-word command in a zsh variable (`X="xcodebuildmcp ui-automation"; $X tap` fails silently as "command not found"); write the full command or a shell function. The `@` key types as `2` on the first try: retype with `--replace-existing` and verify the field value in the snapshot.

Lock screen captures: `button --button-type lock`, then `xcrun simctl push <UDID> <bundle> payload.json` (aps.alert title/body must match what the backend sends), screenshot immediately (the first frame has no "Swipe up to open" hint). To get back into the app, `xcrun simctl launch <UDID> <bundle>` is the only reliable unlock; home, lock toggle, and swipe-from-bottom do not dismiss the cover sheet.

Flow: `build_run_sim` (or the Bash path above), then loop `snapshot_ui` to read elementRefs, `tap` / `type_text` / `swipe` to reach the screen, `screenshot` to capture. Set appearance with `set_sim_appearance` for a Dark Mode capture. Prefer seeded demo data: ask the user for a demo account or a debug flag that fills the app with realistic content. Empty states do not sell.

## Capture checklist
- One capture per storyboard screen, plus 2 spares of the most visual screens.
- Content is realistic and flattering: real-looking names, full charts, no lorem ipsum.
- Same appearance (light or dark) across the set unless a Dark Mode screen is planned.
- Record which capture maps to which storyboard screen in copy.md.
