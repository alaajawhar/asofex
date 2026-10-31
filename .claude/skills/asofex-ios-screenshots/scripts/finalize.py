#!/usr/bin/env python3
"""Finalize App Store screenshots: exact size, RGB, no alpha, plus a contact sheet.

Usage:
  finalize.py --size 1260x2736 --out-dir output/<app>/iphone-6.9 raw/01.png raw/02.png ...
  finalize.py --verify output/<app>/iphone-6.9        # check every PNG in a folder
  finalize.py --contact-sheet output/<app>/iphone-6.9  # writes _contact-sheet.jpg next to them

Resizing: the raw image is scaled to cover the target box (LANCZOS), then center-cropped.
Aspect drift larger than --max-drift (default 2%) is an error: regenerate instead of cropping.
"""
import argparse, sys, os
from pathlib import Path
from PIL import Image

def parse_size(s):
    w, h = s.lower().split("x"); return int(w), int(h)

def fit_cover(img, tw, th, max_drift):
    w, h = img.size
    src_ratio, dst_ratio = w / h, tw / th
    drift = abs(src_ratio - dst_ratio) / dst_ratio
    if drift > max_drift:
        raise SystemExit(f"aspect drift {drift:.1%} > {max_drift:.0%} for {w}x{h} -> {tw}x{th}; regenerate at the right ratio")
    scale = max(tw / w, th / h)
    nw, nh = round(w * scale), round(h * scale)
    img = img.resize((max(nw, tw), max(nh, th)), Image.Resampling.LANCZOS)
    l, t = (img.width - tw) // 2, (img.height - th) // 2
    return img.crop((l, t, l + tw, t + th))

def finalize(paths, size, out_dir, max_drift, start):
    tw, th = parse_size(size); out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(paths, start=start):
        img = Image.open(p)
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255)); rgba = img.convert("RGBA")
            bg.paste(rgba, mask=rgba.split()[-1]); img = bg
        img = img.convert("RGB")
        if img.size != (tw, th):
            img = fit_cover(img, tw, th, max_drift)
        out = out_dir / f"{i:02d}.png"; img.save(out, "PNG", optimize=True)
        print(f"{p} -> {out} {img.size[0]}x{img.size[1]} RGB")

def verify(folder, size=None):
    ok = True; files = sorted(Path(folder).glob("[0-9][0-9].png"))
    if not files: print("no NN.png files found"); return False
    if not (6 <= len(files) <= 10): print(f"WARN: {len(files)} screenshots (want 6-10, Apple max 10)")
    sizes = set()
    for f in files:
        img = Image.open(f); sizes.add(img.size)
        bad = []
        if img.mode != "RGB": bad.append(f"mode={img.mode}")
        if size and img.size != parse_size(size): bad.append(f"size={img.size}")
        if f.stat().st_size > 8 * 1024 * 1024: bad.append("over 8MB")
        print(f"{f.name}: {img.size[0]}x{img.size[1]} {img.mode} {'OK' if not bad else 'FAIL ' + ', '.join(bad)}")
        ok &= not bad
    if len(sizes) > 1: print(f"FAIL: mixed sizes {sizes}"); ok = False
    print("VERIFY", "PASS" if ok else "FAIL"); return ok

def contact_sheet(folder, height=900, gap=24):
    files = sorted(Path(folder).glob("[0-9][0-9].png"))
    thumbs = []
    for f in files:
        img = Image.open(f).convert("RGB"); r = height / img.height
        thumbs.append(img.resize((round(img.width * r), height), Image.Resampling.LANCZOS))
    W = sum(t.width for t in thumbs) + gap * (len(thumbs) + 1)
    sheet = Image.new("RGB", (W, height + 2 * gap), (245, 245, 245)); x = gap
    for t in thumbs: sheet.paste(t, (x, gap)); x += t.width + gap
    out = Path(folder) / "_contact-sheet.jpg"; sheet.save(out, "JPEG", quality=88); print(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="*"); ap.add_argument("--size"); ap.add_argument("--out-dir")
    ap.add_argument("--start", type=int, default=1); ap.add_argument("--max-drift", type=float, default=0.02)
    ap.add_argument("--verify"); ap.add_argument("--contact-sheet")
    a = ap.parse_args()
    if a.verify: sys.exit(0 if verify(a.verify, a.size) else 1)
    elif a.contact_sheet: contact_sheet(a.contact_sheet)
    elif a.inputs and a.size and a.out_dir: finalize(a.inputs, a.size, a.out_dir, a.max_drift, a.start)
    else: ap.print_help(); sys.exit(2)
