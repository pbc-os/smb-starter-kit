---
name: brand-identity
version: 1.0.0
tier: growth
description: "Create a complete, agency-grade brand identity system from scratch. Generates 18 production-ready deliverables covering brand strategy, logo system, color system (WCAG accessible), typography, art direction, iconography, patterns, motion/animation, brand applications, social templates, email templates (production HTML), grid/layout, UI component design system (with TSX), brand governance, brand architecture, W3C design tokens (CSS/Tailwind/Figma/iOS Swift/Android XML exports), SVG vector logos, and a printable HTML brand guide with Figma setup instructions. Also generates 19+ visual assets via AI image generation and 14 SVG vector files."
requires:
  bins: ["python3"]
  skills: ["nano-banana"]
  secrets: ["GEMINI_API_KEY"]
---

# Brand Identity System Generator

> Generate an 18-deliverable brand identity system with visual assets, design tokens, vector logos, and a printable brand guide. This produces the same output as a $100k+ branding agency engagement — strategy through governance, digital through print.

## Setup Verification

The agent should verify the following before using this skill:

1. **Check nano-banana skill:** Required for visual asset generation (19 raster images). Verify: `python3 -c "from google import genai; print('ok')"`
2. **Check API key:** `GEMINI_API_KEY` must be set in environment or `.env` file
3. **Check pngquant (optional):** `which pngquant` — needed only if generating transparent web-ready assets. Install: `brew install pngquant` (macOS) or `apt install pngquant` (Linux)
4. **Sub-agents:** Strongly recommended for parallelizing the 18 deliverables across 4 execution waves

If nano-banana is unavailable, the system still works — all 18 document deliverables generate normally, and visual asset locations are referenced as planned paths for later generation.

---

## Phase 1: Brand Intake

Before generating anything, gather inputs from the user. Present the **Essential Questions** as a numbered list and wait for answers. After the essentials, offer the Deep Dive questions for anyone who wants more control.

### Essential Questions (Always Ask These)

| # | Question | Purpose | Example |
|---|----------|---------|---------|
| 1 | **Product/company name** — exact casing as it should appear | Logo, wordmark, all copy | `FoodCourts.ai` |
| 2 | **What does it do?** — one paragraph, plain language | Strategy, positioning, messaging | "An open food directory that lets AI agents order from any restaurant" |
| 3 | **One-sentence pitch** | Anchor line for all strategy docs | "The open food directory for AI agents to order from any restaurant" |
| 4 | **Tagline/slogan** — or "generate options for me" | Logo lockups, hero sections, campaigns | "Technology disappears. Dinner arrives." |
| 5 | **Brand personality** — 3-5 adjectives that describe the brand's character | Visual direction, voice, all creative decisions | Warm, confident, clear, human-first |
| 6 | **Color direction** — existing hex codes OR mood/feeling description | Entire color system, UI, templates | "Warm earth tones" OR `#5B8C5A, #E8A838, #FAF6F1` |
| 7 | **Typography direction** — existing font names OR personality description | Type system, all documents, code | "Plus Jakarta Sans" OR "modern geometric sans-serif, rounded" |
| 8 | **Logo concept** — wordmark text, symbol/icon, monogram, mascot? | Logo system, vector assets, applications | "Lowercase wordmark + abbreviated mark + robot mascot" |
| 9 | **Design aesthetic** — overall visual direction and illustration style | Art direction, patterns, visual assets | "Warm, organic, tilt-shift diorama illustrations, golden hour lighting" |
| 10 | **Output directory** — where to save the entire system | File paths for all deliverables | `/path/to/project/marketing/lookbook/` |

### Deep Dive Questions (Offer After Essentials)

Present these grouped by category. The user can answer any, all, or none.

**Audience & Market:**
- Target audience — describe 2-3 user personas
- Top 3 competitors
- Key differentiator — what makes this different
- Industry/category

**Brand Foundation:**
- Brand values — 3-5 core values (e.g., transparency, craftsmanship)
- Parent company — name and visibility level (if any)
- Voice traits — how should the brand sound in writing?
- What the brand should NEVER sound like
- Key messages — 3-5 most important things to communicate
- Sensitive topics needing careful handling (payments, privacy, AI trust)

