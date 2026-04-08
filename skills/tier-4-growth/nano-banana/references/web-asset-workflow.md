# Web-Asset Rendering Workflow

How to generate transparent PNG assets suitable for website integration. This workflow was battle-tested producing architectural miniature assets for a production Next.js frontend, where AI-generated transparent PNGs are displayed floating on gradient backgrounds.

## The Problem

Agents frequently fail at background removal because they try to do it in a single generation pass. Gemini's image generation models do not reliably produce true alpha transparency in one shot. The result is images with white backgrounds, partial transparency, or color fringing that looks terrible on non-white website backgrounds.

## The Solution: Multi-Pass Pipeline

Always use separate passes. Each pass has a single, clear job.

```
┌──────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Pass 1:     │     │  Pass 2:     │     │  Pass 3:        │     │  Pass 4:     │     │ Integration │
│  Generate    │────▶│  Remove BG   │────▶│  make_transparent│────▶│  Compress    │────▶│ Web-ready   │
│  (solid bg)  │     │  (Gemini)    │     │  (real RGBA)    │     │  (pngquant)  │     │ asset       │
└──────────────┘     └──────────────┘     └─────────────────┘     └──────────────┘     └─────────────┘
```

**Why four passes?**
- Pass 2 → 3: Gemini renders a checkerboard pattern in RGB, not real RGBA. `make_transparent.py` converts it to a proper alpha channel.
- Pass 3 → 4: Transparent PNGs from generation are typically 1-4MB. `pngquant` compresses them to under 500KB with minimal quality loss — critical for web performance.

### Pass 1: Generate the Subject

Generate the image with a **simple, solid-color background**. This gives the model maximum freedom to focus on the subject quality.

**Best backgrounds for later removal:**
- White (`on a clean white background`) — works best in most cases
- Light gray (`on a plain light gray background`) — good when the subject has white elements
- **Magenta** (`on a solid magenta/hot pink background`) — classic chroma key color, excellent for subjects with white, gray, or earth-toned elements. Battle-tested in production for architectural miniatures
- Solid color that contrasts with the subject

**Prompt structure:**
```
[detailed subject description], [style/mood], on a simple white background
```

**Example:**
```bash
python3 scripts/generate_image.py \
  "a modern two-story ADU building with clean lines and a green roof, photorealistic isometric tilt-shift miniature style, architectural model, on a simple white background" \
  --output ./assets/ --filename adu-greenroof.png --aspect-ratio 1:1
```

**Do NOT:**
- Ask for "transparent background" in the generation prompt — models ignore this
- Use complex or gradient backgrounds — they make removal harder
- Use backgrounds similar in color to the subject

### Pass 2: Remove the Background (Gemini)

Use `edit_image.py` with a specific, explicit background removal prompt. The prompt must be detailed — vague prompts produce vague results.

**The prompt that works:**
```
Remove the background completely. Make the background fully transparent. Keep only the main subject with clean, sharp edges. Output as PNG with alpha transparency.
```

```bash
python3 scripts/edit_image.py \
  "Remove the background completely. Make the background fully transparent. Keep only the main subject with clean, sharp edges. Output as PNG with alpha transparency." \
  --images ./assets/adu-greenroof.png \
  --output ./assets/ --filename adu-greenroof-keyed.png
```

**Critical rules:**
- The output file MUST have a `.png` extension — JPEG does not support transparency
- Do NOT use vague prompts like "remove background" — be explicit about transparency
- Do NOT add creative instructions in the removal pass — keep it purely technical

**Important:** The output of this pass is NOT truly transparent. Gemini renders a checkerboard pattern to visually represent transparency, but the actual PNG is RGB with no alpha channel. You MUST run Pass 3.

### Pass 3: Convert to Real RGBA Transparency

This is the critical step that agents skip. The `make_transparent.py` script detects Gemini's checkerboard pattern and converts it to a real RGBA alpha channel.

```bash
python3 scripts/make_transparent.py ./assets/adu-greenroof-keyed.png \
  --output ./assets/ --filename adu-greenroof-transparent.png
```

**Parameters:**
- `--threshold` (default: 220) — Brightness threshold for background detection. Lower = more aggressive removal. Raise if subject parts are being removed.
- `--feather` (default: 1) — Edge feathering in pixels. Higher = softer edges. Set to 0 for hard edges.
- `--mode` — `auto` (default), `checkerboard`, or `white`

**If shadows or edges have artifacts:**
```bash
python3 scripts/make_transparent.py ./assets/adu-greenroof-keyed.png \
  --threshold 210 --feather 2
```

### Pass 4: Compress for Web (pngquant)

Transparent PNGs from the generation pipeline are large (1-4MB). For web delivery, compress with `pngquant`:

```bash
# Install: brew install pngquant (macOS) or apt install pngquant (Linux)
pngquant --quality=65-85 --force --output ./assets/adu-greenroof-transparent.png \
  ./assets/adu-greenroof-transparent.png
```

**Batch compress all transparent PNGs in a directory:**
```bash
cd ./assets/transparent/
for f in *-transparent.png; do
  pngquant --quality=65-85 --force --output "$f" "$f"
done
```

**Target:** Under 500KB per image. The `--quality=65-85` range preserves visual quality while achieving 60-80% file size reduction. Transparent PNGs compress well because the alpha channel contains large uniform regions.

