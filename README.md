# asofex

App Store Optimization toolkit for [Claude Code](https://claude.com/claude-code). The first skill, **asofex-ios-screenshots**, produces a complete, upload-ready set of 6 to 10 App Store screenshots for iPhone and iPad in one mascot-led style. Each screenshot shows real UI from your app. Every set goes through research, positioning and copy before rendering, and every image is checked before it ships.

![Alarmifex example set](.claude/skills/asofex-ios-screenshots/gallery/alarmifex/iphone-6.9/_contact-sheet.jpg)
![Notifex example set](.claude/skills/asofex-ios-screenshots/gallery/notifex/iphone-6.9/_contact-sheet.jpg)
![Ideafex example set](.claude/skills/asofex-ios-screenshots/gallery/ideafex/iphone-6.9/_contact-sheet.jpg)

## Quickstart

```bash
git clone https://github.com/alaajawhar/asofex.git
cd asofex
claude
```

Then type in Claude Code:

```
/asofex-ios-screenshots make App Store screenshots for my app at ~/code/myapp
```

Claude interviews you, then runs every phase. It stops for your approval at five checkpoints:

1. **Intake.** Claude asks about the app, your audience, your proof, the devices, the locales and the image engine.
2. **Research and positioning.** Agents read your store page, your competitors, reviews and Reddit. Claude writes `research.md` and `positioning.md` for you to approve.
3. **Copy and storyboard.** Claude writes the headlines and the screen order, designs the mascot, and writes one pose per screen into `copy.md`.
4. **Captures and screenshot 1.** Claude takes real captures on the simulator, renders the hook screenshot, and asks you to approve its style.
5. **Full set.** Claude renders every screen against the approved style, checks each one (text, UI fidelity, composition, consistency, aspect), and exports exact App Store Connect sizes.

Output lands in `output/<app>/`. Drag `iphone-6.9/` (1320x2868) and `ipad-13/` (2064x2752) into App Store Connect.

## Requirements

| Need | For | Install |
|---|---|---|
| Claude Code | everything | https://claude.com/claude-code |
| Python 3 + Pillow | prompts, export, checks | `python3 -m pip install --user Pillow` |
| One image engine | rendering | see below |
| Xcode + iOS simulators (iPhone 17 Pro Max, iPad Pro 13") | real UI captures (skip if you supply captures) | Mac App Store |
| Node.js | XcodeBuildMCP simulator control, started from `.mcp.json` | `brew install node` |

Image engines. Pick one during intake:

| Engine | Setup | Notes |
|---|---|---|
| Codex CLI (default) | `npm i -g @openai/codex && codex login` | Uses your ChatGPT plan. No API key needed. |
| OpenAI API | `export OPENAI_API_KEY=...` | Exact sizes and the sharpest text. Change the model with `OPENAI_IMAGE_MODEL`. |
| Gemini API | `export GEMINI_API_KEY=...` | Change the model with `GEMINI_IMAGE_MODEL`. |
| Higgsfield | connect the Higgsfield MCP connector | Uses Higgsfield credits. |

To see what is ready on your machine, run:

```bash
python3 .claude/skills/asofex-ios-screenshots/scripts/preflight.py
```

## Layout

```
.mcp.json                                   XcodeBuildMCP for simulator captures
.claude/skills/asofex-ios-screenshots/
  SKILL.md                                  the workflow Claude follows
  references/                               specs, playbook, capture, render, research, doc templates
  scripts/                                  preflight, make_prompts, render.sh, gen_image (OpenAI/Gemini), finalize
  workflows/asofex-research.js              parallel research sweep
  gallery/                                  three shipped example sets with their docs, specs, and prompts
```

## License

MIT. The gallery screenshots show the author's own apps and are included for reference only. See [LICENSE](LICENSE).