**Visual Details:**
- Mascot concept — brief description (if wanted)
- Reference brands — 2-3 brands whose visual style you admire
- Dark mode — needed or light-only?
- Print specifications — Pantone/CMYK needed?

**Technical:**
- Tech stack — web framework, CSS framework (default: Next.js + Tailwind v4)
- Mobile platforms — iOS, Android, or web-only?
- Design tool — Figma, Sketch, or Adobe? (default: Figma)
- Existing brand assets — file paths to reference for consistency

### Defaults for Missing Inputs

When the user doesn't answer optional questions, make creative decisions silently:

| Missing Input | Default Approach |
|---------------|-----------------|
| No color direction | Generate a palette matching the personality adjectives and industry conventions |
| No typography | Select fonts matching the aesthetic (modern → geometric sans, classic → humanist serif+sans, technical → mono-friendly) |
| No tagline | Generate 3-5 options in the brand strategy document |
| No competitors | Research the industry and identify 3-5 likely competitors |
| No audience | Infer 2-3 personas from the product description |
| No tech stack | Default to Next.js 15 + Tailwind v4 + shadcn/ui |
| No design tool | Default to Figma |
| No illustration style | Match the brand personality (warm → organic/diorama, bold → geometric/3D, minimal → flat/line) |
| No parent company | Treat the product as standalone with no parent hierarchy |
| No voice direction | Derive from brand personality adjectives |

---

## Phase 2: Generate Brand Brief

Before launching sub-agents, synthesize all user inputs into a **Brand Brief** — a structured reference document that every sub-agent receives. This ensures consistency across all 18 deliverables.

The brand brief should contain:
1. **Identity** — name, pitch, tagline, parent company
2. **Personality** — adjectives, voice traits, what to avoid
3. **Audience** — personas, competitors, differentiator
4. **Visual Direction** — colors (with hex codes), fonts (with weights), logo concept, aesthetic, illustration style
5. **Technical** — tech stack, platforms, design tool
6. **Key Messages** — value propositions, trust messages, sensitive topics

Write this as an internal working document (not a deliverable). Save it as `_BRAND-BRIEF.md` in the output directory for reference.

---

## Phase 3: Execute Deliverables

Generate all 18 deliverables using sub-agents for parallelization. Read `references/deliverable-specs.md` for detailed specifications for each deliverable — it contains the required sections, content requirements, size targets, and sub-agent prompt guidance.

### Execution Order

The deliverables have dependencies. Execute in this order:

**Wave 1 — Foundation (launch first, 4-5 parallel agents):**
- `01` Brand Strategy & Positioning
- `03` Color System (needs palette from intake)
- `04` Typography System (needs fonts from intake)
- `15` Brand Architecture (if parent company exists)

**Wave 2 — Visual Systems (launch after Wave 1 colors/type are done, 5-6 parallel agents):**
- `02` Logo Production System
- `05` Art Direction Guide
- `06` Iconography System
- `07` Pattern & Texture Library
- `08` Motion & Animation System

**Wave 3 — Applications & Content (launch in parallel, 4-5 agents):**
- `09` Brand Applications
- `10` Social Media Templates
- `11` Email Templates (Production HTML)
- `12` Responsive Grid & Layout System
- `13` UI Component Design System

**Wave 4 — Governance & Tooling (launch after Waves 1-3, 3-4 agents):**
- `14` Brand Governance & Usage Guide
- `16` Design Tokens Ecosystem
- `17` SVG Vector Assets
- `18` Brand Guide (HTML) & Figma Setup Guide

### Sub-Agent Prompt Pattern

Every sub-agent prompt must include:
1. The complete brand brief (from Phase 2)
2. The specific deliverable spec (from `references/deliverable-specs.md`)
3. The exact output file path
4. Explicit color hex codes, font names, and spacing values — never let sub-agents guess
5. Cross-references to related deliverables they should align with
6. Quality standards: "This is a premium agency deliverable. Every value must be exact. No placeholder content."