**If pngquant is not available**, the Next.js `<Image>` component with `quality={85}` provides runtime compression, but pre-compressing with pngquant is preferred — it reduces storage, CDN bandwidth, and initial load time.

### Verification and QA

After the pipeline, verify each result. **Do not skip this step.** In production, roughly 1 in 5 images needs a re-run or manual fix (bad edges, missing subject parts, artifacts bleeding into surrounding UI elements).

1. **Check the mode:** `python3 -c "from PIL import Image; img = Image.open('output.png'); print(img.mode)"` — must print `RGBA`, not `RGB`
2. **Check alpha stats:** The `make_transparent.py` script prints transparency percentages automatically
3. **Composite test:** Paste the image on a colored background — if the background bleeds through where it shouldn't, adjust the threshold
4. **Web preview:** Drop it on a colored `<div>` and confirm no white/gray box appears

## Naming Convention

Web-ready transparent assets should follow this pattern:

```
[subject]-[descriptor]-transparent.png
```

Examples:
- `adu-01-2story-garage-transparent.png`
- `cameron-05-lakewood-porch-transparent.png`
- `logo-primary-transparent.png`
- `product-hero-transparent.png`

## Web Integration Patterns

### Next.js / React

```tsx
import Image from 'next/image'

// Basic transparent image on gradient background
<div className="bg-gradient-to-b from-sky-50 to-amber-50">
  <Image
    src="/images/product-transparent.png"
    alt="Product"
    width={600}
    height={420}
    className="object-contain drop-shadow-lg"
    quality={85}
    priority  // for above-the-fold images
  />
</div>
```

### Size Variants

Define consistent size variants for reuse:

| Variant | Dimensions | Use Case |
|---------|-----------|----------|
| Hero | 600x420 | Landing page hero, full-width features |
| Card | 280x200 | Grid cards, thumbnails |
| Accent | 140x100 | Inline decorative, badges |
| Background | 800x560 @ 20% opacity | Watermark, ambient decoration |

### CSS Patterns

```css
/* Floating on gradient — the standard pattern */
.asset-float {
  object-fit: contain;
  filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.12));
}

/* Background watermark usage */
.asset-watermark {
  object-fit: contain;
  opacity: 0.2;
  pointer-events: none;
}
```

### Deterministic Assignment from a Pool

When you have a pool of transparent assets and need consistent assignment (e.g., each product always shows the same image):

```ts
function getAssetForId(entityId: string, pool: string[]): string {
  let hash = 0
  for (let i = 0; i < entityId.length; i++) {
    hash = ((hash << 5) - hash) + entityId.charCodeAt(i)
    hash |= 0
  }
  return pool[Math.abs(hash) % pool.length]
}
```

### Random Selection (SSR-Safe)

For random asset display that avoids hydration mismatches:

```ts
import { useState, useEffect, useId } from 'react'

function useRandomAsset(pool: string[]): string {
  const id = useId()
  const [selected, setSelected] = useState(() => {
    // Deterministic for SSR based on component instance
    let hash = 0
    for (let i = 0; i < id.length; i++) {
      hash = ((hash << 5) - hash + id.charCodeAt(i)) | 0
    }
    return pool[Math.abs(hash) % pool.length]
  })

  useEffect(() => {
    // True random on client mount
    setSelected(pool[Math.floor(Math.random() * pool.length)])
  }, [])

  return selected
}
```

## Batch Pipeline

When generating multiple assets (e.g., a set of product images):

1. **Generate all subjects first** (Pass 1) using Flash model for speed
2. **QA the generations** — open each image, regenerate any that don't meet the quality bar. Expect ~20% rejection rate. Common issues: wrong perspective, blurry details, subject clipping
3. **Remove backgrounds in batch** (Pass 2) — same Gemini prompt for all
4. **Run make_transparent on all** (Pass 3) — converts checkerboard to real RGBA
5. **QA the transparency** — composite a few on a colored background. Re-run `make_transparent` with adjusted threshold on failures. Remove any with unfixable artifacts (bokeh bleeding, missing parts)
6. **Compress with pngquant** (Pass 4) — `pngquant --quality=65-85 --force` on all
7. **Rename** to follow the naming convention (`-transparent.png`)

This is more efficient than running the full pipeline per-image, because you can batch each pass and only re-run the subset that fails QA.

**Expect iteration.** In a production run of 23 ADU miniatures we shipped, 2 images were removed post-launch (artifacts bleeding into UI) and 1 had a transparency fix applied to a specific corner. Budget for manual review time.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| White box around subject | JPEG output, or skipped Pass 3 | Ensure `.png` AND run `make_transparent.py` |
| Checkerboard baked into pixels | Skipped Pass 3 | Run `make_transparent.py` — Gemini does NOT output real alpha |
| Image mode is RGB not RGBA | Skipped Pass 3 | Run `make_transparent.py` to add real alpha channel |
| Subject parts cut off | `make_transparent` threshold too aggressive | Raise `--threshold` (e.g., 230) |
| Background remnants at edges | Threshold too conservative | Lower `--threshold` (e.g., 210) |
| White fringe near shadows | Shadow colors close to background | Use `--feather 2` and lower threshold slightly |
| Model returns text not image | Prompt too complex | Simplify the removal prompt — keep it technical |
| 500 Internal Error | Prompt too long or model overloaded | Shorten prompt; retry; try Flash instead of Pro |
