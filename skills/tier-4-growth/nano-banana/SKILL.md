---
name: nano-banana
version: 1.0.0
tier: growth
description: "AI image generation, editing, and web-asset rendering using Google Gemini models. Supports text-to-image, image editing, background removal for transparent PNGs, region-targeted inpainting, and a multi-pass pipeline for producing web-ready assets."
requires:
  bins: ["python3"]
  skills: ["secrets-manager"]
  secrets: ["GEMINI_API_KEY"]
  env: ["GEMINI_API_KEY"]
---

# Nano Banana

AI image generation and editing skill powered by Google Gemini. Generates images from text prompts, edits existing images, removes backgrounds for web-ready transparent PNGs, and performs region-targeted inpainting.

## Setup Verification

The agent should verify the following before using this skill:

1. **Check Python:** `python3 --version` (requires 3.9+)
2. **Check dependencies:** `python3 -c "from google import genai; print('ok')"` — if it fails, install: `pip install -r scripts/requirements.txt`
3. **Check API key:** Verify `GEMINI_API_KEY` is available. Retrieve from your secret manager:
   - GCP: `gcloud secrets versions access latest --secret=GEMINI_API_KEY`
   - Or check for a `.env` / `.env.local` file in the working directory
4. **For inpainting only:** Verify Vertex AI auth: `gcloud auth application-default print-access-token` (inpainting uses Vertex AI, not the Gemini API key)

If the API key is in a secret manager, export it before running scripts:
```bash
export GEMINI_API_KEY=$(gcloud secrets versions access latest --secret=GEMINI_API_KEY)
```

## Capabilities

### 1. Text-to-Image Generation

Generate images from text descriptions.

```bash
python3 scripts/generate_image.py "a serene Japanese garden with cherry blossoms" \
  --aspect-ratio 16:9
```

**Parameters:**
- `prompt` (required): Text description of the image to generate
- `--output` / `-o`: Output directory or file path (default: current directory)
- `--filename` / `-f`: Custom filename (default: auto-generated with timestamp)
- `--aspect-ratio` / `-a`: Image aspect ratio (default: 1:1)
- `--model` / `-m`: Model to use (default: gemini-2.5-flash-image)

### 2. Image Editing

Edit existing images with text prompts.

```bash
python3 scripts/edit_image.py "change the sky to sunset colors" \
  --images landscape.jpg

# Multiple images for consistency/reference (up to 14):
python3 scripts/edit_image.py "create a collage combining these images" \
  --images img1.png img2.png img3.png --aspect-ratio 16:9
```

**Parameters:**
- `prompt` (required): Text description of the edit
- `--images` / `-i` (required): One or more input image paths
- `--output` / `-o`: Output directory or file path (default: current directory)
- `--filename` / `-f`: Custom filename (default: auto-generated)
- `--aspect-ratio` / `-a`: Output aspect ratio (optional)
- `--model` / `-m`: Model to use

### 3. Background Removal (Web-Asset Pipeline)

Remove backgrounds to produce transparent PNGs for websites. This is a **three-pass workflow**.

**CRITICAL: Read `references/web-asset-workflow.md` before attempting background removal.** Agents frequently get this wrong. The key rules:

1. **Always use FOUR separate passes** — do not try to generate a transparent image in one shot
2. **Pass 1 — Generate:** Create the image with a solid-color background (white, light gray, or magenta for earth-toned subjects)
3. **Pass 2 — Remove background:** Use `edit_image.py` to visually remove the background
4. **Pass 3 — Make transparent:** Use `make_transparent.py` to convert to real RGBA (Gemini outputs a checkerboard pattern, NOT actual alpha transparency)
5. **Pass 4 — Compress:** `pngquant --quality=65-85` to get under 500KB for web delivery
6. **Output MUST be PNG** — JPEG does not support transparency

```bash
# Pass 1: Generate the subject (use magenta bg for earth-toned subjects)
python3 scripts/generate_image.py \
  "a modern two-story ADU building, isometric tilt-shift miniature style, on a simple white background" \
  --output ./assets/ --filename subject.png

# Pass 2: Remove the background (Gemini renders checkerboard, not real alpha)
python3 scripts/edit_image.py \
  "Remove the background completely. Make the background fully transparent. Keep only the main subject with clean edges. Output as PNG with alpha transparency." \
  --images ./assets/subject.png \
  --output ./assets/ --filename subject-keyed.png

# Pass 3: Convert checkerboard to real RGBA transparency
python3 scripts/make_transparent.py ./assets/subject-keyed.png \
  --output ./assets/ --filename subject-transparent.png

# Pass 4: Compress for web (target: under 500KB)
pngquant --quality=65-85 --force --output ./assets/subject-transparent.png \
  ./assets/subject-transparent.png
```

