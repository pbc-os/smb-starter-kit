#!/usr/bin/env python3
"""
Convert a background-removed image to actual RGBA transparency.

Gemini's background removal renders a checkerboard pattern to visually
represent transparency, but outputs RGB with no alpha channel. This script
detects the checkerboard/white background and converts it to real RGBA
transparency.

Usage:
    python make_transparent.py input.png --output output-transparent.png
    python make_transparent.py input.png --threshold 220 --output clean.png

This is Pass 3 in the web-asset pipeline:
  generate (Pass 1) → remove bg (Pass 2) → make_transparent (Pass 3) → web-ready
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    missing = []
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    try:
        import numpy as np
    except ImportError:
        missing.append("numpy")
    print(f"Error: Missing packages: {', '.join(missing)}")
    print(f"  Run: pip install {' '.join(missing)}")
    sys.exit(1)


def generate_filename(extension=".png"):
    """Generate a unique filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"transparent_{timestamp}{extension}"


def detect_checkerboard_background(img_array, threshold=220, check_size=8):
    """
    Detect checkerboard transparency pattern that Gemini renders.

    Gemini renders "transparent" backgrounds as a checkerboard of light gray
    pixels typically in the 220-240 range. This function detects those pixels
    and uses flood fill from edges to find the connected background region.

    Returns a boolean mask where True = background (to be made transparent).
    """
    # Convert to grayscale for analysis
    if len(img_array.shape) == 3:
        gray = np.mean(img_array[:, :, :3], axis=2)
    else:
        gray = img_array.astype(float)

    from scipy import ndimage

    # Detect pixels that are uniformly bright (all channels similar, high value)
    # This catches both solid white backgrounds and checkerboard patterns
    if len(img_array.shape) == 3:
        r, g, b = img_array[:,:,0].astype(float), img_array[:,:,1].astype(float), img_array[:,:,2].astype(float)
        # Background pixels have low color variance (gray/white) and high brightness
        color_variance = np.maximum(np.maximum(np.abs(r - g), np.abs(r - b)), np.abs(g - b))
        is_neutral = color_variance < 25  # Low color saturation
        is_bright = gray > threshold
        candidate_bg = is_neutral & is_bright
    else:
        candidate_bg = gray > threshold

    # Step 4: Flood fill from edges to find connected background regions
    # This prevents removing bright areas inside the subject
    edge_mask = np.zeros_like(candidate_bg)
    edge_mask[0, :] = True
    edge_mask[-1, :] = True
    edge_mask[:, 0] = True
    edge_mask[:, -1] = True

    # Label connected components of candidate background
    labeled, num_features = ndimage.label(candidate_bg)

    # Find which labels touch the edges
    edge_labels = set(labeled[edge_mask & candidate_bg].flatten())
    edge_labels.discard(0)  # Remove background label

    # Background = candidate pixels connected to edges
    background = np.zeros_like(candidate_bg)
    for label in edge_labels:
        background |= (labeled == label)

    return background


def detect_white_background(img_array, threshold=220):
    """
    Simple white background detection for images without checkerboard.

    Flood fills from edges to find connected near-white regions.
    """
    from scipy import ndimage

    if len(img_array.shape) == 3:
        gray = np.mean(img_array[:, :, :3], axis=2)
    else:
        gray = img_array.astype(float)

    bright = gray > threshold

    # Flood fill from edges
    edge_mask = np.zeros_like(bright)
    edge_mask[0, :] = True
    edge_mask[-1, :] = True
    edge_mask[:, 0] = True
    edge_mask[:, -1] = True

    labeled, _ = ndimage.label(bright)
    edge_labels = set(labeled[edge_mask & bright].flatten())
    edge_labels.discard(0)

    background = np.zeros_like(bright)
    for label in edge_labels:
        background |= (labeled == label)

    return background


