# Deliverable Specifications

> Detailed content requirements for all 18 brand identity deliverables. Read the relevant section before launching each sub-agent.

---

## Table of Contents

1. [Brand Strategy & Positioning](#01-brand-strategy--positioning)
2. [Logo Production System](#02-logo-production-system)
3. [Color System](#03-color-system)
4. [Typography System](#04-typography-system)
5. [Art Direction Guide](#05-art-direction-guide)
6. [Iconography System](#06-iconography-system)
7. [Pattern & Texture Library](#07-pattern--texture-library)
8. [Motion & Animation System](#08-motion--animation-system)
9. [Brand Applications](#09-brand-applications)
10. [Social Media Templates](#10-social-media-templates)
11. [Email Templates](#11-email-templates)
12. [Grid & Layout System](#12-grid--layout-system)
13. [UI Component Design System](#13-ui-component-design-system)
14. [Brand Governance](#14-brand-governance)
15. [Brand Architecture](#15-brand-architecture)
16. [Design Tokens Ecosystem](#16-design-tokens-ecosystem)
17. [SVG Vector Assets](#17-svg-vector-assets)
18. [Brand Guide & Figma Setup](#18-brand-guide--figma-setup)

---

## 01: Brand Strategy & Positioning

**File:** `01-brand-strategy/BRAND-STRATEGY.md`
**Target:** 40-60KB

### Required Sections

1. **Executive Summary** — one-page brand overview
2. **Market Context** — industry landscape, market size, trends, timing
3. **Competitive Landscape** — 3-5 competitors analyzed (positioning, strengths, weaknesses, visual identity)
4. **Audience Personas** — 2-4 detailed personas with:
   - Name, age, occupation, location
   - Goals, frustrations, tech comfort
   - How they'd discover and use the product
   - What messaging resonates with them
5. **Brand Positioning**
   - Positioning statement (formal: "For [audience] who [need], [product] is the [category] that [benefit] because [reason]")
   - Brand promise
   - Value propositions (3-5)
6. **Brand Identity**
   - Mission statement
   - Vision statement
   - Core values (3-5, each with a short definition and "this means we..." statement)
   - Brand personality (the adjectives from intake, expanded with behavioral descriptions)
7. **Messaging Framework**
   - Primary tagline
   - Supporting taglines (5-8 for different contexts)
   - Elevator pitches (10-second, 30-second, 60-second)
   - Messaging matrix (audience × channel × message)
   - Narrative spine / story structure (e.g., three-beat story)
8. **Tone & Voice Guide**
   - Voice traits table (trait, description, example, counter-example)
   - Tone variations by context (landing page, email, social, support, docs)
   - "We sound like..." / "We never sound like..." lists
9. **Boilerplate Copy**
   - Press boilerplate (short and long)
   - About section copy (website)
   - Social media bios (per platform)
10. **Brand Glossary** — key terms with definitions and "never say" alternatives

### Key Guidelines
- Ground everything in the specific product and market — no generic brand-speak
- Use real-world examples and scenarios from the product
- Every persona should feel like a real person, not a demographic bucket
- The messaging matrix should cover at least 3 audiences × 4 channels

---

## 02: Logo Production System

**File:** `02-logo-system/LOGO-SYSTEM.md`
**Target:** 25-40KB
**Assets:** 4 visual references in `02-logo-system/assets/`

### Required Sections

1. **Logo Overview** — the complete logo family at a glance
2. **Primary Logo** — the default wordmark, typography details, spacing
3. **Logo Mark** — abbreviated/icon version for compact contexts
4. **Logo Lockups** — all approved configurations:
   - Primary horizontal
   - Stacked/vertical
   - With tagline
   - Mark only
   - Color variants (full color, single color, reversed/white)
   - Minimum 6 lockups, ideally 9
5. **Construction Grid** — geometric proportions, x-height relationships, spacing ratios
6. **Clear Space** — minimum spacing rules (defined as a proportion of logo height)
7. **Minimum Sizes** — smallest allowed reproduction (print and digital)
8. **Color Variants** — primary, reversed (white), single-color, grayscale, with specs for each
9. **Co-Branding** — rules for placing the logo alongside partners
10. **Mascot** (if applicable) — character spec, usage contexts, personality
11. **Logo Animation** — brief spec for animated logo (entrance/exit, duration, easing)
12. **Misuse** — 9+ examples of what NOT to do (stretch, recolor, add effects, etc.)
13. **File Format Guide** — when to use SVG, PNG, JPG, EPS for different contexts

### Visual Assets to Generate
- `logo-construction-grid.jpg` — geometric grid overlaid on the wordmark
- `logo-clear-space.jpg` — clear space zones and minimum size diagrams
- `logo-lockups-all.jpg` — grid showing all approved lockups
- `logo-misuse.jpg` — grid showing prohibited treatments with red X marks

---

## 03: Color System

**File:** `03-color-system/COLOR-SYSTEM.md`
**Target:** 35-50KB
**Assets:** 4 visual references in `03-color-system/assets/`

### Required Sections

1. **Color Philosophy** — why these colors, what they communicate
2. **Core Palette** — each color with hex, RGB, HSL, role description
3. **Extended Tint/Shade Scales** — 10-step scale (50-900) for each core color, with hex values
4. **Semantic Color Assignments** — which colors map to: text, background, actions, success, warning, error, info, borders, muted
5. **WCAG Accessibility Matrix** — contrast ratios for every foreground/background combination, with AAA/AA/Fail ratings
6. **Color-Blind Safety** — protanopia, deuteranopia, tritanopia simulations of key combinations
7. **Data Visualization Palette** — categorical (8+ distinct colors) and sequential scales
8. **Gradient Library** — 4-6 branded gradients with CSS `linear-gradient` code
9. **Dark Mode** (if applicable) — adjusted palette with maintained contrast ratios
10. **Print Specifications** — Pantone matches, CMYK values, spot color guidance
11. **Usage Rules** — what to pair, what to avoid, dominant/accent ratios

### Visual Assets to Generate
- `extended-palette.jpg` — tint/shade scales for all core colors
- `accessibility-matrix.jpg` — WCAG contrast grid with pass/fail badges
- `gradient-library.jpg` — gradient swatches with CSS code
- `data-viz-palette.jpg` — categorical and sequential palettes with sample charts

### Critical Rule
Never include pure black (#000000) or cool grays in a warm brand. All neutral values should be derived from the brand's warm tones.

---

## 04: Typography System

**File:** `04-typography/TYPOGRAPHY.md`
**Target:** 35-50KB

### Required Sections

1. **Type Philosophy** — what the typography communicates, why these fonts were chosen
2. **Font Stack** — primary display, body, and mono fonts with complete fallback chains
3. **Type Scale** — from xs (12px) to 6xl (60px), with rem values, line heights, letter spacing
4. **Weight Usage** — which weights for which contexts (headings, body, emphasis, code)
5. **Responsive Typography** — how sizes change across breakpoints
6. **Component Typography** — specific type specs for buttons, inputs, cards, badges, nav, etc.
7. **Pairing Rules** — which combinations work, which to avoid
8. **Heading Hierarchy** — H1-H6 styles with visual examples
9. **Case Rules** — sentence case, lowercase, uppercase usage and where each applies
10. **Web Implementation** — CSS `@font-face`, next/font setup, Google Fonts loading
11. **Performance** — font loading strategy, subsetting, swap behavior
12. **Deprecation Notes** (if migrating from old fonts) — what's being replaced and why

---

## 05: Art Direction Guide

**File:** `05-art-direction/ART-DIRECTION.md`
**Target:** 60-90KB
**Assets:** 3 state illustrations in `05-art-direction/assets/`

### Required Sections

1. **Visual Philosophy** — the brand's visual world, emotional target
2. **Illustration Style Specification**
   - Medium/technique (e.g., diorama, flat, 3D, photography)
   - Camera angle, lens, depth of field
   - Lighting direction, color temperature, quality
   - Scale and proportion rules
   - Color grading / post-processing
3. **Scene Taxonomy** — categories of scenes the brand uses, with descriptions
4. **Photography Rules** (if applicable) — composition, subject matter, mood, editing
5. **State Illustrations** — specs for error, empty, success, loading, onboarding states
6. **AI Image Generation Guide** — prompt engineering templates for consistent image generation
   - Model recommendations
   - Prompt structure (subject, style, lighting, color, camera, mood)
   - 10+ example prompts covering key scenes
   - Quality control checklist
7. **What to Avoid** — styles, compositions, color treatments that are off-brand

### Visual Assets to Generate
- `state-error.jpg` — error/404 state illustration in the brand's style
- `state-empty.jpg` — empty state illustration
- `state-success.jpg` — success/completion state illustration

---

## 06: Iconography System

**File:** `06-iconography/ICONOGRAPHY.md`
**Target:** 40-55KB

### Required Sections

1. **Icon Philosophy** — functional clarity over decorative flair
2. **Icon Library** — preferred icon set (e.g., Lucide, Heroicons, Phosphor) with justification
3. **Icon Specifications** — default size, stroke width, padding, corner radius
4. **Icon Grid** — the alignment grid icons sit on (e.g., 24×24 with 2px padding)
5. **Usage Matrix** — 60+ icon mappings organized by category:
   - Navigation (home, search, menu, back, close)
   - Actions (add, edit, delete, save, share, download)
   - Status (success, warning, error, info, loading)
   - Commerce (cart, payment, order, receipt, delivery)
   - Communication (email, chat, notification, phone)
   - Product-specific icons
6. **Custom Brand Icons** — specs for any icons not in the standard library
7. **Icon Color Rules** — primary, secondary, disabled, interactive states
8. **Accessibility** — aria labels, touch target sizes, focus indicators
9. **Implementation** — how to use in React/Next.js, SVG sprite method

---

## 07: Pattern & Texture Library

**File:** `07-patterns-textures/PATTERNS-TEXTURES.md`
**Target:** 30-45KB
**Assets:** 1 pattern library reference in `07-patterns-textures/assets/`

### Required Sections

1. **Pattern Philosophy** — subtle warmth, not decoration
2. **Pattern Catalog** — 6-8 brand patterns, each with:
   - Visual description
   - CSS implementation (using gradients, SVG backgrounds, or repeating patterns)
   - Use cases (page background, card texture, section divider)
   - Opacity and scale recommendations
3. **Texture Overlays** — noise, grain, paper effects with CSS
4. **Decorative Elements** — lines, dots, geometric accents
5. **Background Compositions** — how to layer patterns, colors, and content
6. **Usage Guidelines** — when to use patterns vs. solid colors, density rules

### Visual Assets to Generate
- `pattern-library.jpg` — grid showing all brand patterns with labels

---

## 08: Motion & Animation System

**File:** `08-motion-animation/MOTION-ANIMATION.md`
**Target:** 35-50KB
**Assets:** 2 visual assets in `08-motion-animation/assets/`

### Required Sections

1. **Motion Philosophy** — what animation communicates in this brand (e.g., warmth, confidence)
2. **Three Rules** — the guiding principles for all motion
3. **Easing Curves** — 4 curves (default, entrance, exit, emphasis) with CSS cubic-bezier values
4. **Duration Scale** — 5 tiers (micro through ambient) with millisecond values and use cases
5. **Logo Animation** — frame-by-frame storyboard (6 frames), CSS keyframe implementation
6. **Page Transitions** — entrance, exit, and content swap animations
7. **Hover & Interaction States** — button, card, link hover effects with CSS
8. **State Transitions** — loading → loaded, empty → populated, collapsed → expanded
9. **Loading & Progress** — spinner, skeleton, progress bar, mascot loading animation
10. **Ambient Effects** — subtle background animations (parallax, drift, twinkle)
11. **Video/Motion Templates** — intro/outro specs for brand videos
12. **Reduced Motion** — `prefers-reduced-motion` fallbacks for every animation
13. **Implementation** — complete CSS keyframes and custom properties

### Visual Assets to Generate
- `logo-animation-storyboard.jpg` — 6-frame storyboard showing the logo reveal sequence
- `robot-mascot-loading.jpg` — mascot/character in a loading context (if mascot exists)

---

## 09: Brand Applications

**File:** `09-brand-applications/BRAND-APPLICATIONS.md`
**Target:** 30-45KB
**Assets:** 3 mockup references in `09-brand-applications/assets/`

### Required Sections

1. **Business Cards** — front/back layout, dimensions, print specs, copy
2. **Letterhead** — header/footer layout, margins, continuation sheets
3. **Email Signature** — HTML template with logo, name, title, links
4. **Envelope** — layout for standard business envelope
5. **Pitch Deck** — cover slide, section divider, content slide, data slide templates
6. **Merchandise/Swag** — t-shirt, mug, tote bag, sticker designs
7. **Signage** — exterior sign, trade show banner, indoor wayfinding
8. **Press Kit** — what to include, boilerplate, approved images, contact

### Visual Assets to Generate
- `stationery-suite.jpg` — business card + letterhead mockup
- `pitch-deck-cover.jpg` — pitch deck cover slide
- `brand-in-context.jpg` — flat-lay lifestyle collage showing brand applied to physical items

---

## 10: Social Media Templates

**File:** `10-social-templates/SOCIAL-TEMPLATES.md`
**Target:** 25-40KB
**Assets:** 1 template kit reference in `10-social-templates/assets/`

### Required Sections

1. **Platform Specifications** — dimensions, file formats, character limits for:
   - Twitter/X (profile, banner, post, card)
   - Instagram (post, story, reel cover, profile)
   - LinkedIn (profile, banner, post, article cover)
   - Facebook (profile, cover, post)
2. **Profile Assets** — avatar, banner/cover for each platform
3. **Post Templates** — 6+ templates:
   - Product announcement
   - Feature highlight
   - Testimonial/quote
   - Data/statistic
   - Behind-the-scenes
   - Milestone celebration
4. **Story Templates** — 3+ templates with call-to-action patterns
5. **Content Guidelines** — hashtag strategy, posting cadence, engagement rules
6. **Copy Patterns** — formulas for each post type with examples

### Visual Assets to Generate
- `social-template-kit.jpg` — overview showing all templates at their platform sizes

---

## 11: Email Templates

**File:** `11-email-templates/EMAIL-TEMPLATES.md`
**Target:** 60-80KB
**Assets:** 1 email mockup in `11-email-templates/assets/`

### Required Sections

1. **Email Design System** — header, body, footer specifications, max-width, padding
2. **Component Library** — reusable email components:
   - Header (logo, navigation)
   - Hero (image + heading)
   - Content block (text + optional image)
   - CTA button (primary + secondary)
   - Feature grid (2-3 columns)
   - Testimonial/quote
   - Footer (links, unsubscribe, social icons, legal)
3. **Typography in Email** — font stacks with web-safe fallbacks, inline style patterns
4. **Color in Email** — which brand colors work in email, background treatments
5. **Production HTML Templates** — complete, tested HTML/CSS for:
   - Welcome/onboarding email
   - Order/transaction confirmation
   - At minimum 2 templates with full HTML source
6. **Subject Line Guidelines** — length, case, formulas, do's and don'ts
7. **Testing Checklist** — email client compatibility, accessibility, link testing

### Visual Assets to Generate
- `welcome-email-mockup.jpg` — the welcome email rendered in a mail client frame

---

## 12: Grid & Layout System

**File:** `12-grid-layout/GRID-LAYOUT.md`
**Target:** 30-45KB

### Required Sections

1. **Grid Philosophy** — rhythm, consistency, breathing room
2. **Base Grid** — unit size (typically 4px or 8px)
3. **Column System** — 12-column grid with gutter and margin specs per breakpoint
4. **Spacing Scale** — the complete spacing token table (base unit × multiplier)
5. **Breakpoints** — 5 breakpoints with pixel values, column counts, margins
6. **Page Anatomy** — standard page layout with header, sidebar, content, footer regions
7. **Container Widths** — max-width constraints per context (marketing page, app, docs)
8. **Vertical Rhythm** — how spacing between sections, cards, and elements is structured
9. **Responsive Behavior** — what reflows, what stacks, what hides at each breakpoint
10. **Implementation** — CSS Grid + Flexbox patterns, Tailwind utility mapping

---

## 13: UI Component Design System

**File:** `13-ui-components/UI-COMPONENTS.md`
**Target:** 80-100KB

### Required Sections

For each component, spec all visual states (default, hover, active, focus, disabled, loading, error) and all size variants (sm, md, lg where applicable).

**Components to spec (minimum 13 categories):**
1. **Buttons** — primary, secondary, ghost, destructive, icon button, button group
2. **Cards** — content card, interactive card, feature card, pricing card
3. **Badges/Tags** — status badges, category tags, count badges
4. **Navigation** — navbar, sidebar, tabs, breadcrumbs, pagination
5. **Forms** — text input, textarea, select, checkbox, radio, toggle, date picker
6. **Dialogs** — modal, drawer/sheet, alert dialog, confirmation
7. **Progress** — progress bar, loading spinner, skeleton loader, step indicator
8. **Toasts/Notifications** — success, error, warning, info, with actions
9. **Tables** — data table, sortable headers, row actions, pagination
10. **Avatar** — sizes, fallback initials, status indicator, group
11. **Tooltip** — placement variants, rich content, delay behavior
12. **Dropdown Menu** — items, submenus, icons, keyboard navigation
13. **Product-specific** — any components unique to this product's domain

Each component spec should include:
- Visual specs (padding, radius, font, colors, shadows)
- TSX/React code example
- Accessibility requirements (ARIA, keyboard, screen reader)
- Tailwind utility classes

---

## 14: Brand Governance

**File:** `14-brand-governance/BRAND-GOVERNANCE.md`
**Target:** 45-60KB

### Required Sections

1. **Purpose** — why brand governance matters, who this document is for
2. **Brand Hierarchy** — who owns the brand, decision-making authority
3. **Usage Rights** — internal use, partner use, press use, community use
4. **Approval Workflow** — how to request brand asset usage, SLAs
5. **Brand Audit Checklist** — 30+ items to verify brand compliance across touchpoints
6. **Common Misuse** — 10+ specific examples of off-brand usage with corrections
7. **Third-Party Guidelines** — what partners/press can and cannot do with the brand
8. **Asset Distribution** — how to access brand assets, file naming, versioning
9. **Legal Notices** — trademark usage, copyright, attribution requirements
10. **Machine-Readable Brand Rules** — structured YAML block that AI tools can parse for automated brand checking

---

## 15: Brand Architecture

**File:** `15-brand-architecture/BRAND-ARCHITECTURE.md`
**Target:** 25-40KB

### Required Sections

1. **Architecture Model** — branded house, house of brands, endorsed, or hybrid
2. **Brand Hierarchy** — visual diagram showing parent → product relationships
3. **Naming System** — how products, features, and tiers are named
4. **Sub-Brand Rules** — when to create a sub-brand vs. feature name
5. **Co-Branding** — logo placement, sizing, spacing when appearing with partners
6. **Attribution** — how to credit the parent company (if applicable)
7. **Domain Strategy** — website URL patterns, subdomain rules
8. **Future-Proofing** — how the architecture accommodates new products/markets

---

## 16: Design Tokens Ecosystem

**File:** `16-design-tokens/DESIGN-TOKENS.md` + 16 supporting files
**Target:** 40-55KB doc

See `references/tooling-specs.md` for the complete token structure, file formats, and platform export specifications.

### Required Files
- 7 W3C DTCG token JSON files (color, typography, spacing, elevation, radii, motion, breakpoints)
- 1 Figma Tokens Studio JSON file
- 3 Style Dictionary files (config, build script, package.json)
- 5 platform export files (CSS, Tailwind, Swift, Android colors, Android dimens)
- 1 comprehensive documentation file

---

## 17: SVG Vector Assets

**File:** `17-vector-assets/VECTOR-ASSETS.md` + 14 SVGs + production notes
**Target:** 40-50KB doc

See `references/tooling-specs.md` for SVG technical specifications.

### Required Files
- 14 SVG files (3 wordmark variants, 3 mark variants, 4 lockups, tagline lockup, favicon, mascot, pattern)
- Documentation covering web/React usage, Figma/Illustrator import, text-to-outlines, responsive SVG
- Production notes for .ai, .eps, PDF, PNG, ICO export

---

## 18: Brand Guide & Figma Setup

**Files:** `18-brand-guide/brand-guide.html` + `18-brand-guide/FIGMA-SETUP.md`
**Target:** 60-80KB HTML + 35-50KB doc

See `references/tooling-specs.md` for the HTML brand guide structure and Figma setup requirements.

### Brand Guide HTML Requirements
- Self-contained single HTML file (no external dependencies except Google Fonts CDN)
- 15-20 "pages" when printed, covering the full brand system visually
- Print-optimized with `@media print` styles and page breaks
- All color swatches, type specimens, and layout diagrams rendered in pure CSS
- Must use the brand's actual fonts loaded from Google Fonts

### Figma Setup Guide Requirements
- Step-by-step instructions a junior designer can follow
- Covers: library setup, token import, color/type/effect styles, component building, logo import, publishing, handoff
- Every value (hex, font, weight, size, shadow) must match the token files exactly
