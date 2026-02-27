# Assessment Checklist

After each generation, read the image carefully and check every item. Check top-to-bottom, left-to-right through the figure.

## Pass / Fail Checklist

### Structure
- [ ] All reference numerals from the table are present in the figure
- [ ] Every reference numeral label matches the table exactly (no abbreviations, no rewordings, no renumbering)
- [ ] Layout matches the specified tier/hierarchy structure
- [ ] Parent/child box relationships are correct (sub-components inside their parent boundaries)

### Style
- [ ] Strict monochrome — no color, no gray fills, no shadows
- [ ] No icons, pictograms, or decorative elements — every component is a plain labeled rectangle
- [ ] No fills inside any box
- [ ] All text is uppercase block letters
- [ ] Line weights are visually distinct: thick outer boundary, medium sub-components, thin arrows

### Arrows
- [ ] Every arrow from the connection list is present
- [ ] Every arrow has the correct label (or is correctly unlabeled)
- [ ] Every arrow points in the correct direction
- [ ] Every arrowhead terminates unambiguously ON a specific target box border
- [ ] No arrowheads floating in empty space
- [ ] No arrowheads touching the wrong box
- [ ] Dashed arrows are visually dashed (not solid)
- [ ] No alphanumeric codes (A1, A2, A3...) appear on or near any arrow

### Header / Caption
- [ ] `SHEET N OF N` appears in the top-right corner
- [ ] `FIG. N` appears centered in bold at the bottom
- [ ] Figure subtitle appears below FIG. N (if specified)
- [ ] No floating tier labels outside boxes (e.g., "TOP TIER", "MIDDLE TIER")

---

## How to Write a Good Fix Description

When an item fails, describe the fix precisely using this template:

```
THE ONE FIX NEEDED:
Currently: [describe exactly what the figure shows that is wrong]
Should be: [describe exactly what it should show]
Spatial context: [COMPONENT A (NUM)] is located [position] and [COMPONENT B (NUM)] is located [position].
The arrow must travel [direction] from [A] to [B], staying [within/outside] the [PARENT] boundary.
The arrowhead must terminate unambiguously ON the [top/bottom/left/right] border of [DESTINATION (NUM)].

Do not change anything else.
```

### Example — Arrow pointing to wrong component
```
THE ONE FIX NEEDED:
Currently: the SCRAPED DATA arrow from STEALTH CATALOG JOB (250) arcs downward and its arrowhead appears to terminate near FLORIST (302) in the vendor tier below the platform.
Should be: the arrowhead must terminate ON the VENDOR CATALOG (220) box, which is inside the platform boundary.
Spatial context: STEALTH CATALOG JOB (250) is on the RIGHT MARGIN of AGENTIC COMMERCE PLATFORM (200). VENDOR CATALOG (220) is a sub-box INSIDE platform (200), positioned second from the left. Both (250) and (220) are part of the same parent box (200). The arrow must travel LEFTWARD within the platform (200) boundary — it does NOT exit the platform downward. The arrowhead must unambiguously land ON the border of VENDOR CATALOG (220).

Do not change anything else.
```

### Example — Alphanumeric codes on arrows
```
THE ONE FIX NEEDED:
Currently: the figure has letter-number codes (A1, A3, A5, A7, A9, A11) printed directly on the arrows as labels.
Should be: remove all those letter-number codes. Arrows carry only the text labels listed in the ARROWS section (e.g., "HTTP 402 REQUEST", "ORDER FULFILLMENT REQUEST"). Do not add any other labels or codes to any arrow.

Do not change anything else.
```

### Example — Icon appeared
```
THE ONE FIX NEEDED:
Currently: the USDC WALLET sub-label inside each AI AGENT box has a wallet/dollar icon next to it.
Should be: remove all icons. USDC WALLET is a plain text sub-label only — no icon, no symbol, no graphic. It should appear as plain uppercase block letters inside a sub-box.

Do not change anything else.
```

---

## Prioritizing Fixes (when multiple issues exist)

Fix issues in this order of severity:

1. **Wrong reference numeral label** — immediately invalidates the claim mapping
2. **Missing component** — omits something claimed in the spec
3. **Arrow pointing to wrong target** — misrepresents the data flow
4. **Missing arrow** — omits a claimed connection
5. **Floating arrowhead** — ambiguous, examiner may question
6. **Alphanumeric codes on arrows** — artifact, distracting but not fatal
7. **Tier labels outside boxes** — minor but unprofessional
8. **Icons present** — minor USPTO style violation
9. **Wrong line weight** — cosmetic

Fix the highest severity issue first, then iterate. Don't try to fix multiple issues in one iteration — the model tends to hallucinate changes when given multiple instructions simultaneously.
