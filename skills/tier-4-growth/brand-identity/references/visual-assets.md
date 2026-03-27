# Visual Asset Generation Guide

> nano-banana prompt templates for generating all 19 raster visual assets in the brand identity system. Each template is parameterized — replace `{placeholders}` with values from the brand brief.

## General Prompt Rules

1. **Always include brand colors** — specify hex codes in every prompt so the AI grounds the color palette
2. **Always specify the illustration style** — match the art direction from the brand brief
3. **Always specify background color** — use the brand's page background color for reference cards. For illustrations that will float on website backgrounds, use `on a simple white background` and run the 4-pass transparent PNG pipeline (see nano-banana skill's `references/web-asset-workflow.md`)
4. **Use descriptive, specific language** — "warm golden hour lighting" not just "nice lighting"
5. **End with style keywords** — clean, professional, brand reference card, elegant, technical
6. **Transparent assets** — state illustrations (error, empty, success), loading state, and mascot images may need transparency for web use. When they do, generate with a white/magenta background and run: `generate_image.py` → `edit_image.py` (remove bg) → `make_transparent.py` (real RGBA) → `pngquant` (compress). Name these with `-transparent.png` suffix.

---

## Logo System Assets (4)

### 1. Logo Construction Grid
```
Generate a professional brand logo construction grid for the wordmark "{product_name}" —
the image should show a clean, minimal geometric construction grid with guide circles,
horizontal/vertical alignment lines, and measurement annotations overlaid on the lowercase
wordmark. The wordmark uses a rounded geometric sans-serif font ({font_name} style).
Show the mathematical proportions and spacing relationships between letters.
{background_color} background, {text_color} text, thin red construction lines and blue
measurement annotations. The style should look like a Pentagram or Collins identity
standards page. Clean, technical, elegant.
```
**Aspect ratio:** 16:9
**Output:** `02-logo-system/assets/logo-construction-grid.jpg`

### 2. Logo Clear Space
```
Generate a professional brand reference card showing logo clear space rules and minimum
size guidelines for the "{product_name}" wordmark. Show the wordmark centered with dashed
lines indicating the clear space zone around it (measured in units of the logo's x-height).
Below, show minimum size examples at different scales with checkmarks for acceptable sizes
and X marks for too-small sizes. Include both print (mm) and digital (px) minimums.
{background_color} background, {text_color} text, {accent_color} measurement lines.
Clean, technical, Pentagram-style brand standards page.
```
**Aspect ratio:** 16:9
**Output:** `02-logo-system/assets/logo-clear-space.jpg`

### 3. Logo Lockups Grid
```
Generate a professional brand reference card showing all approved logo configurations
for "{product_name}". Show a grid of 9 logo lockups: (1) primary horizontal wordmark,
(2) stacked/vertical, (3) wordmark with tagline "{tagline}", (4) mark/icon only,
(5) single-color version, (6) reversed/white on dark background, (7) horizontal lockup
with mark, (8) monochrome grayscale, (9) favicon/social avatar size. Each lockup in its
own labeled cell. {background_color} background with some cells on dark {text_color} to
show reversed versions. Clean, organized, brand standards page.
```
**Aspect ratio:** 16:9
**Output:** `02-logo-system/assets/logo-lockups-all.jpg`

### 4. Logo Misuse
```
Generate a professional brand reference card showing 9 examples of INCORRECT logo usage
for the "{product_name}" brand. Show a 3x3 grid where each cell demonstrates a prohibited
treatment: (1) stretched horizontally, (2) rotated, (3) wrong colors, (4) drop shadow
added, (5) placed on busy background, (6) outline/stroke effect, (7) gradient fill,
(8) rearranged elements, (9) low contrast on similar background. Each cell has a red X
mark and a brief label explaining the violation. {background_color} background.
Clean layout, brand standards page.
```
**Aspect ratio:** 16:9
**Output:** `02-logo-system/assets/logo-misuse.jpg`

---

## Color System Assets (4)

### 5. Extended Palette
```
Generate a professional color system reference card showing extended tint and shade scales.
Display {num_colors} rows (one per brand color), each showing a 10-step gradient from
lightest tint (50) to darkest shade (900). Colors: {list_all_colors_with_names_and_hex}.
Each swatch should be labeled with its step number and hex value. {background_color}
background, clean grid layout, professional typography. Design reference card style.
```
**Aspect ratio:** 16:9
**Output:** `03-color-system/assets/extended-palette.jpg`