---

## Phase 4: Visual Asset Generation

After the document deliverables are complete, generate visual assets using the **nano-banana skill** (Gemini image generation). Read `references/visual-assets.md` for the full prompt templates.

### Asset Categories

| Category | Count | Format | Notes |
|----------|-------|--------|-------|
| Logo references (construction grid, clear space, lockups, misuse) | 4 | JPG | Reference cards, opaque backgrounds |
| Color system references (palette, accessibility, gradients, data viz) | 4 | JPG | Reference cards, opaque backgrounds |
| State illustrations (error, empty, success) | 3 | JPG or **transparent PNG** | Use 4-pass pipeline if these will float on website backgrounds |
| Pattern library reference | 1 | JPG | Reference card |
| Motion storyboard + loading state | 2 | JPG or **transparent PNG** | Loading state illustration may need transparency for web |
| Brand application mockups (stationery, pitch deck, in-context) | 3 | JPG | Photographic mockups, opaque |
| Social template kit reference | 1 | JPG | Reference card |
| Email mockup | 1 | JPG | Reference card |
| **Total raster assets** | **19** | | |

### Generating with nano-banana

Use the nano-banana `generate_image.py` script for all assets:

```bash
# Standard reference card (opaque background, JPG is fine)
python3 scripts/generate_image.py "{prompt from visual-assets.md}" \
  --output ./02-logo-system/assets/ --filename logo-construction-grid.jpg --aspect-ratio 16:9

# State illustration that needs to float on a website background
# Use the 4-pass web-asset pipeline from nano-banana:
python3 scripts/generate_image.py "{illustration prompt}, on a simple white background" \
  --output ./05-art-direction/assets/ --filename state-error-raw.png --aspect-ratio 1:1

python3 scripts/edit_image.py \
  "Remove the background completely. Make the background fully transparent. Keep only the main subject with clean edges. Output as PNG with alpha transparency." \
  --images ./05-art-direction/assets/state-error-raw.png \
  --output ./05-art-direction/assets/ --filename state-error-keyed.png

python3 scripts/make_transparent.py ./05-art-direction/assets/state-error-keyed.png \
  --output ./05-art-direction/assets/ --filename state-error-transparent.png

pngquant --quality=65-85 --force --output ./05-art-direction/assets/state-error-transparent.png \
  ./05-art-direction/assets/state-error-transparent.png
```

### When to Use Transparent PNG vs JPG

| Use Case | Format | Pipeline |
|----------|--------|----------|
| Reference cards (grids, matrices, storyboards) | JPG | Single `generate_image.py` call |
| Mockups with real-world backgrounds (stationery, in-context) | JPG | Single `generate_image.py` call |
| Illustrations that float on website gradient backgrounds | **Transparent PNG** | 4-pass pipeline (generate → remove bg → make_transparent → pngquant) |
| Mascot/character that will be composited in UI | **Transparent PNG** | 4-pass pipeline |
| Loading state animation that sits on app background | **Transparent PNG** | 4-pass pipeline |

### Asset Generation Notes

- Every nano-banana prompt must include the brand's color hex codes, aesthetic direction, and illustration style
- Use `--aspect-ratio 16:9` for landscape references, `1:1` for icons/avatars, `9:16` for stories
- Generate assets to the `assets/` subdirectory within each deliverable's folder
- Name files descriptively: `logo-construction-grid.jpg`, not `image-001.jpg`
- For transparent PNGs, use the `-transparent.png` suffix naming convention
- QA every asset — expect ~20% rejection rate. Regenerate from Pass 1 if quality doesn't meet the bar
- If nano-banana is unavailable, the system still works — documents reference the planned asset locations

---

## Phase 5: SVG Vector Assets

Generate SVG logo files as part of deliverable 17. Read `references/tooling-specs.md` for detailed SVG specifications.

