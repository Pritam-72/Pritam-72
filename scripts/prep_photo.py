"""
Prepare the source image (Luffy Gear 5 illustration) for clean ASCII conversion:
  1. Remove the solid background by color distance from the corners.
  2. Crop square and center on the subject with comfortable padding.
  3. Output: source-prepped.png (RGBA), consumed by make_ascii_svg.py.

    python scripts/prep_photo.py [input.png] [output.png]
"""
import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

im = Image.open(INP).convert("RGBA")
arr = np.array(im)

# Detect background color from top-left corner
bg_color = arr[0, 0, :3].astype(float)
dist = np.linalg.norm(arr[:, :, :3].astype(float) - bg_color, axis=-1)
# Create clean alpha mask
alpha = np.where(dist < 26, 0, 255).astype(np.uint8)
arr[:, :, 3] = alpha

# Find bounding box around subject
ys, xs = np.where(alpha > 0)
cx = (xs.min() + xs.max()) // 2
cy = (ys.min() + ys.max()) // 2
side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 32

sx0 = max(0, cx - side // 2)
sy0 = max(0, cy - side // 2)
sx1 = min(im.width, sx0 + side)
sy1 = min(im.height, sy0 + side)

cropped = Image.fromarray(arr).crop((sx0, sy0, sx1, sy1))
cropped.save(OUT)
print(f"wrote {OUT}: {cropped.size} (RGBA)")
