# Prompt Engineering Reference

## Complete Prompt Template

Use this exact structure for every generation. Paste verbatim where marked.

---

### [1] USPTO STYLE RULES BLOCK

Paste this verbatim at the top of every prompt:

```
You are a USPTO patent illustrator. [For v2+: "Edit this patent figure to fix ONE specific issue. Do not change anything else."]

Strict USPTO patent drawing conventions:
- Black ink on white background only. No color. No shading. No gradients. No fills of any kind.
- No icons, no pictograms, no clip art, no decorative elements of any kind.
- Only geometric shapes: rectangles, lines, arrows, text labels.
- All text in UPPERCASE BLOCK LETTERS, technical drafting font throughout.
- Line weight hierarchy:
    - Thick border (3pt) around the outermost system boundary
    - Medium borders (1.5pt) for all internal sub-component boxes
    - Thin lines (0.75pt) for all arrows and data flow lines
- This figure must look exactly like a figure from a real issued US patent in the USPTO database.
- No floating labels outside boxes. No tier labels (e.g., "TOP TIER", "MIDDLE TIER") anywhere outside component boxes.
- SHEET [N] OF [N] in the top-right corner in small block text.
- FIG. [N] centered in bold block letters at the bottom.
- One line below FIG. [N]: [FIGURE SUBTITLE] in smaller block text.
```

---

### [2] BRIEF DESCRIPTION SECTION

```
---
BRIEF DESCRIPTION OF FIG. [N] (verbatim from specification):
"[Paste the exact text from ## BRIEF DESCRIPTION OF THE DRAWINGS for this figure]"
---
```

---

### [3] REFERENCE NUMERAL TABLE

This is the most important section. If the model doesn't have this, it will invent its own labels.

```
---
REFERENCE NUMERALS — EXACT LABELS (do not change any label in this table):
[NUM] = [EXACT LABEL AS IT SHOULD APPEAR IN THE FIGURE]
[NUM] = [EXACT LABEL]
...
---
```

**How to extract reference numerals from a provisional:**
1. Search the `## DETAILED DESCRIPTION` section for patterns like `Component Name (NNN)` where NNN is a 3-digit number
2. For sub-components, look for lines like "comprising [Sub-component A (NNN)], [Sub-component B (NNN)]..."
3. The figure caption in `## FIGURES` often lists the key reference numerals
4. Cross-check against the Mermaid diagram — but use the PATENT labels, not the Mermaid node labels (these often differ)
5. If a component appears in the figure but wasn't numbered in the spec, assign the next available number in sequence

