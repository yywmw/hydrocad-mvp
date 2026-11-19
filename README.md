# HydroCAD MVP — trapezoidal channel prototype

A **standalone, public demonstration** of input validation, exact trapezoidal wetted-section geometry, and Manning uniform-flow calculations. It is **not** extracted from YY-Web-V2, and is **not a validated engineering design product**.

## Run

Requires Python >= 3.10. No runtime dependencies.

```bash
python calculations.py example.json
```

Tests (pytest required):

```bash
python -m pip install pytest
python -m pytest -q
```

## Inputs (SI units)

- `bottom_width_m`: channel bottom width, strictly positive, m
- `water_depth_m`: flowing depth, strictly positive, m
- `side_slope_h_to_v`: *horizontal : vertical* bank side slope, nonnegative, symmetrical
- `energy_slope`: dimensionless energy gradient **assuming uniform flow**, strictly positive
- `manning_n`: Manning roughness coefficient, strictly positive (SI formulation)

## Mathematics

For bottom width `b`, water depth `h`, and bank slope `m` (H:V):

- Area: `A = h * (b + m*h)`
- Wetted perimeter: `P = b + 2*h*sqrt(1+m^2)`
- Hydraulic radius: `R = A/P`
- Velocity: `V = R^(2/3)*sqrt(S)/n`
- Discharge: `Q = A*V`

Wetted profile points: `(-m*h, h) -> (0,0) -> (b,0) -> (b+m*h,h)`.

**Limitations:** Does not determine water depth from specified discharge; does not assess freeboard, flood safety, nonuniform flow, transitions, permissible velocities, code compliance, or DXF export. Input validation checks numeric integrity, *not* engineering applicability. Any real-world use requires independent engineering review and applicable standards.
