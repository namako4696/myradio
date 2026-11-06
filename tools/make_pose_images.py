#!/usr/bin/env python3
"""Build transparent pose images for the atsutama caster from the white-background cuts.

Usage: python3 tools/make_pose_images.py <source-dir> <out-dir>
The source cuts (624x464, white background) are keyed by the rule
"low saturation + bright = background", which fits this character
(yellow body = saturated, black ribbon/limbs = dark). Only the largest
connected character component is kept, so slivers of neighbouring poses
left at the edges of a cut are dropped. Faint ground shadow is kept as a
low-alpha black so it still reads as a shadow on the dark stage.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def key(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    a = np.array(im).astype(np.int16)
    mn, mx = a.min(axis=2), a.max(axis=2)
    sat = mx - mn
    bg = (sat < 35) & (mn > 175)                 # white / light-grey background
    char = ~bg
    lab, n = ndimage.label(char)
    removed = np.zeros(mn.shape, bool)
    if n > 1:
        sizes = ndimage.sum_labels(char, lab, range(1, n + 1))
        main = 1 + int(np.argmax(sizes))
        keep = ndimage.binary_dilation(lab == main, iterations=3)
        removed = ~keep
        bg = bg | removed
    alpha = np.full(mn.shape, 255, dtype=np.float32)
    alpha[bg] = np.clip((255 - mn[bg]) * 1.5, 0, 55)   # faint shadow stays faint
    alpha[removed] = 0                                # neighbour-pose slivers vanish
    rgba = np.dstack([np.array(im), alpha.astype(np.uint8)])
    rgba[bg, 0:3] = 0
    out = Image.fromarray(rgba, "RGBA")
    r, g, b, al = out.split()
    return Image.merge("RGBA", (r, g, b, al.filter(ImageFilter.GaussianBlur(0.5))))

def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for p in sorted(src.glob("*.png")):
        key(p).save(out / p.name)
        print("keyed", p.name)

if __name__ == "__main__":
    main()
