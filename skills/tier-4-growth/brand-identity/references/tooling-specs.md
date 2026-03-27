# Design Tooling Specifications

> Technical specifications for design tokens (deliverable 16), SVG vector assets (deliverable 17), and the HTML brand guide + Figma setup (deliverable 18). Read the relevant section when generating these deliverables.

---

## Table of Contents

1. [Design Tokens Structure](#design-tokens-structure)
2. [SVG Technical Specifications](#svg-technical-specifications)
3. [HTML Brand Guide Structure](#html-brand-guide-structure)
4. [Figma Setup Guide Structure](#figma-setup-guide-structure)

---

## Design Tokens Structure

### Directory Layout

```
16-design-tokens/
├── DESIGN-TOKENS.md                    # Comprehensive documentation (40-55KB)
├── tokens/
│   ├── color.tokens.json               # W3C DTCG format
│   ├── typography.tokens.json
│   ├── spacing.tokens.json
│   ├── elevation.tokens.json
│   ├── radii.tokens.json
│   ├── motion.tokens.json
│   └── breakpoints.tokens.json
├── figma/
│   └── figma-tokens.json               # Tokens Studio for Figma format
├── style-dictionary/
│   ├── config.json                     # Style Dictionary v4 config
│   ├── build.mjs                       # ESM build script
│   └── package.json                    # Dependencies
└── platforms/
    ├── css/
    │   └── variables.css               # Complete CSS custom properties
    ├── tailwind/
    │   └── tokens.config.js            # Tailwind v4 theme extension
    ├── ios/
    │   └── BrandTokens.swift           # Swift UIColor + UIFont extensions
    └── android/
        ├── colors.xml                  # Android color resources
        └── dimens.xml                  # Android dimension resources
```

### W3C DTCG Token Format

All token files use the W3C Design Tokens Community Group format (https://tr.designtokens.org/format/).

**Structure:**
```json
{
  "tokenGroup": {
    "tokenName": {
      "$value": "the value",
      "$type": "color | dimension | fontFamily | fontWeight | duration | cubicBezier | number | shadow",
      "$description": "What this token is for"
    }
  }
}
```

**Token aliases** use the `{reference.path}` syntax:
```json
{
  "semantic": {
    "text-primary": {
      "$value": "{color.charcoal}",
      "$type": "color",
      "$description": "Primary body text color"
    }
  }
}
```

### Token Categories

**color.tokens.json must include:**
- Core palette (all colors from brand brief with exact hex values)
- Extended tint/shade scales (50-900, 10 steps per core color)
- Semantic aliases (text-primary, text-secondary, bg-primary, bg-secondary, bg-elevated, border-default, border-subtle, action-primary, action-primary-hover, action-secondary, success, warning, error, info)

**typography.tokens.json must include:**
- Font families (display, body, mono) with complete fallback chains
- Font weights (regular, medium, semibold, bold)
- Font sizes (xs through 6xl, in rem)
- Line heights (tight, snug, normal, relaxed)
- Letter spacing (tight, normal, wide, wider)

**spacing.tokens.json must include:**
- Complete scale from 0 to 96 (based on 4px grid), values in rem
- Every step: 0, 1(4px), 2(8px), 3(12px), 4(16px), 5(20px), 6(24px), 8(32px), 10(40px), 12(48px), 16(64px), 20(80px), 24(96px), 32(128px), 40(160px), 48(192px), 64(256px), 80(320px), 96(384px)

**elevation.tokens.json must include:**
- Shadow scale: sm, md, lg, xl, 2xl, inner
- All shadows must use the brand's warm neutral as the shadow color (e.g., `rgba(44, 36, 24, x)` for charcoal-based brands) — NEVER `rgba(0, 0, 0, x)`

**radii.tokens.json must include:**
- Scale: none(0), sm(4px), md(8px), lg(12px), xl(16px), 2xl(24px), full(9999px)

**motion.tokens.json must include:**
- 4 easing curves (default, entrance, exit, emphasis) as cubic-bezier arrays
- 6 durations (micro, short, medium, long, xlong, ambient) in milliseconds

**breakpoints.tokens.json must include:**
- 5 breakpoints (sm, md, lg, xl, 2xl) in pixels

### Figma Tokens Studio Format

The `figma/figma-tokens.json` file uses the Tokens Studio format with all token groups in a single file. Include 3-4 composition tokens showing common component patterns (e.g., button-primary, card-default, input-default).

### Style Dictionary v4 Config

The `style-dictionary/config.json` must define transforms for:
- CSS (custom properties in `:root`)
- Tailwind (theme extension object)
- iOS Swift (UIColor, CGFloat, String constants)
- Android (colors.xml, dimens.xml)

The `build.mjs` must be a working ESM build script. The `package.json` must list `style-dictionary@^4.0.0` as a dependency.

### Platform Export Requirements

**CSS (`platforms/css/variables.css`):**
- Complete `:root` block with ALL tokens as custom properties
- Organized with section comments
- Include `@media (prefers-color-scheme: dark)` section (comment placeholder if dark mode not defined)
- Include `@media (prefers-reduced-motion: reduce)` overrides for motion tokens

**Tailwind (`platforms/tailwind/tokens.config.js`):**
- Export default object mapping all tokens to Tailwind theme keys
- Include both Tailwind v3 (extend) and v4 (`@theme` CSS) formats

**iOS Swift (`platforms/ios/BrandTokens.swift`):**
- Namespace everything under a `Brand` enum
- UIColor extensions for all colors
- CGFloat constants for spacing and radii
- UIFont helpers for the type scale
- UIKit + SwiftUI compatible

**Android (`platforms/android/`):**
- `colors.xml`: All colors in `#AARRGGBB` format, with semantic aliases as `@color/` references
- `dimens.xml`: Spacing in dp, font sizes in sp, radii in dp

---

## SVG Technical Specifications

### Directory Layout

```
17-vector-assets/
├── VECTOR-ASSETS.md                    # Documentation (40-50KB)
├── svg/
│   ├── wordmark.svg                    # Primary — brand text color on transparent
│   ├── wordmark-white.svg              # White for dark backgrounds
│   ├── wordmark-{accent}.svg           # Accent color variant
│   ├── mark.svg                        # Icon/mark — primary colors
│   ├── mark-white.svg                  # Inverted mark
│   ├── mark-outline.svg                # Outline-only variant
│   ├── lockup-horizontal.svg           # Mark + wordmark side by side
│   ├── lockup-horizontal-white.svg     # White variant
│   ├── lockup-stacked.svg              # Mark above wordmark
│   ├── lockup-stacked-white.svg        # White variant
│   ├── lockup-tagline.svg              # Wordmark + tagline
│   ├── favicon.svg                     # Minimal favicon
│   ├── mascot-simplified.svg           # Simplified mascot outline (if applicable)
│   └── pattern-{name}.svg             # Repeatable brand pattern tile
└── production/
    └── PRODUCTION-NOTES.md             # Export instructions (10-15KB)
```

### SVG Requirements

**Every SVG must:**
- Use `viewBox` attribute only — no fixed `width`/`height` (allows infinite scaling)
- Include `role="img"` on the root `<svg>` element
- Include a `<title>` element as the first child for accessibility
- Be valid, well-formed XML (properly closed tags, quoted attributes)
- Never use `#000000` (pure black) — use the brand's text color
- Never reference external files (no `<image>`, no external CSS, no fonts by URL)

**SVG structure template:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  {Product Name} Logo — {Variant Name}
  Font: {Font Name} {Weight}

  NOTE: This SVG uses live text. For environments where {Font Name}
  is not available, convert text to outlines in your vector editor:
  - Illustrator: Type → Create Outlines
  - Figma: Right-click → Flatten
  - Inkscape: Path → Object to Path
-->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">
  <title>{Product Name} — {Variant Name}</title>
  <!-- Content -->
</svg>
```

### Suggested ViewBox Sizes

| Variant | ViewBox | Notes |
|---------|---------|-------|
| Wordmark | `0 0 280 40` | Wide, accommodate full text |
| Mark | `0 0 80 80` | Square |
| Horizontal lockup | `0 0 400 60` | Mark + gap + wordmark |
| Stacked lockup | `0 0 160 120` | Portrait |
| Tagline lockup | `0 0 300 60` | Wordmark + tagline below |
| Favicon | `0 0 32 32` | Compact |
| Mascot | `0 0 120 120` | Square, detail-friendly |
| Pattern tile | `0 0 16 16` | Small, repeatable |

### Text Handling

Use `<text>` elements with the brand font specified in `font-family`. Always include system fallbacks:
```xml
<text font-family="'{Font Name}', system-ui, sans-serif" font-weight="600">
```

Include the outline conversion comment in every SVG file.

### Pattern SVG

Use the SVG `<pattern>` element for repeatable tiles:
```xml
<defs>
  <pattern id="brand-pattern" width="16" height="16" patternUnits="userSpaceOnUse">
    <!-- pattern content -->
  </pattern>
</defs>
<rect width="100%" height="100%" fill="url(#brand-pattern)" />
```

### Production Notes Content

The `production/PRODUCTION-NOTES.md` must cover:
1. How to create Adobe Illustrator (.ai) files from SVGs
2. How to create EPS files for print vendors
3. How to create PDF versions for press kits
4. PNG export sizes: 16, 32, 64, 128, 256, 512, 1024px
5. ICO favicon creation (multi-resolution)
6. Apple Touch Icon (180×180)
7. Android adaptive icon (108dp foreground, 72dp safe zone)
8. CMYK color conversion notes with exact values

---

## HTML Brand Guide Structure

### File
`18-brand-guide/brand-guide.html` — single self-contained HTML file

### Requirements
- All CSS in a `<style>` block — no external stylesheets
- Fonts loaded via `@import` from Google Fonts CDN (the only external dependency)
- Print-optimized with `@media print` styles
- Proper `page-break-before` / `break-before` for PDF page separation
- A4/Letter compatible layout, ~800px max-width
- 15-20 "pages" when printed

### Page Structure

| Page | Title | Content |
|------|-------|---------|
| 1 | Cover | Product name (large), "Brand Identity System", preparer, date |
| 2 | Brand Overview | What it is, tagline, core story, design philosophy |
| 3 | Logo System | Wordmark + mark rendered in CSS, clear space rules, lockup list |
| 4 | Logo Variants | Color variants on light/dark backgrounds, all in CSS |
| 5 | Color Palette — Primary | Large swatches for all core colors with hex values and roles |
| 6 | Color Palette — Extended | Tint/shade scales for 3-4 key colors |
| 7 | Color Usage & Accessibility | Semantic assignments, WCAG notes, rules |
| 8 | Typography — Typefaces | Font specimens at all weights, character set preview |
| 9 | Typography — Scale | Full type scale rendered at actual sizes |
| 10 | Typography — Usage | Heading hierarchy, body, caption, code styles |
| 11 | Spacing & Grid | Base grid, spacing scale, column grid diagram |
| 12 | Elevation & Shadows | Shadow scale on cards, border radius scale |
| 13 | Iconography | Icon style, grid, example category icons |
| 14 | Motion & Animation | Easing curves, duration scale, rules summary |
| 15 | Art Direction | Illustration style, color grading, scene taxonomy |
| 16 | Brand Voice | Voice traits, tone variations, key messages |
| 17 | Do's and Don'ts | Visual rules, prohibited treatments |
| 18 | Resources | File locations, related documents, contact |

### Design Specs
- Background: brand page background color
- Text: brand text color (never `#000000`)
- Headings: brand display font, bold weight
- Body: brand body font, regular weight
- Section labels: brand muted/secondary text color
- Accent elements: brand primary action color
- Dividers: brand border color
- Use CSS-rendered elements wherever possible (not images)

---

## Figma Setup Guide Structure

### File
`18-brand-guide/FIGMA-SETUP.md` — comprehensive Markdown guide (35-50KB)

### Required Sections

1. **Library Setup**
   - Creating a new Figma team library
   - Recommended file structure (Cover, Colors, Typography, Components, Icons, Patterns)
   - Layer and component naming conventions

2. **Importing Design Tokens**
   - Installing Tokens Studio for Figma plugin
   - Step-by-step: import `figma-tokens.json` from `16-design-tokens/figma/`
   - Token set organization
   - Syncing tokens to Figma styles
   - Describe what each step looks like (since screenshots can't be embedded)

3. **Setting Up Color Styles**
   - Create all core colors as Figma color styles
   - Naming: `Brand/{Color Name}` for core, `Brand/{Color}/500` for scales
   - Semantic aliases: `Semantic/Text Primary`, `Semantic/Action Primary`, etc.

4. **Setting Up Typography Styles**
   - Adding fonts from Google Fonts
   - Creating text styles for every type scale level
   - Naming: `Heading/H1`, `Body/Regular`, `Code/Default`, etc.
   - Each style: font, weight, size, line height, letter spacing

5. **Setting Up Effect Styles**
   - Shadow styles matching elevation tokens
   - Naming: `Elevation/SM` through `Elevation/2XL`
   - Background blur effects

6. **Building Core Components**
   - Button (Primary, Secondary, Ghost — Default/Hover/Active/Disabled × SM/MD/LG)
   - Card (with auto-layout, shadow, padding, radius)
   - Badge (Success, Warning, Error, Info variants)
   - Input (Default, Focus, Error states)
   - Use auto-layout and proper constraints throughout

7. **Importing SVG Logos**
   - How to import from `17-vector-assets/svg/`
   - Converting to components
   - Setting up variants using component properties

8. **Publishing the Library**
   - How to publish as a team library
   - How consuming files link to the library
   - Update and republish workflow

9. **Handoff Workflow**
   - Dev Mode inspection
   - Design token references
   - Asset export settings
   - CSS code generation
   - Token-to-code mapping tables

### Quality Requirements
- Every value (hex, font name, weight, size, shadow) must match the token files exactly
- A junior designer should be able to follow the guide without additional help
- No placeholder content — every section has real, complete instructions
