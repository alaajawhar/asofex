#!/usr/bin/env python3
"""Render one screenshot through an image API directly (no Codex). Standard library + Pillow only.

usage:
  gen_image.py --engine openai|gemini --prompt-file 03.prompt.txt --out 03.raw.png \
               [--image capture.png] [--image style-ref.png] [--size 1760x3824] [--quality high]

Images are passed in order, so the first --image is "Image 1" in the prompt, the second is "Image 2".

openai : needs OPENAI_API_KEY. Model from OPENAI_IMAGE_MODEL (default gpt-image-2).
         Uses /v1/images/edits when images are attached, /v1/images/generations otherwise.
         Size defaults from the prompt's "aspect ratio W:H" line: 1760x3824 for iPhone, 2064x2752 for iPad.
gemini : needs GEMINI_API_KEY (or GOOGLE_API_KEY). Model from GEMINI_IMAGE_MODEL
         (default gemini-3-pro-image-preview). Gemini only accepts fixed aspect ratios, so the
         script asks for the closest one (9:16 for iPhone, 3:4 for iPad), tells the model which
         central band survives, and center-crops the result to the exact target ratio.
         The uncropped image is kept as <out>.uncropped.png.
"""
import argparse, base64, json, os, re, sys, urllib.request, urllib.error, uuid
from pathlib import Path

GEMINI_RATIOS = {"1:1": 1.0, "2:3": 2 / 3, "3:4": 0.75, "4:5": 0.8, "9:16": 9 / 16}


def target_ratio(prompt):
    m = re.search(r"aspect ratio (\d+):(\d+)", prompt)
    return (int(m.group(1)) / int(m.group(2))) if m else 1320 / 2868


def http_json(url, body, headers, timeout=600):
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} from {url}: {e.read().decode(errors='replace')[:800]}")


def multipart(fields, files):
    b = uuid.uuid4().hex
    out = bytearray()
    for k, v in fields.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, path in files:
        out += (f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{Path(path).name}"\r\n'
                f"Content-Type: image/png\r\n\r\n").encode()
        out += Path(path).read_bytes() + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={b}"


def openai(prompt, images, size, quality, out):
    key = os.environ.get("OPENAI_API_KEY") or sys.exit("OPENAI_API_KEY is not set")
    model = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
    if not size:
        size = "1760x3824" if target_ratio(prompt) < 0.6 else "2064x2752"
    auth = {"Authorization": f"Bearer {key}"}
    if images:
        body, ctype = multipart({"model": model, "prompt": prompt, "size": size, "quality": quality, "n": "1"},
                                [("image[]", p) for p in images])
        res = http_json("https://api.openai.com/v1/images/edits", body, {**auth, "Content-Type": ctype})
    else:
        body = json.dumps({"model": model, "prompt": prompt, "size": size, "quality": quality, "n": 1}).encode()
        res = http_json("https://api.openai.com/v1/images/generations", body, {**auth, "Content-Type": "application/json"})
    Path(out).write_bytes(base64.b64decode(res["data"][0]["b64_json"]))


def gemini(prompt, images, out):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or sys.exit("GEMINI_API_KEY is not set")
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")
    want = target_ratio(prompt)
    name, have = min(GEMINI_RATIOS.items(), key=lambda kv: abs(kv[1] - want))
    if abs(have - want) / want > 0.02:
        keep = want / have
        prompt += (f"\nCanvas note: this image is generated at {name} and will be center-cropped to aspect ratio "
                   f"{want:.4f}:1, keeping only the central {keep:.0%} of the width. Keep the headline, subheadline, phone, "
                   f"and character entirely inside that central band; only background and ground shapes may extend to the edges.")
    parts = [{"inline_data": {"mime_type": "image/png", "data": base64.b64encode(Path(p).read_bytes()).decode()}} for p in images]
    parts.append({"text": prompt})
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"responseModalities": ["IMAGE"],
                                            "imageConfig": {"aspectRatio": name, "imageSize": "4K"}}}).encode()
    res = http_json(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", body,
                    {"x-goog-api-key": key, "Content-Type": "application/json"})
    data = None
    for c in res.get("candidates", []):
        for part in c.get("content", {}).get("parts", []):
            blob = part.get("inlineData") or part.get("inline_data")
            if blob:
                data = blob["data"]
    if not data:
        sys.exit("Gemini returned no image: " + json.dumps(res)[:800])
    raw = Path(out)
    raw.write_bytes(base64.b64decode(data))
    from PIL import Image
    img = Image.open(raw)
    w, h = img.size
    if abs(w / h - want) / want > 0.02:
        img.save(raw.with_suffix(".uncropped.png"))
        nw = round(h * want) if w / h > want else w
        nh = h if w / h > want else round(w / want)
        l, t = (w - nw) // 2, (h - nh) // 2
        img.crop((l, t, l + nw, t + nh)).save(raw)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True, choices=["openai", "gemini"])
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--image", action="append", default=[])
    ap.add_argument("--size")
    ap.add_argument("--quality", default="high")
    a = ap.parse_args()
    prompt = Path(a.prompt_file).read_text()
    if a.engine == "openai":
        openai(prompt, a.image, a.size, a.quality, a.out)
    else:
        gemini(prompt, a.image, a.out)
    from PIL import Image
    print(Path(a.out).resolve(), "x".join(map(str, Image.open(a.out).size)))
