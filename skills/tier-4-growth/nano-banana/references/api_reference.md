# Nano Banana API Reference

Quick reference for Google Gemini image generation models.

## Models

| Model ID | Name | Best For | Max Reference Images |
|----------|------|----------|---------------------|
| `gemini-2.5-flash-image` | Nano Banana Flash | Fast iterations, high volume, lower cost | 14 |
| `gemini-3-pro-image-preview` | Nano Banana Pro | High quality, text rendering, complex prompts | 14 |

### Model Selection Guide

- **Flash** (`gemini-2.5-flash-image`) — Default. Use for:
  - Rapid prototyping and iterations
  - Bulk generation (batch asset creation)
  - Cost-sensitive workloads
  - Quick edits and background removal

- **Pro** (`gemini-3-pro-image-preview`) — Use for:
  - Final production assets
  - Text rendering in images (logos, infographics)
  - Complex multi-element compositions
  - When Flash output quality isn't sufficient

**Important:** Model IDs change over time. If a model returns a 404 or 500 error, check [Google AI Studio](https://aistudio.google.com) for the latest available model IDs.

## Aspect Ratios

| Ratio | Dimensions | Use Case |
|-------|-----------|----------|
| `1:1` | Square | Profile pictures, icons, logos, social posts |
| `2:3` | Portrait | Posters, book covers, Pinterest |
| `3:2` | Landscape | Photos, banners, blog headers |
| `3:4` | Portrait | Social media stories, mobile cards |
| `4:3` | Landscape | Presentations, displays |
| `4:5` | Portrait | Instagram posts |
| `5:4` | Landscape | Prints, certificates |
| `9:16` | Vertical | Mobile, TikTok, Reels, Stories |
| `16:9` | Widescreen | YouTube, desktop wallpapers, hero sections |
| `21:9` | Ultra-wide | Cinematic, website banners |

## Supported Input Formats

For image editing (`edit_image.py`):
- PNG (`.png`) — preferred, supports transparency
- JPEG (`.jpg`, `.jpeg`)
- WebP (`.webp`)
- GIF (`.gif`)

## Common Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| `SAFETY_BLOCKED` | Prompt violated content policy | Modify prompt to be more appropriate |
| `INVALID_ARGUMENT` | Bad parameter value | Check aspect ratio, model values |
| `RESOURCE_EXHAUSTED` | Rate limit exceeded | Wait and retry, or reduce concurrency |
| `PERMISSION_DENIED` | Invalid or missing API key | Check GEMINI_API_KEY |
| `NOT_FOUND` | Model unavailable | Verify model ID — it may have changed |
| `500 INTERNAL` | Server error or prompt too long | Shorten prompt; retry; switch models |

## Rate Limits

- Standard tier: ~60 requests per minute
- Higher tiers available through Google Cloud billing
- For high-volume needs, space requests or use batch processing

## Pricing (approximate, subject to change)

- **Flash** (`gemini-2.5-flash-image`): ~$0.039 per image
- **Pro** (`gemini-3-pro-image-preview`): Contact Google for current pricing

## Prompting Best Practices

### Generation Prompts

1. **Be specific:** Include details about style, lighting, composition, perspective
2. **Describe what you want:** Positive framing works better than "don't do X"
3. **Specify style explicitly:** "photorealistic", "flat vector illustration", "watercolor painting"
4. **Include background direction:** "on a clean white background" for later removal
5. **Keep it focused:** One clear subject per image, avoid overloading the prompt

### Editing Prompts

1. **Be technical, not creative:** For operations like background removal, use precise language
2. **One operation per pass:** Don't combine "remove background AND change the color AND add a shadow"
3. **Reference the subject:** "Keep only the main subject" helps the model understand what to preserve
4. **Specify output format:** "Output as PNG with alpha transparency" when you need transparency

### Multi-Image Reference

Pro model supports up to 14 reference images for:
- Style consistency across a set of images
- Character/subject consistency
- Collage and composite creation

Pass multiple images to `edit_image.py` with `--images img1.png img2.png ...`

## Authentication

### Gemini API (generate + edit)

Set the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY=your_key_here
```

Or place in `.env` / `.env.local` in the working directory:
```env
GEMINI_API_KEY=your_api_key_here
```

Get an API key at: https://aistudio.google.com/apikey

### Vertex AI (inpainting only)

Inpainting uses Vertex AI, which authenticates via Google Cloud Application Default Credentials:

```bash
gcloud auth application-default login
```

The inpaint script also requires a GCP project ID and region (configured in the script).