### 6. Accessibility Matrix
```
Generate a professional WCAG accessibility contrast ratio matrix for a brand color system.
Show a grid where rows and columns are brand colors: {list_colors_with_hex}. Each cell
shows the contrast ratio (e.g., "7.2:1") with a badge indicating AAA (green), AA (amber),
or Fail (red). Diagonal cells are N/A. {background_color} background, clean data table
layout, professional reference card. Include a legend explaining AAA (≥7:1), AA (≥4.5:1),
AA Large (≥3:1), Fail (<3:1).
```
**Aspect ratio:** 16:9
**Output:** `03-color-system/assets/accessibility-matrix.jpg`

### 7. Gradient Library
```
Generate a professional gradient library reference card showing 6 branded gradients.
Each gradient is a wide horizontal bar with its CSS code printed below. Use combinations
of these brand colors: {list_colors_with_hex}. Gradients should feel cohesive with the
brand — warm, harmonious transitions. Include gradient names (e.g., "Golden Hour",
"Market Fresh"). {background_color} background, clean layout, design reference style.
```
**Aspect ratio:** 16:9
**Output:** `03-color-system/assets/gradient-library.jpg`

### 8. Data Visualization Palette
```
Generate a professional data visualization palette reference card. Show two sections:
(1) Categorical palette — 8 distinct colors that work together in charts, derived from
brand colors {list_colors_with_hex}, plus complementary additions for variety. Show as
color dots with hex labels and a sample bar chart using them. (2) Sequential palette —
a single-hue gradient scale (lightest to darkest) based on {primary_color}, shown as
a gradient bar with 5 labeled stops and a sample heatmap. {background_color} background,
clean reference card layout.
```
**Aspect ratio:** 16:9
**Output:** `03-color-system/assets/data-viz-palette.jpg`

---

## Art Direction Assets (3)

### 9. Error State Illustration
```
Generate a {illustration_style} illustration for an error/404 state.
{scene_description_for_error}. Color palette: {list_colors_with_hex}.
{lighting_description}. The mood should be {error_mood} — something went wrong but it's
not scary. {background_color} background if the illustration doesn't fill the frame.
High quality, professional illustration.
```
**Aspect ratio:** 1:1
**Output:** `05-art-direction/assets/state-error.jpg`

### 10. Empty State Illustration
```
Generate a {illustration_style} illustration for an empty state (no content yet).
{scene_description_for_empty}. Color palette: {list_colors_with_hex}.
{lighting_description}. The mood should be {empty_mood} — inviting the user to get
started. {background_color} background if the illustration doesn't fill the frame.
High quality, professional illustration.
```
**Aspect ratio:** 1:1
**Output:** `05-art-direction/assets/state-empty.jpg`

### 11. Success State Illustration
```
Generate a {illustration_style} illustration for a success/completion state.
{scene_description_for_success}. Color palette: {list_colors_with_hex}.
{lighting_description}. The mood should be {success_mood} — celebration without being
over the top. {background_color} background if the illustration doesn't fill the frame.
High quality, professional illustration.
```
**Aspect ratio:** 1:1
**Output:** `05-art-direction/assets/state-success.jpg`

---

## Pattern & Texture Assets (1)

### 12. Pattern Library
```
Generate a professional pattern library reference card showing 6 brand patterns.
Arrange in a 2x3 grid, each cell containing a sample of the pattern with a label below.
Patterns should match the brand aesthetic ({aesthetic_description}):
(1) subtle linen/fabric texture, (2) dot grid, (3) flowing wave/organic lines,
(4) topographic/contour lines, (5) diagonal stripes, (6) soft bokeh/light circles.
All patterns use brand colors: {list_colors_with_hex} at low opacity.
{background_color} overall background. Clean reference card layout.
```
**Aspect ratio:** 16:9
**Output:** `07-patterns-textures/assets/pattern-library.jpg`

---

## Motion & Animation Assets (2)

### 13. Logo Animation Storyboard
```
Generate a professional animation storyboard showing 6 sequential frames for a logo
reveal animation. Frame 1: empty {background_color} canvas. Frame 2: the mark/icon
fades in at center. Frame 3: mark slides to its final position. Frame 4: wordmark
"{product_name}" begins revealing left to right. Frame 5: full lockup visible.
Frame 6: final settled position. Each frame in a numbered cell with timing labels
(0.0s, 0.3s, 0.6s, 0.9s, 1.2s, 1.5s). Arrow lines showing motion paths.
Brand colors: {text_color} logo, {background_color} background.
Professional storyboard layout, clean and technical.
```
**Aspect ratio:** 16:9
**Output:** `08-motion-animation/assets/logo-animation-storyboard.jpg`