Key SVGs to generate (14 files):
- Wordmark (3 color variants: primary, white, accent color)
- Mark (3 variants: primary, white/inverted, outline)
- Lockups (4: horizontal, horizontal-white, stacked, stacked-white)
- Tagline lockup
- Favicon SVG
- Simplified mascot outline
- Brand pattern tile (repeatable)

All SVGs must:
- Use `viewBox` only (no fixed width/height) for infinite scaling
- Include `<title>` and `role="img"` for accessibility
- Use exact brand hex colors — never `#000000`
- Include font conversion instructions in comments

---

## Phase 6: Design Tokens & Platform Exports

Generate as part of deliverable 16. Read `references/tooling-specs.md` for the complete token structure.

**Token files (W3C DTCG format):** color, typography, spacing, elevation, radii, motion, breakpoints
**Figma Tokens:** Single JSON for Tokens Studio plugin import
**Style Dictionary:** Config + build script for automated platform exports
**Platform exports:** CSS variables, Tailwind v4 config, iOS Swift extensions, Android XML resources

Every value must be derived from the brand brief — hex codes, font names, spacing scale, shadow values. No generic defaults.

---

## Phase 7: Assembly & Verification

After all deliverables and assets are generated:

1. **Create master index** — `BRAND-LOOKBOOK.md` at the root of the output directory. This is the table of contents for the entire system with links to every document and asset inventory.

2. **Create tracking document** — `MASTER-PLAN.md` with a deliverable tracker table showing status, size, and location for all 18 items.

3. **Verify completeness** — Run a file check confirming:
   - All 18 document files exist and are non-empty
   - All 19 visual assets exist (if nano-banana was available)
   - All 14 SVGs exist and are valid XML
   - All design token JSON files parse cleanly
   - Platform export files exist (CSS, Tailwind, Swift, Android)
   - Brand guide HTML exists

4. **Report to user** — Present a final summary table showing all deliverables, file counts, and total size.

---

## Deliverable Inventory

| # | Deliverable | Target Size | Key Contents |
|---|-------------|-------------|-------------|
| 01 | Brand Strategy & Positioning | 40-60KB | Competitive landscape, personas, positioning, values, messaging matrix |
| 02 | Logo Production System | 25-40KB | Lockups, construction grid, clear space, color variants, misuse |
| 03 | Color System | 35-50KB | Core palette, tint/shade scales, WCAG matrix, color-blind safety, gradients, print specs |
| 04 | Typography System | 35-50KB | Type scale, weight usage, responsive sizing, component typography, implementation |
| 05 | Art Direction Guide | 60-90KB | Illustration style spec, photography rules, scene taxonomy, prompt engineering guide |
| 06 | Iconography System | 40-55KB | Icon library mapping, custom specs, grid, usage matrix, accessibility |
| 07 | Pattern & Texture Library | 30-45KB | Brand patterns with CSS, textures, decorative elements, backgrounds |
| 08 | Motion & Animation System | 35-50KB | Easing curves, durations, logo animation, transitions, loading states, CSS keyframes |
| 09 | Brand Applications | 30-45KB | Business cards, letterhead, email signature, pitch deck, swag, signage, press kit |
| 10 | Social Media Templates | 25-40KB | Platform specs, post templates, story templates, content guidelines |
| 11 | Email Templates | 60-80KB | Email design system, component library, production HTML (welcome, order confirmation) |
| 12 | Grid & Layout System | 30-45KB | Base grid, column system, spacing scale, page anatomy, responsive behavior |
| 13 | UI Component Design System | 80-100KB | Buttons, cards, badges, nav, forms, dialogs, progress, toasts, tables — all states, TSX code |
| 14 | Brand Governance | 45-60KB | Third-party usage, misuse examples, audit checklist, approval workflow, legal |
| 15 | Brand Architecture | 25-40KB | Brand hierarchy, naming system, sub-brand rules, co-branding, attribution |
| 16 | Design Tokens Ecosystem | 40-55KB doc + 16 files | W3C DTCG tokens, Figma Tokens, Style Dictionary, CSS/Tailwind/Swift/Android exports |
| 17 | SVG Vector Assets | 40-50KB doc + 14 SVGs | All logo variants, favicon, mascot outline, pattern tile, production notes |
| 18 | Brand Guide & Figma Setup | 60-80KB HTML + 35-50KB doc | Printable HTML brand guide (18 pages), Figma library setup with step-by-step instructions |

