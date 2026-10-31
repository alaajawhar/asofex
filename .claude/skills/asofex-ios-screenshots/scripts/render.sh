#!/bin/zsh
# Render one App Store screenshot with the chosen image engine.
# usage: render.sh <render_dir> <NN> <capture.png> [version_suffix]
#   render_dir : folder holding NN.prompt.txt (and style-ref.png once screenshot 1 is approved)
#   NN         : two-digit screen number, e.g. 03
#   capture    : the real UI capture passed as Image 1 ("none" for a screen with no UI)
#   suffix     : optional, e.g. v2 -> reads NNv2.prompt.txt (falls back to NN.prompt.txt), writes NN.rawv2.png
# Engine: $ASOFEX_ENGINE, else the first line of <render_dir>/../engine.txt, else codex.
#   codex  : Codex CLI built-in image_gen (ChatGPT login, no API key). ~1.5 MP, upscaled by finalize.py.
#   openai : OpenAI image API via gen_image.py (OPENAI_API_KEY). Exact sizes, sharpest text.
#   gemini : Gemini image API via gen_image.py (GEMINI_API_KEY). Center-cropped to the iPhone ratio.
#   higgsfield : not scriptable; Claude renders through the Higgsfield MCP tools (references/render.md).
# Attaches style-ref.png as Image 2 when present. Always closes stdin (a backgrounded codex exec hangs otherwise).
set -u
setopt null_glob
R=${1:A}; NN=$2; CAP=$3; SUF=${4:-}
HERE=${0:A:h}
cd "$R" || exit 1
[[ "$CAP" != none ]] && CAP=${CAP:A}
ENGINE=${ASOFEX_ENGINE:-}
[[ -z "$ENGINE" && -f "$R/../engine.txt" ]] && ENGINE=$(head -1 "$R/../engine.txt" | tr -d '[:space:]')
ENGINE=${ENGINE:-codex}
PROMPT="$NN$SUF.prompt.txt"; [ -f "$PROMPT" ] || PROMPT="$NN.prompt.txt"
IMGS=(); [[ "$CAP" != none ]] && IMGS+=("$CAP"); [ -f "$R/style-ref.png" ] && IMGS+=("$R/style-ref.png")
OUT="$R/$NN.raw$SUF.png"

case $ENGINE in
  codex)
    ARGS=(); for i in "${IMGS[@]}"; do ARGS+=(-i "$i"); done
    FULL="Use your built-in image_gen tool to generate ONE image.
$(cat "$PROMPT")
Output: one image. Copy the raw generated PNG, unresized, to ./$NN.raw.png in the current working directory and reply with its absolute path and pixel dimensions."
    codex exec --dangerously-bypass-approvals-and-sandbox -C "$R" "${ARGS[@]}" \
      --output-last-message "$NN$SUF.log.txt" "$FULL" < /dev/null > "$NN$SUF.codex.out" 2>&1
    if [ -n "$SUF" ] && [ -f "$R/$NN.raw.png" ]; then mv "$R/$NN.raw.png" "$OUT"; fi
    tail -c 160 "$NN$SUF.log.txt"; echo ;;
  openai|gemini)
    ARGS=(); for i in "${IMGS[@]}"; do ARGS+=(--image "$i"); done
    python3 "$HERE/gen_image.py" --engine "$ENGINE" --prompt-file "$PROMPT" --out "$OUT" "${ARGS[@]}" \
      < /dev/null > "$NN$SUF.$ENGINE.out" 2>&1
    cat "$NN$SUF.$ENGINE.out" | tail -5 ;;
  higgsfield)
    echo "higgsfield is rendered by Claude through the Higgsfield MCP tools, see references/render.md"; exit 2 ;;
  *)
    echo "unknown engine: $ENGINE (codex|openai|gemini|higgsfield)"; exit 2 ;;
esac
RAWS=("$R"/$NN.raw*.png); (( ${#RAWS} )) && ls -la "${RAWS[@]}"
[ -f "$OUT" ] || { echo "render failed: $OUT not written, see $NN$SUF.*.out / .log.txt"; exit 1; }