### 14. Loading State
```
Generate a {illustration_style} illustration showing {mascot_or_character_description}
in a loading/waiting context. {loading_scene_description}. Color palette:
{list_colors_with_hex}. {lighting_description}. The mood should be patient, charming,
and slightly whimsical — making the wait feel pleasant. High quality illustration.
```
**Aspect ratio:** 1:1
**Output:** `08-motion-animation/assets/{mascot_name}-loading.jpg`

---

## Brand Application Assets (3)

### 15. Stationery Suite
```
Generate a professional mockup of a brand stationery suite for "{product_name}".
Show a business card (front and back) and letterhead arranged in a flat-lay composition.
Business card: {text_color} wordmark on {background_color}, contact details in
{secondary_text_color}. Letterhead: {background_color} paper, wordmark header,
address footer. Warm, elegant photography style with subtle shadow.
Professional mockup, real materials feel.
```
**Aspect ratio:** 16:9
**Output:** `09-brand-applications/assets/stationery-suite.jpg`

### 16. Pitch Deck Cover
```
Generate a professional pitch deck cover slide for "{product_name}".
Large wordmark centered, tagline "{tagline}" below in smaller text.
Background: {illustration_style} scene or gradient using brand colors
{list_primary_colors}. Bottom: "Confidential" or "Prepared: {date}".
Aspect ratio 16:9, presentation slide format. Clean, confident, premium.
```
**Aspect ratio:** 16:9
**Output:** `09-brand-applications/assets/pitch-deck-cover.jpg`

### 17. Brand In Context
```
Generate a professional flat-lay lifestyle mockup showing the "{product_name}" brand
applied across multiple touchpoints. Include: smartphone showing the app/website,
laptop with the homepage, business cards, a tote bag or mug with the logo, stickers,
and a notebook. All items arranged on a clean surface. Brand colors:
{list_colors_with_hex}. Warm lighting, {aesthetic_description} aesthetic.
Professional product photography style.
```
**Aspect ratio:** 16:9
**Output:** `09-brand-applications/assets/brand-in-context.jpg`

---

## Social Template Assets (1)

### 18. Social Template Kit
```
Generate a professional social media template overview showing 5 platform templates
for "{product_name}": (1) Twitter/X banner (1500×500), (2) Instagram post (1080×1080),
(3) Instagram Story (1080×1920), (4) LinkedIn cover (1128×191), (5) profile avatar
(400×400). Each template shown at relative scale with platform label. Templates use
brand colors {list_colors_with_hex}, wordmark, and {illustration_style} imagery.
{background_color} overall background. Professional template kit reference card.
```
**Aspect ratio:** 16:9
**Output:** `10-social-templates/assets/social-template-kit.jpg`

---

## Email Assets (1)

### 19. Welcome Email Mockup
```
Generate a professional email mockup showing a welcome/onboarding email for
"{product_name}" rendered inside a mail client frame (like Apple Mail or Gmail).
Email has: {illustration_style} hero image header, "Welcome to {product_name}" heading
in {text_color}, body text explaining how to get started, a {primary_action_color} CTA
button, and a footer with social links and unsubscribe. Email background:
{background_color}. Card content on white. Mail client chrome around it.
Professional email mockup, realistic rendering.
```
**Aspect ratio:** 3:4
**Output:** `11-email-templates/assets/welcome-email-mockup.jpg`

---

## Core Brand Assets (5-7)

Generate these general-purpose brand reference images for the root `assets/` directory:

### Wordmark Reference
```
Generate a clean, minimal brand reference showing the wordmark "{product_name}"
in {font_name} {font_weight}, {text_color} on {background_color}.
Centered, plenty of whitespace. Below the wordmark, small text:
"Font: {font_name} {font_weight} | Color: {text_color_hex}".
Clean, minimal, identity reference card.
```
**Output:** `assets/wordmark.jpg`

### Color Palette Card
```
Generate a brand color palette reference card showing {num_colors} color swatches
in a horizontal row. Each swatch is a circle or rounded rectangle with the color name
above and hex value below. Colors: {list_all_colors_with_names_and_hex}.
{background_color} background. Clean, minimal, professional reference card.
```
**Output:** `assets/color-palette.jpg`

### Type Specimen
```
Generate a typography specimen card for {font_name}. Show the full alphabet (uppercase
and lowercase), numerals 0-9, and common punctuation. Below, show the font at different
weights: {list_weights}. Use {text_color} text on {background_color}.
Include the font name as a heading. Clean, elegant type specimen layout.
```
**Output:** `assets/type-specimen.jpg`
