#!/usr/bin/env python3
"""
Region-targeted image editing via Imagen 3 mask-based inpainting (Vertex AI).

Edits ONLY the masked region of an image while preserving everything else.
Requires Vertex AI (gcloud ADC auth), not a GEMINI_API_KEY.

Usage:
    # With a pre-made mask PNG (white=edit, black=preserve):
    python inpaint_image.py "redraw these arrows with clean routing" \
        --image figure.png --mask mask.png

    # Auto-generate a rectangular mask from bounding box coordinates:
    python inpaint_image.py "fix the arrow routing in this region" \
        --image figure.png --bbox 100,200,500,600

    # Removal mode (erase content in masked area, fill with background):
    python inpaint_image.py "" --image figure.png --mask mask.png --mode remove
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai.types import (
        Image,
        RawReferenceImage,
        MaskReferenceImage,
        MaskReferenceConfig,
        EditImageConfig,
    )
except ImportError:
    print("Error: google-genai package not installed.")
    print("  Run: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image as PILImage
except ImportError:
    print("Error: Pillow package not installed.")
    print("  Run: pip install Pillow")
    sys.exit(1)

# Configuration — override these via environment variables if needed
GCP_PROJECT = os.environ.get("GCP_PROJECT_ID", os.environ.get("GOOGLE_CLOUD_PROJECT", ""))
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
MODEL = "imagen-3.0-capability-001"

EDIT_MODES = {
    "insert": "EDIT_MODE_INPAINT_INSERTION",
    "remove": "EDIT_MODE_INPAINT_REMOVAL",
}


def generate_filename(prefix="inpainted", extension=".png"):
    """Generate a unique filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}{extension}"


def create_bbox_mask(image_path: Path, bbox: str, output_path: Path) -> Path:
    """Create a black/white mask PNG from bounding box coordinates."""
    img = PILImage.open(image_path)
    width, height = img.size

    try:
        coords = [int(c.strip()) for c in bbox.split(",")]
        if len(coords) != 4:
            raise ValueError
        x1, y1, x2, y2 = coords
    except (ValueError, IndexError):
        print(f"Error: Invalid bbox format '{bbox}'")
        print("  Expected: x1,y1,x2,y2 (e.g., 100,200,500,600)")
        sys.exit(1)

    x1 = max(0, min(x1, width))
    y1 = max(0, min(y1, height))
    x2 = max(0, min(x2, width))
    y2 = max(0, min(y2, height))

    if x2 <= x1 or y2 <= y1:
        print(f"Error: Invalid bbox region ({x1},{y1}) to ({x2},{y2})")
        sys.exit(1)

    mask = PILImage.new("RGB", (width, height), (0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255))

    mask.save(output_path, "PNG")
    print(f"  Generated mask: {output_path} ({x2-x1}x{y2-y1}px region)")
    return output_path


def validate_mask_dimensions(image_path: Path, mask_path: Path):
    """Ensure mask dimensions match the source image exactly."""
    img = PILImage.open(image_path)
    mask = PILImage.open(mask_path)

    if img.size != mask.size:
        print(f"  Mask dimensions {mask.size} don't match image {img.size}. Resizing...")
        mask = mask.resize(img.size, PILImage.NEAREST)
        mask.save(mask_path, "PNG")
        print(f"  Resized mask saved to {mask_path}")


def ensure_png(image_path: Path) -> Path:
    """Convert image to PNG if needed (Imagen requires PNG for best results)."""
    if image_path.suffix.lower() == ".png":
        return image_path

    png_path = image_path.with_suffix(".png")
    img = PILImage.open(image_path)
    if img.mode == "RGBA":
        bg = PILImage.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    img.save(png_path, "PNG")
    print(f"  Converted {image_path.suffix} -> PNG: {png_path}")
    return png_path


