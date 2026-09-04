#!/usr/bin/env python3
"""
Strip white background from a pack JPG → transparent PNG.
Used before uploading pack images to Figma so packs sit cleanly on coloured cards.

Usage:
    python3 strip_white_bg.py <input.jpg> <output.png> [--threshold 235]
"""
import sys
from pathlib import Path

def strip(src: Path, dst: Path, threshold: int = 235):
    from PIL import Image
    im = Image.open(src).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > threshold and g > threshold and b > threshold:
                px[x, y] = (r, g, b, 0)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "PNG")
    print(f"saved {dst}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    threshold = 235
    if "--threshold" in sys.argv:
        threshold = int(sys.argv[sys.argv.index("--threshold") + 1])
    strip(src, dst, threshold)