def make_transparent(input_path, output=None, filename=None, threshold=220,
                     feather=1, mode="auto"):
    """
    Convert background to actual RGBA transparency.

    Args:
        input_path: Path to input image
        output: Output directory or file path
        filename: Custom filename
        threshold: Brightness threshold for background detection (0-255)
        feather: Edge feathering radius in pixels (0 = hard edges)
        mode: Detection mode - "auto", "checkerboard", or "white"
    """
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"Error: Image not found: {input_path}")
        sys.exit(1)

    img = Image.open(input_path)
    print(f"Processing: {input_path}")
    print(f"  Size: {img.size}, Mode: {img.mode}")

    # If already RGBA with transparency, skip
    if img.mode == "RGBA":
        alpha = np.array(img.getchannel("A"))
        transparent_pct = (alpha < 10).sum() / alpha.size * 100
        if transparent_pct > 5:
            print(f"  Image already has {transparent_pct:.0f}% transparent pixels. Skipping.")
            return input_path

    # Convert to RGB array for analysis
    img_rgb = img.convert("RGB")
    arr = np.array(img_rgb)

    # Detect background
    print(f"  Detection mode: {mode}, threshold: {threshold}")

    if mode == "auto":
        # Try checkerboard first, fall back to white
        try:
            bg_mask = detect_checkerboard_background(arr, threshold)
            bg_pct = bg_mask.sum() / bg_mask.size * 100
            if bg_pct < 5 or bg_pct > 95:
                # Checkerboard detection didn't find a reasonable background
                bg_mask = detect_white_background(arr, threshold)
                print("  Using white background detection")
            else:
                print(f"  Checkerboard background detected ({bg_pct:.0f}% of image)")
        except ImportError:
            # scipy not available, use simple threshold
            print("  scipy not available, using simple threshold detection")
            bg_mask = detect_white_background_simple(arr, threshold)
    elif mode == "checkerboard":
        bg_mask = detect_checkerboard_background(arr, threshold)
    elif mode == "white":
        bg_mask = detect_white_background(arr, threshold)
    else:
        print(f"Error: Invalid mode '{mode}'. Use 'auto', 'checkerboard', or 'white'.")
        sys.exit(1)

    bg_pct = bg_mask.sum() / bg_mask.size * 100
    print(f"  Background pixels: {bg_pct:.1f}%")

    if bg_pct < 1:
        print("  Warning: Very little background detected. Result may not look right.")
        print("  Try adjusting --threshold (lower = more aggressive)")

    # Create alpha channel (255 = opaque, 0 = transparent)
    alpha = np.where(bg_mask, 0, 255).astype(np.uint8)

    # Optional edge feathering for smoother edges
    if feather > 0:
        try:
            from scipy.ndimage import gaussian_filter
            alpha_float = gaussian_filter(alpha.astype(float), sigma=feather)
            alpha = np.clip(alpha_float, 0, 255).astype(np.uint8)
            print(f"  Applied {feather}px edge feathering")
        except ImportError:
            pass  # Skip feathering if scipy not available

    # Combine RGB + Alpha
    rgba = np.dstack([arr, alpha])
    result = Image.fromarray(rgba, "RGBA")

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.parent

    if output_path.is_dir() or not output_path.suffix:
        output_path.mkdir(parents=True, exist_ok=True)
        fname = filename if filename else f"{input_path.stem}-transparent.png"
        output_path = output_path / fname
    else:
        if filename:
            output_path = output_path.parent / filename

    # Force PNG extension
    if output_path.suffix.lower() != ".png":
        output_path = output_path.with_suffix(".png")

    result.save(output_path, "PNG")

    # Verify
    verify = Image.open(output_path)
    if verify.mode == "RGBA":
        v_alpha = np.array(verify.getchannel("A"))
        t_pct = (v_alpha < 10).sum() / v_alpha.size * 100
        o_pct = (v_alpha > 245).sum() / v_alpha.size * 100
        print(f"  Saved: {output_path}")
        print(f"  Result: {t_pct:.0f}% transparent, {o_pct:.0f}% opaque, RGBA mode")
        print("PASS: Transparent PNG created")
    else:
        print(f"  Warning: Output is {verify.mode}, expected RGBA")

    return output_path


def detect_white_background_simple(img_array, threshold=220):
    """Fallback: simple brightness threshold without scipy."""
    if len(img_array.shape) == 3:
        gray = np.mean(img_array[:, :, :3], axis=2)
    else:
        gray = img_array.astype(float)

    # Simple threshold — may include bright subject areas
    return gray > threshold


def main():
    parser = argparse.ArgumentParser(
        description="Convert background-removed images to actual RGBA transparency",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script fixes a common issue where Gemini's background removal
renders a checkerboard pattern instead of actual transparency.

Examples:
  python make_transparent.py image.png
  python make_transparent.py image.png --output ./assets/
  python make_transparent.py image.png --threshold 230 --feather 2
  python make_transparent.py image.png --mode white --threshold 250
        """
    )
    parser.add_argument("input", help="Input image path (from background removal pass)")
    parser.add_argument("--output", "-o", help="Output directory or file path")
    parser.add_argument("--filename", "-f", help="Custom output filename")
    parser.add_argument("--threshold", "-t", type=int, default=220,
                        help="Brightness threshold for background detection 0-255 (default: 220)")
    parser.add_argument("--feather", type=int, default=1,
                        help="Edge feathering radius in pixels (default: 1, 0 = hard edges)")
    parser.add_argument("--mode", choices=["auto", "checkerboard", "white"], default="auto",
                        help="Background detection mode (default: auto)")

    args = parser.parse_args()
    make_transparent(
        input_path=args.input, output=args.output, filename=args.filename,
        threshold=args.threshold, feather=args.feather, mode=args.mode
    )


if __name__ == "__main__":
    main()
