import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from calculations import ChannelInput, calculate_channel


def base(**overrides):
    data = dict(bottom_width_m=3, water_depth_m=2, side_slope_h_to_v=1.5,
                energy_slope=0.001, manning_n=0.015)
    data.update(overrides)
    return ChannelInput(**data)


def test_geometry_and_manning():
    out = calculate_channel(base())
    assert out["top_width_m"] == pytest.approx(9)
    assert out["area_m2"] == pytest.approx(12)
    perimeter = 3 + 4 * math.sqrt(3.25)
    assert out["wetted_perimeter_m"] == pytest.approx(perimeter)
    assert out["discharge_m3_per_s"] == pytest.approx(
        12 / .015 * (12 / perimeter) ** (2/3) * math.sqrt(.001))
    assert out["wetted_section_vertices_m"] == [[-3, 2], [0, 0], [3, 0], [6, 2]]


@pytest.mark.parametrize("field,value", [
    ("bottom_width_m", 0), ("water_depth_m", -1),
    ("side_slope_h_to_v", -0.1), ("energy_slope", 0),
    ("manning_n", 0), ("manning_n", float('nan')),
    ("water_depth_m", float('inf')), ("bottom_width_m", True),
    ("energy_slope", "hello"),
])
def test_invalid_inputs(field, value):
    with pytest.raises(ValueError):
        calculate_channel(base(**{field: value}))


def test_rectangular_section():
    out = calculate_channel(base(side_slope_h_to_v=0))
    assert out["area_m2"] == pytest.approx(6)
    assert out["wetted_perimeter_m"] == pytest.approx(7)
