# Example: Web-Asset Pipeline

End-to-end walkthrough of generating a set of transparent PNG assets for a website product grid.

## Scenario

You're building a landing page that displays product images floating on a gradient background. You need 4 transparent PNGs of architectural miniature buildings.

## Step 1: Setup

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Export API key (from Secret Manager or .env)
export GEMINI_API_KEY=$(gcloud secrets versions access latest --secret=GEMINI_API_KEY)

# Create output directory
mkdir -p ./assets/raw ./assets/transparent
```

## Step 2: Generate Subjects (Pass 1)

Generate all 4 images with white backgrounds using Flash for speed:

```bash
python3 scripts/generate_image.py \
  "a modern single-story ADU cottage with a front porch, photorealistic isometric tilt-shift miniature, architectural model on a simple white background" \
  --output ./assets/raw/ --filename cottage-porch.png --aspect-ratio 1:1

python3 scripts/generate_image.py \
  "a two-story ADU over a garage, contemporary design with large windows, photorealistic isometric tilt-shift miniature, architectural model on a simple white background" \
  --output ./assets/raw/ --filename 2story-garage.png --aspect-ratio 1:1

python3 scripts/generate_image.py \
  "a spanish-style ADU with terracotta roof and arched doorway, photorealistic isometric tilt-shift miniature, architectural model on a simple white background" \
  --output ./assets/raw/ --filename spanish-style.png --aspect-ratio 1:1

python3 scripts/generate_image.py \
  "a minimalist prefab modular ADU with flat roof, photorealistic isometric tilt-shift miniature, architectural model on a simple white background" \
  --output ./assets/raw/ --filename prefab-modern.png --aspect-ratio 1:1
```

## Step 3: Review Generations

Open `./assets/raw/` and visually check each image:
- Is the subject well-composed and centered?
- Is the background clean and uniform (easy to remove)?
- Does the style match across the set?

Regenerate any that don't meet the bar. Consistency across the set matters more than individual perfection.

## Step 4: Remove Backgrounds (Pass 2 — Gemini)

Run the background removal pass on each. Note: Gemini outputs a checkerboard pattern, NOT real transparency.

```bash
for img in cottage-porch 2story-garage spanish-style prefab-modern; do
  python3 scripts/edit_image.py \
    "Remove the background completely. Make the background fully transparent. Keep only the main subject with clean, sharp edges. Output as PNG with alpha transparency." \
    --images "./assets/raw/${img}.png" \
    --output ./assets/keyed/ \
    --filename "${img}-keyed.png"
done
```

## Step 5: Convert to Real RGBA (Pass 3 — make_transparent)

This is the critical step. Gemini's "transparent" output is actually RGB with a baked-in checkerboard pattern. `make_transparent.py` detects the checkerboard and converts it to a real RGBA alpha channel.

```bash
for img in cottage-porch 2story-garage spanish-style prefab-modern; do
  python3 scripts/make_transparent.py "./assets/keyed/${img}-keyed.png" \
    --output ./assets/transparent/ \
    --filename "${img}-transparent.png"
done
```

Each run prints verification stats:
```
Result: 83% transparent, 16% opaque, RGBA mode
PASS: Transparent PNG created
```

## Step 6: Verify

Spot-check by compositing on a colored background:

```python
from PIL import Image
img = Image.open('./assets/transparent/cottage-porch-transparent.png')
assert img.mode == 'RGBA', f"Expected RGBA, got {img.mode}"
bg = Image.new('RGBA', img.size, (0, 100, 200, 255))
bg.paste(img, (0, 0), img)
bg.convert('RGB').save('./assets/verify/cottage-porch-on-blue.png')
```

If you see checkerboard artifacts in the blue composite, lower the threshold:
```bash
python3 scripts/make_transparent.py ./assets/keyed/cottage-porch-keyed.png \
  --threshold 210 --feather 2
```

## Step 7: Integrate into Website

### File placement (Next.js example)

```
public/
└── images/
    └── products/
        ├── cottage-porch-transparent.png
        ├── 2story-garage-transparent.png
        ├── spanish-style-transparent.png
        └── prefab-modern-transparent.png
```

### React component

```tsx
import Image from 'next/image'

const PRODUCTS = [
  { id: 'cottage', src: '/images/products/cottage-porch-transparent.png', name: 'Cottage ADU' },
  { id: 'garage', src: '/images/products/2story-garage-transparent.png', name: '2-Story Garage' },
  { id: 'spanish', src: '/images/products/spanish-style-transparent.png', name: 'Spanish Style' },
  { id: 'prefab', src: '/images/products/prefab-modern-transparent.png', name: 'Prefab Modern' },
]

export function ProductGrid() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
      {PRODUCTS.map((p) => (
        <div key={p.id} className="flex flex-col items-center">
          <div className="bg-gradient-to-b from-sky-50 to-amber-50 rounded-2xl p-6">
            <Image
              src={p.src}
              alt={p.name}
              width={280}
              height={200}
              className="object-contain drop-shadow-lg"
              quality={85}
            />
          </div>
          <p className="mt-3 font-semibold text-sm">{p.name}</p>
        </div>
      ))}
    </div>
  )
}
```

### Key CSS patterns

```css
/* Floating asset on gradient */
.product-image {
  object-fit: contain;
  filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.12));
}

/* Hero-sized display */
.product-hero {
  max-width: 600px;
  height: auto;
}

/* Background watermark at low opacity */
.product-watermark {
  opacity: 0.15;
  pointer-events: none;
  position: absolute;
  inset: 0;
  object-fit: contain;
}
```

## Result

4 transparent PNG assets, each:
- Named with `-transparent.png` suffix
- Clean edges with no fringe or halo
- Consistent isometric tilt-shift style
- Ready for display on any background color or gradient
- Optimized for web delivery via Next.js `<Image>` at quality 85
