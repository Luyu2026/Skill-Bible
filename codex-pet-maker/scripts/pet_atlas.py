#!/usr/bin/env python3
"""Utilities for packaging Codex custom pet sprite sheets.

The Codex desktop pet picker expects an 8 x 9 atlas at 1536 x 1872 px.
Each frame is 192 x 208 px. This script cleans common image generation
artifacts, validates pet folders, and fixes left/right row orientation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover - only hit in missing envs.
    raise SystemExit(
        "Pillow is required. Install it with `python3 -m pip install Pillow` "
        "or run this script in the Codex bundled Python runtime."
    ) from exc


COLS = 8
ROWS = 9
CELL_W = 192
CELL_H = 208
ATLAS_W = COLS * CELL_W
ATLAS_H = ROWS * CELL_H
MIN_COMPONENT_AREA = 18


@dataclass
class Component:
    bbox: tuple[int, int, int, int]
    area: int
    cx: float
    cy: float


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def is_fake_background_pixel(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    if a < 8:
        return True
    bright_neutral = max(r, g, b) - min(r, g, b) <= 20 and (r + g + b) / 3 >= 198
    return bright_neutral


def clean_border_background(image: Image.Image) -> Image.Image:
    """Remove white/checkerboard-like background connected to the border."""
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size
    seen = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def enqueue(x: int, y: int) -> None:
        idx = y * width + x
        if not seen[idx] and is_fake_background_pixel(pixels[x, y]):
            seen[idx] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height:
                enqueue(nx, ny)

    for y in range(height):
        for x in range(width):
            if seen[y * width + x]:
                r, g, b, _ = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
    return image


def alpha_mask_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox()


def component_list(image: Image.Image) -> list[Component]:
    alpha = image.getchannel("A")
    width, height = image.size
    data = alpha.load()
    seen = bytearray(width * height)
    components: list[Component] = []

    for start_y in range(height):
        for start_x in range(width):
            idx = start_y * width + start_x
            if seen[idx] or data[start_x, start_y] <= 8:
                continue
            seen[idx] = 1
            queue = deque([(start_x, start_y)])
            min_x = max_x = start_x
            min_y = max_y = start_y
            area = 0
            sum_x = 0
            sum_y = 0

            while queue:
                x, y = queue.popleft()
                area += 1
                sum_x += x
                sum_y += y
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if not (0 <= nx < width and 0 <= ny < height):
                        continue
                    nidx = ny * width + nx
                    if seen[nidx] or data[nx, ny] <= 8:
                        continue
                    seen[nidx] = 1
                    queue.append((nx, ny))

            if area >= MIN_COMPONENT_AREA:
                components.append(
                    Component(
                        bbox=(min_x, min_y, max_x + 1, max_y + 1),
                        area=area,
                        cx=sum_x / area,
                        cy=sum_y / area,
                    )
                )
    return components


def row_fit_limits(row: int) -> tuple[int, int, int]:
    """Return max width, max height, and y bias for a zero-based row."""
    limits = {
        1: (170, 146, 8),
        2: (170, 146, 8),
        4: (166, 166, 2),
        5: (166, 166, 0),
        6: (176, 150, 8),
        7: (154, 166, 6),
        8: (176, 154, 6),
    }
    return limits.get(row, (158, 166, 0))


def nearest_cell(component: Component) -> tuple[int, int]:
    col = min(COLS - 1, max(0, int(component.cx // CELL_W)))
    row = min(ROWS - 1, max(0, int(component.cy // CELL_H)))
    return row, col


def repack_to_grid(image: Image.Image) -> Image.Image:
    """Place each generated frame back into its expected atlas cell.

    Image models often leak a fragment from a neighboring frame into the next
    cell. Grouping visible components by nearest cell removes those shadows
    while preserving accessory marks inside the same frame.
    """
    image = image.convert("RGBA")
    output = Image.new("RGBA", (ATLAS_W, ATLAS_H), (255, 255, 255, 0))
    groups: dict[tuple[int, int], list[Component]] = {}

    for comp in component_list(image):
        width = comp.bbox[2] - comp.bbox[0]
        height = comp.bbox[3] - comp.bbox[1]
        if comp.area < 35 and (width <= 3 or height <= 3):
            continue
        groups.setdefault(nearest_cell(comp), []).append(comp)

    for row in range(ROWS):
        for col in range(COLS):
            comps = groups.get((row, col), [])
            if not comps:
                continue
            left = min(comp.bbox[0] for comp in comps)
            top = min(comp.bbox[1] for comp in comps)
            right = max(comp.bbox[2] for comp in comps)
            bottom = max(comp.bbox[3] for comp in comps)
            frame = image.crop((left, top, right, bottom))
            bbox = alpha_mask_bbox(frame)
            if bbox is None:
                continue
            frame = frame.crop(bbox)

            max_w, max_h, y_bias = row_fit_limits(row)
            scale = min(max_w / frame.width, max_h / frame.height, 1.0)
            new_w = max(1, int(round(frame.width * scale)))
            new_h = max(1, int(round(frame.height * scale)))
            if (new_w, new_h) != frame.size:
                frame = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)

            x = col * CELL_W + (CELL_W - frame.width) // 2
            y = row * CELL_H + (CELL_H - frame.height) // 2 + y_bias
            y = max(row * CELL_H, min(y, (row + 1) * CELL_H - frame.height))
            output.alpha_composite(frame, (x, y))

    return output


def add_grid_check(image: Image.Image, out_path: Path) -> None:
    check = Image.new("RGBA", image.size, (255, 255, 255, 255))
    check.alpha_composite(image)
    draw = ImageDraw.Draw(check)
    for x in range(0, ATLAS_W + 1, CELL_W):
        draw.line((x, 0, x, ATLAS_H), fill=(255, 0, 0, 120), width=1)
    for y in range(0, ATLAS_H + 1, CELL_H):
        draw.line((0, y, ATLAS_W, y), fill=(255, 0, 0, 120), width=1)
    draw.text((6, CELL_H + 6), "row 2: RIGHT movement, character faces RIGHT", fill=(255, 0, 0, 255))
    draw.text((6, CELL_H * 2 + 6), "row 3: LEFT movement, character faces LEFT", fill=(255, 0, 0, 255))
    check.convert("RGB").save(out_path)


def atomic_save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_pet_json(out_dir: Path, pet_id: str, display_name: str, description: str) -> None:
    data = {
        "id": pet_id,
        "displayName": display_name,
        "description": description,
        "spritesheetPath": "spritesheet.png",
        "frameWidth": CELL_W,
        "frameHeight": CELL_H,
        "columns": COLS,
        "rows": ROWS,
    }
    (out_dir / "pet.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate_pet_dir(pet_dir: Path) -> list[str]:
    errors: list[str] = []
    pet_json = pet_dir / "pet.json"
    if not pet_json.exists():
        return [f"missing {pet_json}"]

    try:
        data = json.loads(pet_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid pet.json: {exc}"]

    sprite_name = data.get("spritesheetPath", "spritesheet.png")
    sprite_path = pet_dir / sprite_name
    if not sprite_path.exists():
        errors.append(f"missing sprite sheet: {sprite_path}")
        return errors

    image = load_rgba(sprite_path)
    if image.size != (ATLAS_W, ATLAS_H):
        errors.append(f"sprite size is {image.size}, expected {(ATLAS_W, ATLAS_H)}")
    for key, expected in {
        "frameWidth": CELL_W,
        "frameHeight": CELL_H,
        "columns": COLS,
        "rows": ROWS,
    }.items():
        if int(data.get(key, expected)) != expected:
            errors.append(f"{key} is {data.get(key)}, expected {expected}")

    alpha = image.getchannel("A")
    if alpha.getextrema()[0] == 255:
        errors.append("sprite sheet has no transparent pixels")
    corner_alpha = [image.getpixel((x, y))[3] for x, y in ((0, 0), (ATLAS_W - 1, 0), (0, ATLAS_H - 1))]
    if max(corner_alpha) > 10:
        errors.append("sprite sheet corners are not transparent; clean fake backgrounds first")

    return errors


def command_package(args: argparse.Namespace) -> int:
    source = load_rgba(Path(args.input))
    if source.size != (ATLAS_W, ATLAS_H):
        source = source.resize((ATLAS_W, ATLAS_H), Image.Resampling.LANCZOS)
    clean = clean_border_background(source)
    final = repack_to_grid(clean) if args.repack else clean

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    atomic_save_png(final, out_dir / "spritesheet.png")
    atomic_save_png(final, out_dir / "spritesheet-clean.png")
    add_grid_check(final, out_dir / "spritesheet-grid-check.png")
    write_pet_json(out_dir, args.id, args.display_name, args.description)

    errors = validate_pet_dir(out_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK packaged {out_dir}")
    if args.install:
        install_pet(out_dir, Path(args.pets_root).expanduser())
    return 0


def command_validate(args: argparse.Namespace) -> int:
    pet_dir = Path(args.pet_dir)
    errors = validate_pet_dir(pet_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK {pet_dir}")
    return 0


def command_flip_rows(args: argparse.Namespace) -> int:
    pet_dir = Path(args.pet_dir)
    sprite_path = pet_dir / "spritesheet-clean.png"
    if not sprite_path.exists():
        data = json.loads((pet_dir / "pet.json").read_text(encoding="utf-8"))
        sprite_path = pet_dir / data.get("spritesheetPath", "spritesheet.png")
    image = load_rgba(sprite_path)
    if image.size != (ATLAS_W, ATLAS_H):
        raise SystemExit(f"{sprite_path} must be {(ATLAS_W, ATLAS_H)}, got {image.size}")

    output = image.copy()
    for row_number in args.rows:
        row = row_number - 1
        if not 0 <= row < ROWS:
            raise SystemExit(f"row must be 1-{ROWS}: {row_number}")
        for col in range(COLS):
            box = (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
            frame = output.crop(box).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            output.paste(frame, box)

    atomic_save_png(output, pet_dir / "spritesheet.png")
    atomic_save_png(output, pet_dir / "spritesheet-clean.png")
    add_grid_check(output, pet_dir / "spritesheet-grid-check.png")
    errors = validate_pet_dir(pet_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK flipped rows {', '.join(map(str, args.rows))} in {pet_dir}")
    return 0


def install_pet(pet_dir: Path, pets_root: Path) -> None:
    target = pets_root / pet_dir.name
    pets_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(pet_dir, target, dirs_exist_ok=True)
    print(f"OK installed {target}")


def command_install(args: argparse.Namespace) -> int:
    pet_dir = Path(args.pet_dir)
    errors = validate_pet_dir(pet_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    install_pet(pet_dir, Path(args.pets_root).expanduser())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    package = subparsers.add_parser("package", help="create a pet folder from a generated atlas")
    package.add_argument("--input", required=True, help="input generated atlas image")
    package.add_argument("--out-dir", required=True, help="output pet folder")
    package.add_argument("--id", required=True, help="stable pet id")
    package.add_argument("--display-name", required=True, help="name shown in Codex")
    package.add_argument("--description", required=True, help="description shown in Codex")
    package.add_argument("--repack", action="store_true", help="recenter frames into strict grid cells")
    package.add_argument("--install", action="store_true", help="also copy the pet into ~/.codex/pets")
    package.add_argument("--pets-root", default="~/.codex/pets", help="install target root")
    package.set_defaults(func=command_package)

    validate = subparsers.add_parser("validate", help="validate an existing pet folder")
    validate.add_argument("--pet-dir", required=True)
    validate.set_defaults(func=command_validate)

    flip = subparsers.add_parser("flip-rows", help="mirror each frame in one or more rows")
    flip.add_argument("--pet-dir", required=True)
    flip.add_argument("--rows", type=int, nargs="+", required=True, help="1-based rows to mirror")
    flip.set_defaults(func=command_flip_rows)

    install = subparsers.add_parser("install", help="copy a pet folder into ~/.codex/pets")
    install.add_argument("--pet-dir", required=True)
    install.add_argument("--pets-root", default="~/.codex/pets")
    install.set_defaults(func=command_install)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
