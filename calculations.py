"""Small, independently testable trapezoidal-channel hydraulic calculator.

Units: SI (m, m^2, m^3/s). This is an educational MVP, not a certified design tool.
Uniform-flow capacity is calculated using Manning's equation; the supplied slope
must be the energy slope applicable to the assumed uniform-flow condition.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite, sqrt
import argparse
import json


@dataclass(frozen=True)
class ChannelInput:
    bottom_width_m: float
    water_depth_m: float
    side_slope_h_to_v: float
    energy_slope: float
    manning_n: float


def _number(value: object, name: str, *, strictly_positive: bool) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name}: booleans are not valid numbers")
    try:
        result = float(value)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError(f"{name}: must be a finite number") from exc
    if not isfinite(result):
        raise ValueError(f"{name}: must be finite")
    if strictly_positive and result <= 0:
        raise ValueError(f"{name}: must be > 0")
    if not strictly_positive and result < 0:
        raise ValueError(f"{name}: must be >= 0")
    return result


def calculate_channel(spec: ChannelInput) -> dict[str, float | list[list[float]]]:
    """Return uniform-flow hydraulics and wetted section coordinates.

    A = h(b + mh), P = b + 2h sqrt(1+m^2), R=A/P,
    V=(1/n) R^(2/3) sqrt(S), Q=AV.
    Here m is horizontal/vertical side-slope ratio on BOTH sides.
    """
    b = _number(spec.bottom_width_m, "bottom_width_m", strictly_positive=True)
    h = _number(spec.water_depth_m, "water_depth_m", strictly_positive=True)
    m = _number(spec.side_slope_h_to_v, "side_slope_h_to_v", strictly_positive=False)
    s = _number(spec.energy_slope, "energy_slope", strictly_positive=True)
    n = _number(spec.manning_n, "manning_n", strictly_positive=True)

    top_width = b + 2 * m * h
    area = h * (b + m * h)
    wetted_perimeter = b + 2 * h * sqrt(1 + m * m)
    if not all(isfinite(v) and v > 0 for v in (top_width, area, wetted_perimeter)):
        raise ValueError("Geometry overflow or invalid cross section")
    radius = area / wetted_perimeter
    velocity = radius ** (2 / 3) * sqrt(s) / n
    discharge = area * velocity
    vertices = [[-m*h, h], [0., 0.], [b, 0.], [b + m*h, h]]
    if not all(isfinite(v) for v in (radius, velocity, discharge, *(coord for p in vertices for coord in p))):
        raise ValueError("Numeric overflow")
    return {
        "top_width_m": top_width,
        "area_m2": area,
        "wetted_perimeter_m": wetted_perimeter,
        "hydraulic_radius_m": radius,
        "velocity_m_per_s": velocity,
        "discharge_m3_per_s": discharge,
        "wetted_section_vertices_m": vertices,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Manning uniform-flow trapezoidal channel MVP")
    parser.add_argument("json_file", help="Path to JSON with ChannelInput keys")
    args = parser.parse_args()
    with open(args.json_file, encoding="utf-8") as f:
        spec = ChannelInput(**json.load(f))
    print(json.dumps(calculate_channel(spec), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
