"""CineVista geometry reference, NOT an Android/camera implementation.

Landscape, encoded-pixel horizontal squeeze, EXIF orientation 1 only.
No images are read or resampled. Rectangles use floating-point edge coordinates
with half-open semantics [left, right), [top, bottom). Encoder alignment,
interpolation, color processing and camera/EVF calibration are not simulated.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math


@dataclass(frozen=True)
class Rect:
    left: float
    top: float
    right: float
    bottom: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top


@dataclass(frozen=True)
class FramePlan:
    source_width: int
    source_height: int
    squeeze: float
    target_aspect: float
    source_crop: Rect
    retained_area_fraction: float
    output_width: int
    output_height: int
    output_aspect_relative_error: float
    output_policy: str


def _positive_finite(name: str, value: float) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric, not bool")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite positive number") from exc
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    return result


def _size(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 2:
        raise ValueError(f"{name} must be an integer >= 2")
    return value


def _offset(name: str, value: float) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be within [-1, 1]") from exc
    if not math.isfinite(result) or not -1 <= result <= 1:
        raise ValueError(f"{name} must be within [-1, 1]")
    return result


def plan_frame(width: int, height: int, squeeze: float = 1.0,
               target_aspect: float | None = None,
               offset_x: float = 0.0, offset_y: float = 0.0,
               output_policy: str = "compact",
               output_width: int | None = None,
               orientation: int = 1) -> FramePlan:
    """Plan maximal-area crop and de-squeeze; no camera capability is implied.

    target_aspect=None keeps the complete naturally de-squeezed image.
    compact keeps at most the source crop's horizontal sample count.
    expanded permits horizontal interpolation up to crop_width * squeeze.
    output_width is an optional cap, never an instruction to upscale further.
    Integer height is rounded nearest; this reference does not require even
    dimensions, since actual encoder alignment constraints must be measured.
    """
    width = _size("width", width)
    height = _size("height", height)
    s = _positive_finite("squeeze", squeeze)
    if s < 1.0:
        raise ValueError("This reference only supports squeeze >= 1")
    if orientation != 1:
        raise ValueError("Reference supports EXIF orientation 1 only; do not silently rotate")
    ox = _offset("offset_x", offset_x)
    oy = _offset("offset_y", offset_y)
    if output_policy not in ("compact", "expanded"):
        raise ValueError("output_policy must be compact or expanded")
    if output_width is not None:
        output_width = _size("output_width", output_width)

    natural = width * s / height
    r = natural if target_aspect is None else _positive_finite("target_aspect", target_aspect)
    # Target in raw/encoded coordinates: horizontal expansion is undone here.
    raw_ratio = r / s
    if width / height >= raw_ratio:
        crop_h = float(height)
        crop_w = min(float(width), crop_h * raw_ratio)
    else:
        crop_w = float(width)
        crop_h = min(float(height), crop_w / raw_ratio)
    x = max(0.0, width - crop_w) * (ox + 1.0) / 2.0
    y = max(0.0, height - crop_h) * (oy + 1.0) / 2.0
    crop = Rect(x, y, x + crop_w, y + crop_h)
    nominal_width = crop_w if output_policy == "compact" else crop_w * s
    maximum_width = nominal_width if output_width is None else min(nominal_width, output_width)
    ow = int(math.floor(maximum_width + 1e-9))
    oh = int(math.floor(ow / r + 0.5))
    if ow < 2 or oh < 2:
        raise ValueError("Requested frame/export is too small")
    return FramePlan(width, height, s, r, crop, crop_w * crop_h / (width * height),
                     ow, oh, abs(ow / oh - r) / r, output_policy)


def fit_display(target_aspect: float, framebuffer_width: int,
                framebuffer_height: int, display_pixel_aspect: float = 1.0) -> Rect:
    """Fit the whole frame into a display, accounting for physical pixel shape.

    pixel_aspect = physical_display_aspect / framebuffer_aspect.
    Target rectangle pixel ratio must be target_aspect / pixel_aspect.
    Does NOT prove that Sony's live-preview plane accepts this rectangle.
    """
    r = _positive_finite("target_aspect", target_aspect)
    pw = _size("framebuffer_width", framebuffer_width)
    ph = _size("framebuffer_height", framebuffer_height)
    p = _positive_finite("display_pixel_aspect", display_pixel_aspect)
    pixel_ratio = r / p
    if pw / ph >= pixel_ratio:
        h = float(ph)
        w = h * pixel_ratio
    else:
        w = float(pw)
        h = w / pixel_ratio
    return Rect((pw-w)/2, (ph-h)/2, (pw+w)/2, (ph+h)/2)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=7952)
    parser.add_argument("--height", type=int, default=5304)
    parser.add_argument("--squeeze", type=float, default=1.0)
    parser.add_argument("--aspect", type=float, default=65/24)
    parser.add_argument("--policy", choices=("compact", "expanded"), default="compact")
    args = parser.parse_args()
    try:
        plan = plan_frame(args.width, args.height, args.squeeze, args.aspect,
                          output_policy=args.policy)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(asdict(plan), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
