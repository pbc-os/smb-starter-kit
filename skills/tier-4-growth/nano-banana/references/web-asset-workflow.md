# Web-Asset Rendering Workflow

How to generate transparent PNG assets suitable for website integration. This workflow was battle-tested producing architectural miniature assets for CrossBeam's Next.js frontend, where AI-generated transparent PNGs are displayed floating on gradient backgrounds.

## The Problem

Agents frequently fail at background removal because they try to do it in a single generation pass. Gemini's image generation models do not reliably produce true alpha transparency in one shot. The result is images with white backgrounds, partial transparency, or color fringing that looks terrible on non-white website backgrounds.

## The Solution: Multi-Pass Pipeline

Always use separate passes. Each pass has a single, clear job.

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Pass 1:     │     │  Pass 2:         │     │  Pass 3:     │     │  Integration │
│  Generate    │────▶│  Remove BG       │────▶│  Cleanup     │────▶│  Web-ready   │
│  (solid bg)  │     │  (transparent)   │     │  (if needed) │     │  asset       │
└──────────────┘     └──────────────────┘     └──────────────┘     └──────────────┘
```

### Pass 1: Generate the Subject

Generate the image with a **simple, solid-color background**. This gives the model maximum freedom to focus on the subject quality.

**Best backgrounds for later removal:**
- White (`on a clean white background`) — works best in most cases
- Light gray (`on a plain light gray background`) — good when the subject has white elements
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

### Pass 2: Remove the Background

Use `edit_image.py` with a specific, explicit background removal prompt. The prompt must be detailed — vague prompts produce vague results.

**The prompt that works:**
```
Remove the background completely. Make the background fully transparent. Keep only the main subject with clean, sharp edges. Output as PNG with alpha transparency.
```

```bash
python3 scripts/edit_image.py \
  "Remove the background completely. Make the background fully transparent. Keep only the main subject with clean, sharp edges. Output as PNG with alpha transparency." \
  --images ./assets/adu-greenroof.png \
  --output ./assets/ --filename adu-greenroof-transparent.png
```

**Critical rules:**
- The output file MUST have a `.png` extension — JPEG does not support transparency
- Do NOT use vague prompts like "remove background" — be explicit about transparency
- Do NOT add creative instructions in the removal pass — keep it purely technical

### Pass 3: Cleanup (If Needed)

After removal, inspect the result. Common issues:
- **White fringe/halo** around edges (most common)
- **Semi-transparent patches** where the background wasn't fully removed
- **Missing subject parts** that were similar in color to the background

If any of these are present, run a cleanup pass:

```bash
python3 scripts/edit_image.py \
  "Clean up the edges of this transparent PNG. Remove any white fringe, halo, or semi-transparent artifacts around the subject edges. The background must be completely transparent with no artifacts. Preserve all subject detail." \
  --images ./assets/adu-greenroof-transparent.png \
  --output ./assets/ --filename adu-greenroof-transparent.png
```

### Verification

After the pipeline, verify the result before using it:

1. **Visual check:** Open the PNG in a viewer that shows transparency (Preview on macOS shows a checkerboard pattern for transparent areas)
2. **File size check:** A transparent PNG is typically larger than the original (alpha channel adds data). If it's smaller, the transparency may not have been applied
3. **Web preview check:** Drop it on a colored `<div>` and confirm no white box appears

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
2. **Review the generations** — regenerate any that don't meet quality bar
3. **Remove backgrounds in batch** (Pass 2) — same prompt for all
4. **Cleanup pass only on those that need it** (Pass 3)
5. **Final review** — verify all are clean transparent PNGs
6. **Rename** to follow the naming convention

This is more efficient than running the full pipeline per-image, because you can batch the removal pass and only do cleanup on the subset that needs it.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| White box around subject | JPEG output, not PNG | Ensure output filename ends in `.png` |
| Partial transparency | Vague removal prompt | Use the exact prompt from Pass 2 above |
| Subject parts missing | Background color too similar to subject | Regenerate Pass 1 with a contrasting background color |
| White fringe/halo | Common edge artifact | Run Pass 3 cleanup |
| Model returns text instead of image | Prompt too complex | Simplify the removal prompt — keep it technical, not creative |
| 500 Internal Error | Prompt too long or model overloaded | Shorten the prompt; retry; try Flash instead of Pro |