**Label formatting rules:**
- All caps: `CONTROL MODULE`, not `Control Module`
- Keep it short: max ~4 words per label
- Endpoint paths stay as-is: `/.WELL-KNOWN/RESOURCE-NAME` (the leading `/.` is correct — it's RFC 5785)
- Vendor names stay as branded: `THIRD-PARTY API`, `PAYMENT PROCESSOR`

---

### [4] DIRECTED CONNECTION LIST

List every arrow as a plain bullet point. **Never use A1/A2/A3 or any alphanumeric codes** — the model treats them as labels to render on the arrow lines.

```
---
ARROWS — every arrow and its label (no alphanumeric codes, plain bullets only):
- From [ORIGIN (NUM)] [direction] to [DESTINATION (NUM)]: [line style] | label: "[LABEL TEXT]"
- From [ORIGIN (NUM)] [direction] to [DESTINATION (NUM)]: [line style] | no label
- Between [COMPONENT A (NUM)] and [COMPONENT B (NUM)]: bidirectional solid | label: "[LABEL TEXT]"
---
```

**Line style options:** `solid`, `dashed`, `bidirectional solid`, `bidirectional dashed`

**Examples:**
```
- From each of CLIENT AGENT (100), CLIENT AGENT (102), CLIENT AGENT (104) downward to PLATFORM (200): solid | label: "SERVICE REQUEST"
- From PLATFORM (200) upward to each of CLIENT AGENT (100), CLIENT AGENT (102), CLIENT AGENT (104): solid | label: "SERVICE RESPONSE"
- From TOKEN LEDGER (231) rightward to PAYMENT PROCESSOR (232): solid | no label
- Between PAYMENT MODULE (230) and EXTERNAL NETWORK (260): bidirectional solid | label: "NETWORK TX"
- From DATA COLLECTOR (250) leftward to DATA STORE (220): solid | label: "COLLECTED DATA"
- From REQUEST ROUTER (240) dashed to SERVICE PROVIDER (300): dashed | label: "FULFILLMENT REQUEST"
```

---

### [5] LAYOUT INSTRUCTIONS

Describe the spatial layout. For complex arrows, always include a SPATIAL CONTEXT paragraph:

```
---
LAYOUT:
[Describe the tier structure, left-to-right ordering, nesting hierarchy]

SPATIAL CONTEXT FOR ARROWS (read this before drawing any arrow):
[For each non-obvious arrow, explain the spatial relationship:]
- [COMPONENT A (NUM)] is located [position] relative to [COMPONENT B (NUM)]
- Therefore the arrow from (A) to (B) travels [direction], staying [within/outside] [boundary]
- The arrowhead must terminate [unambiguously on / clearly touching] the [border/interior] of [destination box]
---
```

**Spatial context is critical for arrows that cross tier boundaries or travel in unexpected directions.** The model defaults to routing arrows in the "logical" direction (down for "outputs to", up for "receives from") which may conflict with the actual spatial layout.

**Common spatial context to always specify:**
- When a component on the right margin of a parent box needs to send data to a component on the left inside the same parent: "travels leftward within the parent boundary, does NOT exit the parent"
- When an arrow should go up from a lower tier component to a component inside a higher tier: "arcs upward and terminates on the [left/right/top] border of [destination]"
- When two arrows from the same origin go in different directions: specify each separately with explicit directional language

---

### [6] ONE FIX NEEDED (v2+ only)

```
---
THE ONE FIX NEEDED:
[Describe in precise spatial terms what is wrong:]
- What the current figure shows: "[describe the incorrect behavior]"
- What it should show instead: "[describe the correct behavior with spatial precision]"
- Origin component: [COMPONENT (NUM)] located [where]
- Destination component: [COMPONENT (NUM)] located [where]
- Correct path: the arrow should travel [direction], staying [within/outside] [boundary], with arrowhead clearly terminating ON the [border] of [destination box]

Do not change anything else. Every other component label, reference numeral, layout, and arrow must remain exactly as it appears in the input image.
---
```

---

## Known Hard Layout Cases

These issues are persistent across model versions — plan for them in Step 1, not after v1 fails.

### Cross-tier arrows in dense multi-row platform layouts
**Problem:** When a parent box contains multiple rows of sub-components and an arrow needs to reach a component in the bottom row (e.g., PROCESSING PIPELINE at the bottom of a 3-row platform), the model consistently routes the arrowhead to the top row instead.

**Why:** The model sees the top row of the platform first and terminates there.

**Mitigation options (pick one before writing the prompt):**
1. **Reorder sub-components** — move the arrow's target to the top row of the platform in the layout spec
2. **Split the platform** — divide the dense platform into two side-by-side columns in the layout (e.g., "left column: input processing and validation; right column: output routing and delivery")
3. **Accept the limitation** — if the routing issue doesn't affect claim accuracy, select the best version and note it for the attorney

### Terminal state positioning in state machines
**Problem:** Terminal end states (e.g., JOB COMPLETE, JOB ABORTED) are placed by the model adjacent to the last state visited in the diagram flow rather than adjacent to their correct origin state.

**Why:** The model follows narrative flow rather than the explicit transition table.

**Mitigation:** In the layout instructions, explicitly position each terminal state:
```
LAYOUT:
- Place CLOSED (310) at top-center
- Place OPEN (320) below-center
- Place HALF-OPEN (330) below OPEN
- Place ABORT (340) to the right of HALF-OPEN
- Place terminal END (360) IMMEDIATELY TO THE LEFT OF CLOSED (310) — not below HALF-OPEN
- Place terminal END (370) IMMEDIATELY TO THE RIGHT OF ABORT (340)
```
Adjacent positioning prevents the model from routing terminal arrows to wrong states.

---

## Common Failure Modes and Fixes

### Arrow points to wrong component
**Cause:** Model routes arrow based on "logical flow" rather than spatial layout.
**Fix:** Add SPATIAL CONTEXT paragraph specifying exact origin position, destination position, and required path direction.

### Arrow arrowhead is ambiguous / floating
**Cause:** Model drew the arrow but didn't clearly terminate it on a box border.
**Fix:** Add: "arrowhead must unambiguously terminate ON the border of [BOX NAME (NUM)] — not floating, not touching an adjacent box"

### Model adds alphanumeric labels to arrows (A1, A2...)
**Cause:** Connection list used A1/A2 notation.
**Fix:** Remove all alphanumeric codes from connection list. Use only plain bullet points with text descriptions.

### Component labels don't match the reference numeral table
**Cause:** Mermaid diagram was used as seed, or reference numeral table was incomplete.
**Fix:** Never use Mermaid as seed. Add missing components to reference numeral table. Re-generate as v1 (fresh, no seed).

### Floating tier labels appear outside boxes
**Cause:** Model defaults to adding structural labels for readability.
**Fix:** Add to style rules: "No floating labels outside boxes. No tier labels (TOP TIER, MIDDLE TIER, BOTTOM TIER) anywhere outside component boxes."

### Icons or filled shapes appear
**Cause:** Model interprets wallet, network, blockchain, database as things to illustrate.
**Fix:** Add explicitly: "No icons, no pictograms, no clip art. Every component is a plain rectangle with a text label only."

### Reference number inconsistency (model changes a number)
**Cause:** Model thinks it's correcting an error.
**Fix:** Add to style rules: "These reference numerals are fixed by the specification and cannot be changed. Do not renumber any component."

---

## Script Invocation Reference

### v1 — Generate from scratch
```bash
# Ensure GEMINI_API_KEY is set in your environment (see secrets-manager skill for setup).
python3 ~/.claude/skills/nano-banana/scripts/generate_image.py \
  "$PROMPT" \
  --output ~/Downloads \
  --filename "PATENT-FIG{N}-V1-{SLUG}.jpg" \
  --aspect-ratio "4:3" \
  --model "gemini-3-pro-image-preview"
```

### v2+ — Iterate on previous version
```bash
# Ensure GEMINI_API_KEY is set in your environment (see secrets-manager skill for setup).
python3 ~/.claude/skills/nano-banana/scripts/edit_image.py \
  "$PROMPT" \
  --images "~/Downloads/PATENT-FIG{N}-V{PREV}-{SLUG}.jpg" \
  --output ~/Downloads \
  --filename "PATENT-FIG{N}-V{NEXT}-{SLUG}.jpg" \
  --aspect-ratio "4:3" \
  --model "gemini-3-pro-image-preview"
```

### Aspect ratio guide
| Figure type | Aspect ratio |
|---|---|
| System architecture (horizontal tiers) | 4:3 |
| Sequence / flowchart (tall) | 3:4 |
| State machine | 1:1 |
| Timeline / pipeline (wide) | 16:9 |
