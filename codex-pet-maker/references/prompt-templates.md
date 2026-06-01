# Prompt Templates

Use these as starting points. Keep the user's requested identity and style above the template when they provide references.

Important production rule: final pet artwork should come from image generation, not programmatic drawing. Use scripts only after the artwork exists, for packaging, cleanup, validation, direction fixes, or small bad-cell repairs.

## Pig Hero Mascot

```text
Create a Codex-compatible 8-column by 9-row chibi pig hero spritesheet.
Character: glossy red-suited pig hero mascot, red helmet/hood, yellow eye patches on helmet, yellow wrist bands, yellow pig emblem on belly, pink snout and cheeks, small ears, big friendly eyes.
Canvas: exactly 1536x1872 if possible, each frame fits a 192x208 cell.
Rows:
1 idle standing, blink, breathing;
2 side movement facing right, clean loop;
3 side movement facing left, clean loop;
4 greeting/waving;
5 happy celebration/jump;
6 error/confused, first two frames holding ERROR sign;
7 progress bars labeled exactly 0%, 20%, 40%, 60%, 80%, 100%, 100%, 100%;
8 front-facing walk/patrol;
9 sitting with small dark laptop, typing/blinking.
Critical quality: one pig per cell, no ghosting, no afterimages, no duplicate silhouettes, no motion trails, no shadows, no cropped limbs, no cell bleeding.
Background: transparent if possible, otherwise flat removable light checker-free background.
```

## Pet Photo Cat

```text
Create a Codex-compatible 8-column by 9-row chibi cat spritesheet from the reference cat photos.
Preserve key traits: coat colors and markings, eye color, face shape, tail type, body softness, and the cat's general expression.
Canvas: exactly 1536x1872 if possible, each frame fits a 192x208 cell.
Rows:
1 seated idle, slow blink, ear twitch, tail curl;
2 side-walk movement facing right, paws alternating;
3 side-walk or trot movement facing left, paws alternating;
4 paw raise / attention / tiny meow;
5 cat-specific play, roll, loaf, stretch, or pounce;
6 error/confused, first two frames holding ERROR sign;
7 progress bars labeled exactly 0%, 20%, 40%, 60%, 80%, 100%, 100%, 100%;
8 front-facing walk toward viewer;
9 keyboard/laptop cat, paw tapping or sleepy blink.
Critical quality: one cat per cell, no ghosting, no afterimages, no duplicate silhouettes, no cropped ears/tail/paws, no cell bleeding.
Background: transparent if possible, otherwise flat removable light checker-free background.
```

## Pet Photo Dog

```text
Create a Codex-compatible 8-column by 9-row soft chibi dog spritesheet from the reference dog photo.
Style anchor: match the existing cat pet spritesheets, especially cream-orange-cat-coder and tuxedo-cat-coder: delicate fluffy fur edges, soft watercolor-like semi-3D sticker volume, gentle shading, warm highlights, big expressive eyes, cute rounded proportions.
Identity anchor: use the reference dog photo for breed traits: coat colors and markings, ear shape, tail type, face mask or muzzle color, body proportions, and the dog's general expression.
Avoid program-drawn vector art, pixel art, hard icon outlines, flat emoji style, jagged edges, and geometric blocky bodies.
Canvas: exactly 1536x1872 if possible, each frame fits a 192x208 cell.
Rows:
1 seated idle, blink, breathing;
2 side-run or side-walk movement facing right, paws alternating;
3 side-run or side-walk movement facing left, paws alternating;
4 paw raise / greeting;
5 happy jump or playful bounce;
6 error/confused, first two frames holding ERROR sign;
7 progress bars labeled exactly 0%, 20%, 40%, 60%, 80%, 100%, 100%, 100%;
8 front-facing walk toward viewer;
9 sitting with small dark laptop, typing/blinking.
Critical quality: one dog per cell, no ghosting, no afterimages, no duplicate silhouettes, no motion trails, no cropped ears/tail/paws, no cell bleeding.
Background: transparent if possible, otherwise flat removable light checker-free background.
```

## Pet Photo Rabbit / White Fur Pet

```text
Create a Codex-compatible 8-column by 9-row soft chibi rabbit spritesheet from the reference rabbit photo.
Style anchor: match the existing soft cat pet spritesheets: fluffy fur edges, gentle semi-3D sticker volume, soft shadows, bright round eyes, cute rounded proportions, clean readable silhouette.
Identity anchor: preserve the reference rabbit's white fluffy fur, tall upright ears with soft pink inner ears, round cheeks, tiny pink nose, compact body, small paws, and gentle curious expression.
Canvas: exactly 1536x1872 if possible, each frame fits a 192x208 cell.
Rows:
1 seated idle, blink, ear twitch;
2 side-hop movement facing right, paws alternating;
3 side-hop movement facing left, paws alternating;
4 paw raise / attention;
5 happy hop, tiny spin, or playful bounce;
6 error/confused, first two frames holding ERROR sign;
7 progress bars labeled exactly 0%, 20%, 40%, 60%, 80%, 100%, 100%, 100%;
8 front-facing hop toward viewer;
9 sitting with small dark laptop, paw typing/blinking.
Critical quality: one rabbit per cell, no ghosting, no afterimages, no duplicate silhouettes, no motion trails, no cropped ears/paws, no cell bleeding.
Background: transparent if possible. If transparent output is unreliable, use a flat removable pale cyan/blue background, not white and not checkerboard, so white fur is preserved during cleanup.
```

## Cartoon Mascot

```text
Create a Codex-compatible 8-column by 9-row chibi cartoon mascot spritesheet from the reference image.
Final artwork must be image-generated, not programmatic vector drawing.
Style anchor: preserve the reference character's simple mascot look, clean black outline, flat friendly colors, expressive face, and readable silhouette.
Identity anchor: preserve the reference character's key traits: sky-blue body, round head, one pointed cat-like ear, orange cheek circles, black oval nose, closed smiling eyes, small white tongue/mouth, tiny body, clasped hands, playful happy personality.
Canvas: exactly 1536x1872 if possible, each frame fits a 192x208 cell.
Rows:
1 idle standing, blink, breathing;
2 side movement facing right, clean loop;
3 side movement facing left, clean loop;
4 greeting/waving or clasped-hands attention;
5 happy bounce / delighted dance;
6 error/confused, first two frames holding ERROR sign;
7 progress bars labeled exactly 0%, 20%, 40%, 60%, 80%, 100%, 100%, 100%;
8 front-facing walk/patrol;
9 sitting with small dark laptop, typing/blinking.
Critical quality: one mascot per cell, no ghosting, no afterimages, no duplicate silhouettes, no motion trails, no cropped limbs/ears/tail/props, no cell bleeding.
Background: transparent if possible, otherwise flat removable light checker-free background.
```

## Repair Prompt

When regenerating only a bad row:

```text
Create exactly 8 separate replacement frames in one row, matching the existing pet style and scale.
Each frame must be a single isolated subject centered in its own cell with generous padding.
No motion trails, no ghosting, no afterimages, no duplicate silhouettes, no cropped body parts, no background.
```