def inpaint_image(prompt, image, mask=None, bbox=None, output=".", filename=None,
                   mode="insert", mask_dilation=0.01, num_images=1, negative_prompt=None):
    """Edit a specific region of an image using Imagen 3 mask-based inpainting."""
    image_path = Path(image)
    if not image_path.exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    if not mask and not bbox:
        print("Error: Must provide either --mask or --bbox")
        sys.exit(1)

    if mask and bbox:
        print("Both --mask and --bbox provided. Using --mask.")
        bbox = None

    if not GCP_PROJECT:
        print("Error: GCP project not set.")
        print("  Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT environment variable,")
        print("  or run: gcloud config set project YOUR_PROJECT_ID")
        sys.exit(1)

    image_path = ensure_png(image_path)

    if bbox:
        mask_path = image_path.parent / f"_mask_{image_path.stem}.png"
        create_bbox_mask(image_path, bbox, mask_path)
    else:
        mask_path = Path(mask)
        if not mask_path.exists():
            print(f"Error: Mask not found: {mask_path}")
            sys.exit(1)

    validate_mask_dimensions(image_path, mask_path)

    output_path = Path(output)
    if output_path.is_dir() or not output_path.suffix:
        output_path.mkdir(parents=True, exist_ok=True)
        fname = filename if filename else generate_filename()
        output_path = output_path / fname
    else:
        if filename:
            output_path = output_path.parent / filename

    if output_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
        output_path = output_path.with_suffix(".png")

    edit_mode = EDIT_MODES.get(mode)
    if not edit_mode:
        print(f"Error: Invalid mode '{mode}'. Use 'insert' or 'remove'.")
        sys.exit(1)

    print(f"Inpainting image...")
    print(f"  Image: {image_path}")
    print(f"  Mask: {mask_path}")
    print(f"  Mode: {mode} ({edit_mode})")
    print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"  Project: {GCP_PROJECT} / {GCP_LOCATION}")

    try:
        client = genai.Client(vertexai=True, project=GCP_PROJECT, location=GCP_LOCATION)
    except Exception as e:
        print(f"Error initializing Vertex AI client: {e}")
        print("  Ensure gcloud ADC is set up: gcloud auth application-default login")
        sys.exit(1)

    raw_ref = RawReferenceImage(
        reference_image=Image.from_file(location=str(image_path)),
        reference_id=0,
    )
    mask_ref = MaskReferenceImage(
        reference_id=1,
        reference_image=Image.from_file(location=str(mask_path)),
        config=MaskReferenceConfig(
            mask_mode="MASK_MODE_USER_PROVIDED",
            mask_dilation=mask_dilation,
        ),
    )

    edit_config = EditImageConfig(
        edit_mode=edit_mode,
        number_of_images=num_images,
        output_mime_type="image/png",
    )
    if negative_prompt:
        edit_config.negative_prompt = negative_prompt

    try:
        result = client.models.edit_image(
            model=MODEL,
            prompt=prompt,
            reference_images=[raw_ref, mask_ref],
            config=edit_config,
        )

        if not result.generated_images:
            print("Error: No images generated. The prompt may have been blocked.")
            sys.exit(1)

        saved_paths = []
        for i, gen_img in enumerate(result.generated_images):
            if num_images > 1:
                stem = output_path.stem
                suffix = output_path.suffix
                save_path = output_path.parent / f"{stem}_{i+1}{suffix}"
            else:
                save_path = output_path

            gen_img.image.save(location=str(save_path))
            saved_paths.append(save_path)
            print(f"Saved: {save_path.absolute()}")

        if bbox:
            mask_path.unlink(missing_ok=True)

        return saved_paths[0]

    except Exception as e:
        error_msg = str(e)
        print(f"Error during inpainting: {error_msg}")

        if "PERMISSION_DENIED" in error_msg:
            print(f"  Ensure Vertex AI API is enabled:")
            print(f"  gcloud services enable aiplatform.googleapis.com --project={GCP_PROJECT}")
        elif "not found" in error_msg.lower():
            print(f"  Model {MODEL} may not be available in {GCP_LOCATION}.")
        elif "application default credentials" in error_msg.lower():
            print("  Run: gcloud auth application-default login")

        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Region-targeted image editing via Imagen 3 mask-based inpainting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python inpaint_image.py "redraw with clean arrow routing" \\
      --image figure.png --mask region_mask.png

  python inpaint_image.py "fix the overlapping labels" \\
      --image figure.png --bbox 100,200,500,600

  python inpaint_image.py "" --image photo.png --mask mask.png --mode remove

  python inpaint_image.py "clean patent line art" \\
      --image figure.png --bbox 300,400,800,700 --num-images 4
        """
    )
    parser.add_argument("prompt", help="What to draw in the masked region (empty for removal)")
    parser.add_argument("--image", "-i", required=True, help="Source image path")
    parser.add_argument("--mask", "-m", help="Mask PNG path (white=edit, black=preserve)")
    parser.add_argument("--bbox", "-b", help="Bounding box x1,y1,x2,y2 (auto-generates mask)")
    parser.add_argument("--output", "-o", default=".", help="Output directory or file path")
    parser.add_argument("--filename", "-f", help="Custom output filename")
    parser.add_argument("--mode", choices=["insert", "remove"], default="insert",
                        help="Edit mode: insert (add content) or remove (erase)")
    parser.add_argument("--mask-dilation", type=float, default=0.01,
                        help="Mask edge expansion 0.0-1.0 (default: 0.01)")
    parser.add_argument("--num-images", "-n", type=int, default=1, choices=[1, 2, 3, 4],
                        help="Number of result candidates (default: 1)")
    parser.add_argument("--negative-prompt", help="What to avoid in the edit")

    args = parser.parse_args()
    inpaint_image(
        prompt=args.prompt, image=args.image, mask=args.mask, bbox=args.bbox,
        output=args.output, filename=args.filename, mode=args.mode,
        mask_dilation=args.mask_dilation, num_images=args.num_images,
        negative_prompt=args.negative_prompt,
    )


if __name__ == "__main__":
    main()