---

## Directory Structure

```
[output-directory]/
├── BRAND-LOOKBOOK.md                    # Master index
├── MASTER-PLAN.md                       # Deliverable tracker
├── _BRAND-BRIEF.md                      # Internal working document
├── assets/                              # Core brand assets
│   ├── wordmark.jpg
│   ├── mark.jpg
│   ├── color-palette.jpg
│   ├── type-specimen.jpg
│   └── logo-usage.jpg
├── 01-brand-strategy/
│   └── BRAND-STRATEGY.md
├── 02-logo-system/
│   ├── LOGO-SYSTEM.md
│   └── assets/ (4 visual assets)
├── 03-color-system/
│   ├── COLOR-SYSTEM.md
│   └── assets/ (4 visual assets)
├── 04-typography/
│   └── TYPOGRAPHY.md
├── 05-art-direction/
│   ├── ART-DIRECTION.md
│   └── assets/ (3 state illustrations)
├── 06-iconography/
│   └── ICONOGRAPHY.md
├── 07-patterns-textures/
│   ├── PATTERNS-TEXTURES.md
│   └── assets/ (1 pattern library)
├── 08-motion-animation/
│   ├── MOTION-ANIMATION.md
│   └── assets/ (2 visual assets)
├── 09-brand-applications/
│   ├── BRAND-APPLICATIONS.md
│   └── assets/ (3 mockups)
├── 10-social-templates/
│   ├── SOCIAL-TEMPLATES.md
│   └── assets/ (1 template kit)
├── 11-email-templates/
│   ├── EMAIL-TEMPLATES.md
│   └── assets/ (1 email mockup)
├── 12-grid-layout/
│   └── GRID-LAYOUT.md
├── 13-ui-components/
│   └── UI-COMPONENTS.md
├── 14-brand-governance/
│   └── BRAND-GOVERNANCE.md
├── 15-brand-architecture/
│   └── BRAND-ARCHITECTURE.md
├── 16-design-tokens/
│   ├── DESIGN-TOKENS.md
│   ├── tokens/ (7 .tokens.json files)
│   ├── figma/figma-tokens.json
│   ├── style-dictionary/ (config + build script)
│   └── platforms/ (css/, tailwind/, ios/, android/)
├── 17-vector-assets/
│   ├── VECTOR-ASSETS.md
│   ├── svg/ (14 SVG files)
│   └── production/PRODUCTION-NOTES.md
└── 18-brand-guide/
    ├── brand-guide.html
    └── FIGMA-SETUP.md
```

---

## Quality Standards

Every deliverable must meet these standards:

1. **No placeholder content** — every section has real, specific, actionable content
2. **Exact values** — hex codes, font names, spacing values, easing curves are precise and consistent across all documents
3. **Cross-referencing** — documents reference each other where relevant (e.g., color system references accessibility matrix, typography references the deprecated fonts)
4. **Implementation-ready** — CSS, TSX, Swift, Android code must be syntactically correct and copy-pasteable
5. **Accessible** — WCAG contrast ratios documented, reduced-motion fallbacks included, SVGs have titles
6. **No cool grays or pure black** — if the brand uses warm tones (most do), enforce warm neutrals everywhere
7. **Consistent naming** — token names, CSS variables, file names follow the same conventions throughout

---

## Reference Files

Read these for detailed specifications when generating each deliverable:

| File | Contents | When to Read |
|------|----------|-------------|
| `references/deliverable-specs.md` | Detailed specs for all 18 deliverables — required sections, content guide, size targets | Before launching any sub-agent |
| `references/visual-assets.md` | nano-banana prompt templates for all 19 raster visual assets | Before generating images |
| `references/tooling-specs.md` | Design token structure (W3C DTCG), SVG technical specs, platform export formats, HTML brand guide structure | Before generating deliverables 16-18 |
