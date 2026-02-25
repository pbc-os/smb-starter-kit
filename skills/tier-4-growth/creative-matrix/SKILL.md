---
name: creative-matrix
description: Generate Meta/Facebook ad creative concepts using a 3x3x3 Creative Multiplication framework (3 messaging angles x 3 formats x 3 funnel stages = 27 unique concepts). This skill should be used when the user wants to generate ad creatives, build a creative brief, plan ad campaigns, overcome creative fatigue, or scale paid social creative. Produces structured briefs with copy, format specs, and targeting. Optionally generates draft image and video assets if nano-banana or fal.ai tools are available.
---

# Creative Matrix

## Overview

Generate a full set of ad creative concepts for any brand using the Creative Multiplication framework by **Curtis Howland**. The framework produces 27 unique creative concepts by combining 3 messaging angles (Pain Point, Desire, Social Proof) x 3 creative formats (Static, Video, Carousel) x 3 funnel stages (TOF, MOF, BOF). Each concept is distinct enough to avoid auction overlap in Meta's algorithm.

> **Attribution**: The Creative Multiplication framework was created by [Curtis Howland](https://www.linkedin.com/in/curtishowland/), based on $30M+ in Meta ad spend. This skill implements his methodology as published on LinkedIn.

## Prerequisites — Asset Generation (Optional)

Brief/copy generation requires no additional tools. Asset generation is optional and requires the user to bring their own API keys:

- **Static image generation**: Requires nano-banana skill (Gemini) OR fal.ai MCP server (Flux, SDXL)
- **Video generation**: Requires fal.ai MCP server (Kling, MiniMax, Wan)
- **No tools available**: Output briefs only — the user or their production team handles asset creation

To detect availability, check if nano-banana or fal.ai tools are accessible before offering asset generation.

## Workflow

### Phase 1: Gather Brand Context

Before generating concepts, collect the following from the user. Ask concisely — do not overwhelm with questions. Prioritize the first three; the rest are helpful but optional.

1. **Brand/Product** — What is the product or service?
2. **Target Audience** — Who is the ideal customer? Demographics, psychographics, pain points.
3. **Offer** — What is the current offer? (discount, bundle, free trial, etc.)
4. **Product Category Signal** — Is the value immediately visible (fashion, jewelry, food) or does the customer need to believe a transformation (skincare, supplements, coaching)? This determines the static vs video weighting.
5. **Existing Creative Winners** — Any ads that have worked well? What angle/format were they?
6. **Budget Tier** — Starter (5-10 concepts), Growth (15-18 concepts), or Full Matrix (all 27).
7. **Platform Notes** — Stories-heavy? Feed-heavy? Reels? This affects format specs.

### Phase 2: Generate the Creative Matrix

Load `references/framework.md` for the full framework reference including angles, formats, funnel stages, sub-triggers, benchmarks, and combination examples.

For each concept in the matrix, produce a structured brief:

```
## [Cell ID] — [Funnel] x [Format] x [Angle]

**Hook/Headline**: [The opening line or visual hook]
**Body Copy**: [Supporting copy, 2-3 sentences max]
**CTA**: [Call to action]
**Sub-Angle**: [Which sub-angle: frustration/fear/regret, aspiration/freedom/status, testimony/authority/relatability]
**Triggers**: [Psychological triggers activated]
**Format Spec**: [Dimensions, duration, card count, production notes]
**Targeting**: [Funnel stage targeting notes]
**Priority**: [High/Medium/Low based on rules below]
```

#### Prioritization Rules

Apply these rules when assigning priority and recommending test order:

- Allocate 80% of creative volume to TOF
- Weight statics higher for visually-obvious products (fashion, jewelry, food)
- Weight video higher for belief-driven products (skincare, supplements, transformations)
- Decision rule: SEE IT → static. BELIEVE IT → video.
- Carousels for education-heavy or comparison-selling products
- Mark Partnership/creator-handle ads as high priority when applicable (53% lower CAC)
- For starter budgets, recommend a balanced sample: 3 TOF (one per format), 2 MOF, 1 BOF

#### Recommended Starter Set (6 Concepts)

When the user selects Starter tier or does not specify, generate these 6 as a minimum viable test:

1. TOF x Static x Pain Point
2. TOF x Video x Desire
3. TOF x Carousel x Social Proof
4. MOF x Video x Social Proof
5. MOF x Static x Desire
6. BOF x Static x Pain Point (with offer)

### Phase 3: Asset Generation (Optional)

If asset generation tools are available and the user requests assets:

#### Static Images

1. For each static concept, compose an image generation prompt based on the brief's hook, visual direction, and brand context
2. Generate using nano-banana or fal.ai image generation
3. Aim for smartphone-aesthetic quality — studio polish is not needed (smartphone beats studio 84% of the time in Stories)
4. Generate 1-2 variants per concept for A/B testing

#### Carousel Cards

1. For each carousel concept, generate individual card images
2. Card 1 must hook with the problem or question — never lead with the product
3. Final card includes the CTA and offer
4. Maintain visual consistency across cards

#### Video

1. For each video concept, generate a video using fal.ai if available
2. Focus the prompt on the first 3 seconds — this decides everything
3. Include text overlay direction in the prompt for hook text
4. If fal.ai video is not available, output a detailed script/storyboard instead:
   - Shot-by-shot breakdown
   - Timing (focus on 3-second hook)
   - Text overlay copy
   - Audio/music direction
   - Recommended length (15s, 30s, or 60s)

### Phase 4: Output Summary

After generating all concepts, provide a summary table:

| # | Funnel | Format | Angle | Sub-Angle | Hook (short) | Priority |
|---|--------|--------|-------|-----------|--------------|----------|

Follow with:
- **Recommended test order** — which concepts to launch first
- **Performance benchmarks to watch** — hook rate thresholds for video (kill below 25%, good 30-40%, scale above 40%), static conversion share targets
- **Iteration guidance** — when to kill, iterate, or scale each concept

## Format Specs Quick Reference

| Format | Dimensions | Notes |
|--------|-----------|-------|
| Static (Feed) | 1080x1080 or 1080x1350 | 1350 for more real estate |
| Static (Stories/Reels) | 1080x1920 | Full screen vertical |
| Video (Feed) | 1080x1080 or 1080x1350 | First 3 sec = everything |
| Video (Stories/Reels) | 1080x1920 | 15s or 30s preferred |
| Carousel (Feed) | 1080x1080 per card | 3-5 cards typical |
