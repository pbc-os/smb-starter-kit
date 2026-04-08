---
name: patent-figure
version: 1.0.0
tier: experimental
description: "Generate and iteratively refine USPTO-style patent figure drawings from provisional patent application markdown files, using nano-banana for v1 generation and targeted single-fix edits for v2+ iteration."
requires:
  bins: ["python3"]
  skills: ["nano-banana"]
  secrets: ["GEMINI_API_KEY"]
---

# Patent Figure Generator

Generates formal USPTO-style patent figure drawings from provisional patent application `.md` files, then iteratively refines them using targeted single-fix edits.

## Prerequisites

- `nano-banana` skill installed (uses its `generate_image.py` and `edit_image.py` scripts)
- `GEMINI_API_KEY` accessible as an env var (see `secrets-manager` skill for how to wire this from your secret store)
- `pip3 install google-genai python-dotenv` if not already installed

## Core Workflow

**v1 — fresh generation (no seed image):**
Use `generate_image.py` with the full structured prompt (5 sections, see below).

**v2+ — targeted iteration (previous image as seed):**
Use `edit_image.py` with the previous version as seed + the same structured prompt + a "ONE FIX NEEDED" section.

**Never use the Mermaid diagram as a seed.** Mermaid diagrams use different internal labels than what the patent figure needs. The model will follow the Mermaid labels and override your prompt.

---

## Step 1 — Parse the Provisional

From the provisional `.md` file, extract:

1. **Brief Description** — find `## BRIEF DESCRIPTION OF THE DRAWINGS` and copy the line for the specific figure verbatim (e.g., `**FIG. 1** — System architecture overview: ...`)

2. **Verify figure number** — before generating anything, cross-check the figure number against the Brief Description. Users sometimes describe a figure by its content rather than its actual number (e.g., asking for "FIG. 2 — the trust tier diagram" when FIG. 2 is actually the signal pipeline and FIG. 3 is the tier diagram). Always generate the figure that matches the spec for that number, and note any discrepancy to the user.

3. **Reference numerals** — scan the `## DETAILED DESCRIPTION` section for every component with a parenthetical number (e.g., `Discovery Engine (210)`). Build an exact table: `210 = DISCOVERY ENGINE`. These must match what will appear in the figure exactly — this table is the single most important section of your prompt and prevents the model from hallucinating component labels. If the provisional has no parenthetical numerals yet, assign them yourself starting from the 100-series for top-level components, 200-series for platform internals, 300-series for external components.

4. **Figure structure** — read the Mermaid and ASCII diagrams in `## FIGURES` for the target figure to understand the spatial layout (which components are inside which parent, left-to-right order, hierarchy).

5. **Identify layout risks before building the prompt** — scan for these known hard cases and plan mitigations upfront (see details in `references/prompt_engineering.md`):
   - **Cross-tier arrows in multi-row platforms**: if an arrow needs to reach a component at the bottom of a dense multi-row parent box, the model will route it to the top row instead. Mitigation: reorder components so the target is in the top row, or split the platform into two columns.
   - **Terminal state positioning**: in state machine figures, terminal end states (job complete, abort) should be positioned adjacent to their origin state in the layout spec. If left unspecified, the model places them below the last-visited state.

Read `references/prompt_engineering.md` for the complete prompt template and reference numeral extraction tips.

---

## Step 2 — Build the Structured Prompt

Every prompt (v1 and v2+) contains these 5 sections in order:

```
[1] USPTO STYLE RULES BLOCK
[2] BRIEF DESCRIPTION (verbatim from spec)
[3] REFERENCE NUMERAL TABLE (exact labels, do not change any)
[4] DIRECTED CONNECTION LIST (plain bullets — no A1/A2 codes)
[5] LAYOUT INSTRUCTIONS
[+ ONE FIX NEEDED (v2+ only)]
```

Read `references/prompt_engineering.md` for the full template for each section. The most common mistakes to avoid:
- **Never use A1/A2/A3 notation** in the connection list — the model renders them literally as labels on the arrows
- **Always describe spatial relationships** for arrows (e.g., "X is on the right margin of parent box Y; Z is inside Y second from left — therefore the arrow travels leftward within Y's boundary")

---

## Step 3 — Generate v1

```bash
# Ensure GEMINI_API_KEY is set in your environment (see secrets-manager skill for setup).
python3 ~/.claude/skills/nano-banana/scripts/generate_image.py \
  "$PROMPT" \
  --output ~/Downloads \
  --filename "PATENT-FIG{N}-V1-{FIGURE-NAME}.jpg" \
  --aspect-ratio "4:3" \
  --model "gemini-3-pro-image-preview"
```

Use `4:3` aspect ratio for system architecture / flowchart figures. Use `3:4` for tall sequential figures (e.g., sequence diagrams).

---

## Step 4 — Assess and Identify Fixes

After generating, read the image and check against this checklist:

- [ ] All reference numerals present and match the table exactly
- [ ] All arrows present with correct labels
- [ ] Every arrow arrowhead terminates unambiguously on the correct target box (not floating, not pointing to wrong component)
- [ ] No floating tier labels outside boxes (e.g., "TOP TIER", "MIDDLE TIER")
- [ ] No icons, no fills, no color — strict monochrome line art
- [ ] `SHEET N OF N` in top-right corner
- [ ] `FIG. N` caption centered at bottom
- [ ] No alphanumeric codes (A1, A2...) on arrows
- [ ] All text in uppercase block letters

Read `references/assessment_checklist.md` for common failure modes and how to describe fixes precisely.

---

## Step 5 — Iterate (v2+)

Fix **one issue per iteration**. Add a `THE ONE FIX NEEDED` section at the end of the prompt:

```
THE ONE FIX NEEDED:
[Describe exactly what is wrong and exactly what it should look like instead.
Include spatial context: which box is the origin, which box is the destination,
what direction the arrow should travel, which boundary it should stay within.]

Do not change anything else. Every other component label, reference numeral,
layout, and arrow must remain exactly as it appears in the input image.
```

Then call `edit_image.py` with the previous version as `--images` input.

Repeat until all checklist items pass. Typically takes 3–7 iterations for a complex system architecture figure.

---

## Output

Save final figure to `~/Downloads/PATENT-FIG{N}-FINAL-{FIGURE-NAME}.jpg` and embed it in the provisional `.md` file:

```markdown
![FIG. N — Description](./PATENT-FIG{N}-FINAL-{FIGURE-NAME}.jpg)
*FIG. N: [Brief description with reference numerals]*
```

Use a relative path (not a raw GitHub URL) so pandoc can embed it when converting to `.docx`.

---

## Reference Files

- `references/prompt_engineering.md` — complete prompt template with all 5 sections filled in, plus tips for extracting reference numerals
- `references/assessment_checklist.md` — common failure modes and how to write precise fix descriptions
