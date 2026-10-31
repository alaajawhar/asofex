#!/usr/bin/env python3
"""Check what this machine can do before an asofex run. Prints one line per check plus a fix hint.

Image engines (at least one must be ready):
  codex   : Codex CLI installed and logged in (ChatGPT plan, no API key needed)
  openai  : OPENAI_API_KEY set
  gemini  : GEMINI_API_KEY or GOOGLE_API_KEY set
  higgsfield : MCP connector, not checkable here; look for mcp__*higgsfield* tools with ToolSearch
Also checks: python3 Pillow (required), Xcode + simulators and Node.js (only for simulator captures).
"""
import os, shutil, subprocess, json

def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)

ok = lambda b: "READY  " if b else "MISSING"
results = {}

try:
    import PIL; pil = True
except ImportError:
    pil = False
print(f"{ok(pil)} Pillow (required)            fix: python3 -m pip install --user Pillow")

codex = shutil.which("codex")
codex_ok = False
if codex:
    rc, out = run(["codex", "login", "status"])
    codex_ok = rc == 0 and "not logged" not in out.lower()
print(f"{ok(codex_ok)} engine codex                  fix: npm install -g @openai/codex && codex login")
openai = bool(os.environ.get("OPENAI_API_KEY"))
print(f"{ok(openai)} engine openai                 fix: export OPENAI_API_KEY=... (model: OPENAI_IMAGE_MODEL, default gpt-image-2)")
gemini = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
print(f"{ok(gemini)} engine gemini                 fix: export GEMINI_API_KEY=... (model: GEMINI_IMAGE_MODEL, default gemini-3-pro-image-preview)")
print("CHECK   engine higgsfield             Claude: ToolSearch \"higgsfield generate_image\"; connect the Higgsfield connector if absent")

import glob
dev = os.environ.get("DEVELOPER_DIR", "")
if not dev:
    rc, dev = run(["xcode-select", "-p"])
xcode = os.path.isdir(dev) and "CommandLineTools" not in dev
exported = False
if not xcode:
    found = sorted(glob.glob("/Applications/Xcode*.app") + glob.glob(os.path.expanduser("~/Applications/Xcode*.app")))
    if found:
        dev = found[0] + "/Contents/Developer"; xcode = exported = True
        os.environ["DEVELOPER_DIR"] = dev
hint = f"   note: export DEVELOPER_DIR={dev} before every xcrun/xcodebuild call" if exported else ""
print(f"{ok(xcode)} Xcode (simulator captures)    DEVELOPER_DIR={dev}" + (hint if xcode else "   fix: install Xcode from the App Store"))
if xcode:
    rc, out = run(["xcrun", "simctl", "list", "devices", "available", "-j"])
    names = set()
    if rc == 0:
        for devs in json.loads(out).get("devices", {}).values():
            names |= {d["name"] + " " + d.get("deviceTypeIdentifier", "").replace("-", " ") for d in devs}
    for want in ("iPhone 17 Pro Max", "iPad Pro 13"):
        hit = any(want in n for n in names)
        print(f"{ok(hit)} simulator {want:<20} fix: Xcode > Settings > Components, add the iOS runtime, then create the device")
node = bool(shutil.which("npx"))
print(f"{ok(node)} Node.js (XcodeBuildMCP via npx) fix: brew install node")

engines = [n for n, b in (("codex", codex_ok), ("openai", openai), ("gemini", gemini)) if b]
print("\nready engines:", ", ".join(engines) or "none (unless Higgsfield is connected)")