**Why Pass 3 is required:** Gemini's background removal renders a visible checkerboard pattern to represent transparency, but the actual PNG output is **RGB with no alpha channel**. The `make_transparent.py` script detects this checkerboard pattern and converts it to real RGBA transparency with a proper alpha channel.

**If artifacts remain** (white fringe near shadows), adjust the threshold:
```bash
python3 scripts/make_transparent.py ./assets/subject-keyed.png \
  --threshold 210 --feather 2
```

**Naming convention:** Web-ready transparent assets should use the `-transparent.png` suffix.

### 4. Region-Targeted Inpainting (Vertex AI)

Edit ONLY a specific region of an image while preserving everything else. Uses Imagen 3 via Vertex AI (requires `gcloud auth application-default login`, not GEMINI_API_KEY).

```bash
# Edit a bounding box region (auto-generates mask):
python3 scripts/inpaint_image.py "redraw these arrows with clean routing" \
  --image figure.png --bbox 100,200,500,600

# With a pre-made mask PNG (white=edit, black=preserve):
python3 scripts/inpaint_image.py "fix the overlapping labels" \
  --image figure.png --mask region_mask.png

# Remove content from a region:
python3 scripts/inpaint_image.py "" --image photo.png --bbox 50,50,300,200 --mode remove
```

**Parameters:**
- `prompt` (required): What to draw in the masked region (empty string for removal)
- `--image` / `-i` (required): Source image path
- `--mask` / `-m`: Path to mask PNG (white=area to edit, black=preserve)
- `--bbox` / `-b`: Bounding box `x1,y1,x2,y2` — auto-generates a rectangular mask
- `--output` / `-o`: Output directory or file path
- `--filename` / `-f`: Custom filename
- `--mode`: `insert` (default) or `remove`
- `--mask-dilation`: Mask edge expansion 0.0-1.0 (default: 0.01)
- `--num-images` / `-n`: Generate 1-4 candidates (default: 1)
- `--negative-prompt`: What to avoid

**When to use inpaint vs edit:**
- **Inpaint** — fix a specific area without disturbing the rest (e.g., fix arrows in one corner)
- **Edit** — the entire image needs modification (e.g., style changes, background removal)

## Supported Parameters

### Aspect Ratios
`1:1` | `2:3` | `3:2` | `3:4` | `4:3` | `4:5` | `5:4` | `9:16` | `16:9` | `21:9`

### Models

| Model ID | Name | Best For |
|----------|------|----------|
| `gemini-2.5-flash-image` | Nano Banana Flash (default) | Fast iterations, lower cost, good quality |
| `gemini-3-pro-image-preview` | Nano Banana Pro | Higher quality, text rendering, complex prompts |

**Default is Flash.** Use Pro when you need higher fidelity for final assets or when the prompt requires advanced reasoning (text in images, complex compositions).

## Web-Asset Rendering Pipeline

For generating assets intended for websites, follow the full pipeline documented in `references/web-asset-workflow.md`. Summary:

```
Generate (solid bg) → Remove BG (Gemini) → Make Transparent (real RGBA) → Compress (pngquant) → Integrate
```

Key integration patterns for web:
- Use `object-contain` to preserve aspect ratios
- Apply `drop-shadow` for floating depth on gradient backgrounds
- Use Next.js `<Image>` with `quality={85}` and appropriate `sizes`
- For random/deterministic assignment from a pool, hash the entity ID

See `examples/web-asset-pipeline.md` for a complete walkthrough.

## Resources

### scripts/
- `generate_image.py` — Text-to-image generation (Gemini API)
- `edit_image.py` — Image editing and visual background removal (Gemini API)
- `make_transparent.py` — Converts checkerboard backgrounds to real RGBA transparency (Pillow + scipy)
- `inpaint_image.py` — Region-targeted inpainting (Imagen 3, Vertex AI)
- `requirements.txt` — Python dependencies

### references/
- `api_reference.md` — Model comparison, error codes, rate limits, prompting tips
- `web-asset-workflow.md` — Multi-pass rendering pipeline for web-ready transparent PNGs

### examples/
- `web-asset-pipeline.md` — Step-by-step example of the full generate → key → integrate workflow

## Notes

- All generated images include invisible SynthID watermarks (added by Gemini)
- Pro model supports up to 14 reference images for style/subject consistency
- The background removal pass may need 1-2 attempts — always verify the output
- For batch generation, use Flash model for iterations and Pro for final versions
