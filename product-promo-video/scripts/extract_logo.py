#!/usr/bin/env python3
"""从官方宣传图（og-image、发布会主视觉）里抠出 logo，存成透明底 PNG。
官网找不到 SVG、logo 只出现在一张大图里时用。抠出来的仍是官方 logo，不是重画的。

用法:
  python3 extract_logo.py og.png logo.png --mode white   [--box x0,y0,x1,y1] [--pad 20]
  python3 extract_logo.py og.png logo.png --mode on-dark [--box ...]
mode:
  white    彩色/渐变背景上的白色 logo：接近白色的像素保留为白色，其余透明
  on-dark  黑色背景上的彩色 logo：亮度当作透明度，保留原色（适合发光、渐变字）
  on-light 白色背景上的深色/彩色 logo：与白色的差异当作透明度
box 是在原图上的裁剪范围（像素），不给就自动按有内容的区域裁。
"""
import argparse
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--mode", choices=["white", "on-dark", "on-light"], required=True)
ap.add_argument("--box"); ap.add_argument("--pad", type=int, default=16)
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
if a.box: im = im.crop(tuple(int(v) for v in a.box.split(",")))
rgb = np.asarray(im).astype(np.float32) / 255
mx, mn = rgb.max(2), rgb.min(2)

if a.mode == "white":
    # 白：最暗通道要高，且饱和度低
    alpha = np.clip((mn - .78) / .17, 0, 1) * np.clip(1 - (mx - mn - .06) / .2, 0, 1)
    color = np.ones_like(rgb)
elif a.mode == "on-dark":
    alpha = np.clip((mx - .08) / .55, 0, 1)
    color = np.clip(rgb / np.maximum(alpha[..., None], 1e-3), 0, 1)
else:
    alpha = np.clip(((1 - mn) - .06) / .5, 0, 1)
    color = np.clip(1 - (1 - rgb) / np.maximum(alpha[..., None], 1e-3), 0, 1)

alpha = np.where(alpha < .18, 0, alpha)   # 去掉背景里的淡色光斑
out = np.dstack([color, alpha])
ys, xs = np.where(alpha > .1)
if len(xs) == 0: raise SystemExit("没抠到东西，换个 mode 或调整 box")
y0, y1, x0, x1 = max(ys.min() - a.pad, 0), ys.max() + a.pad, max(xs.min() - a.pad, 0), xs.max() + a.pad
Image.fromarray((out[y0:y1, x0:x1] * 255).astype(np.uint8), "RGBA").save(a.out)
print(f"logo {x1 - x0}×{y1 - y0} → {a.out}")
