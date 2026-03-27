#!/usr/bin/env python3
"""
Edit existing images with text prompts using Google Gemini's Nano Banana models.

Usage:
    python edit_image.py "your edit prompt" --images image.png [options]

Examples:
    python edit_image.py "remove the background" --images photo.png
    python edit_image.py "combine into a collage" --images img1.png img2.png img3.png
"""

import argparse
import mimetypes
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("  Run: pip install google-genai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
    env_local = Path(".env.local")
    if env_local.exists():
        load_dotenv(env_local)
except ImportError:
    pass  # dotenv is optional

VALID_ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
VALID_MODELS = ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"]
DEFAULT_MODEL = "gemini-2.5-flash-image"
SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".webp", ".gif"]


def get_api_key():
    """Get API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        print("  Set it via: export GEMINI_API_KEY=your_key")
        print("  Or add to .env file: GEMINI_API_KEY=your_key")
        print("  Get a key at: https://aistudio.google.com/apikey")
        sys.exit(1)
    return api_key


def generate_filename(extension=".png"):
    """Generate a unique filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"edited_{timestamp}{extension}"


def get_mime_type(file_path: Path) -> str:
    """Get MIME type for an image file."""
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        mime_type = "image/png"
    return mime_type


def load_image(image_path: Path) -> "types.Part":
    """Load an image file and return as a Gemini Part."""
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    if image_path.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"Error: Unsupported image format: {image_path.suffix}")
        print(f"  Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        sys.exit(1)

    with open(image_path, "rb") as f:
        image_data = f.read()

    mime_type = get_mime_type(image_path)
    return types.Part.from_bytes(data=image_data, mime_type=mime_type)


def save_image(image_data: bytes, output_path: Path) -> Path:
    """Save image data to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


def build_prompt_with_aspect(prompt: str, aspect_ratio: str = None) -> str:
    """Build a prompt that includes aspect ratio guidance if specified."""
    if not aspect_ratio:
        return prompt

    aspect_descriptions = {
        "1:1": "square format",
        "2:3": "vertical portrait format (2:3)",
        "3:2": "horizontal landscape format (3:2)",
        "3:4": "vertical portrait format (3:4)",
        "4:3": "horizontal format (4:3)",
        "4:5": "vertical format (4:5)",
        "5:4": "horizontal format (5:4)",
        "9:16": "tall vertical format (9:16)",
        "16:9": "widescreen horizontal format (16:9)",
        "21:9": "ultra-wide cinematic format (21:9)"
    }
    aspect_hint = aspect_descriptions.get(aspect_ratio, f"{aspect_ratio} aspect ratio")
    if "aspect" not in prompt.lower() and "ratio" not in prompt.lower() and "format" not in prompt.lower():
        return f"Output in {aspect_hint}. {prompt}"
    return prompt


def edit_image(prompt, images, output=".", filename=None, aspect_ratio=None, model=DEFAULT_MODEL):
    """Edit image(s) with a text prompt."""
    if not images:
        print("Error: At least one image is required.")
        sys.exit(1)

    image_paths = [Path(img) for img in images]

    if aspect_ratio and aspect_ratio not in VALID_ASPECT_RATIOS:
        print(f"Error: Invalid aspect ratio '{aspect_ratio}'")
        print(f"  Valid options: {', '.join(VALID_ASPECT_RATIOS)}")
        sys.exit(1)

    if model not in VALID_MODELS:
        print(f"Error: Invalid model '{model}'")
        print(f"  Valid options: {', '.join(VALID_MODELS)}")
        sys.exit(1)

    if len(image_paths) > 14:
        print(f"Error: Maximum 14 images supported, got {len(image_paths)}")
        sys.exit(1)

    output_path = Path(output)
    if output_path.is_dir() or not output_path.suffix:
        output_path.mkdir(parents=True, exist_ok=True)
        fname = filename if filename else generate_filename()
        output_path = output_path / fname
    else:
        if filename:
            output_path = output_path.parent / filename

    if output_path.suffix.lower() not in [".png", ".jpg", ".jpeg", ".webp"]:
        output_path = output_path.with_suffix(".png")

    full_prompt = build_prompt_with_aspect(prompt, aspect_ratio)

    print(f"Editing image{'s' if len(image_paths) > 1 else ''}...")
    print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"  Input: {', '.join(str(p) for p in image_paths)}")
    print(f"  Model: {model}")
    if aspect_ratio:
        print(f"  Aspect Ratio: {aspect_ratio}")

    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    image_parts = [load_image(p) for p in image_paths]
    contents = [full_prompt] + image_parts
    config = types.GenerateContentConfig(response_modalities=["IMAGE"])

    try:
        response = client.models.generate_content(
            model=model, contents=contents, config=config
        )

        if not response.candidates:
            print("Error: No image generated. The prompt may have been blocked.")
            sys.exit(1)

        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            print("Error: No image data in response.")
            sys.exit(1)

        image_part = None
        for part in candidate.content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_part = part
                break

        if not image_part:
            print("Error: No image found in response.")
            for part in candidate.content.parts:
                if hasattr(part, "text") and part.text:
                    print(f"  Response: {part.text}")
            sys.exit(1)

        image_data = image_part.inline_data.data
        mime_type = image_part.inline_data.mime_type

        if mime_type == "image/png":
            if output_path.suffix.lower() != ".png":
                output_path = output_path.with_suffix(".png")
        elif mime_type in ["image/jpeg", "image/jpg"]:
            if output_path.suffix.lower() not in [".jpg", ".jpeg"]:
                output_path = output_path.with_suffix(".jpg")
        elif mime_type == "image/webp":
            if output_path.suffix.lower() != ".webp":
                output_path = output_path.with_suffix(".webp")

        saved_path = save_image(image_data, output_path)
        print(f"Edited image saved to: {saved_path.absolute()}")
        return saved_path

    except Exception as e:
        print(f"Error editing image: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Edit images with text prompts using Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python edit_image.py "remove the background" --images photo.png
  python edit_image.py "make it look like sunset" --images landscape.jpg --aspect-ratio 16:9
  python edit_image.py "combine into a collage" --images img1.png img2.png img3.png
  python edit_image.py "add a hat to the person" --images portrait.png --output edited.png
        """
    )
    parser.add_argument("prompt", help="Text description of the edit to apply")
    parser.add_argument("--images", "-i", nargs="+", required=True, help="One or more input image paths")
    parser.add_argument("--output", "-o", default=".", help="Output directory or file path (default: current directory)")
    parser.add_argument("--filename", "-f", help="Custom filename for the edited image")
    parser.add_argument("--aspect-ratio", "-a", choices=VALID_ASPECT_RATIOS, help="Output aspect ratio (optional)")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, choices=VALID_MODELS, help=f"Gemini model to use (default: {DEFAULT_MODEL})")

    args = parser.parse_args()
    edit_image(
        prompt=args.prompt, images=args.images, output=args.output,
        filename=args.filename, aspect_ratio=args.aspect_ratio, model=args.model
    )


if __name__ == "__main__":
    main()
