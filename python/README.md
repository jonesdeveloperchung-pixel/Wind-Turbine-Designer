# Wind Turbine Designer

A production-ready wind turbine design tool that uses Rust for fast numerical calculations and Python for user interaction, data handling, and visualization.

## Features

- **Fast Rust Core**: Numerically correct calculations using Betz limit, TSR optimization, and power coefficient models
- **Python Interface**: Easy-to-use CLI and optional GUI
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multiple Output Formats**: JSON and CSV export
- **Visualization**: Power curves and design analysis plots
- **IEC Standards Compliance**: Based on IEC-61400-1 guidelines

## Installation

### Prerequisites

- Python 3.8+
- Rust (latest stable)
- Cargo

### Build from Source

1. Clone the repository
2. Run the build script:

```bash
python build.py
```

This will:
- Compile the Rust library
- Install the Python package in development mode
- Set up command-line tools

### Manual Build

If you prefer to build manually:

```bash
# Build Rust library
cd rust
cargo build --release

# Install Python package
cd ../python
pip install -e .
```

## Usage

### Command Line Interface

Generate a turbine design:

```bash
wind-turbine design --wattage 50 --radius 0.5 --wind-speed 6 --output design.json
```

Options:
- `--wattage`: Target power output in watts
- `--air-density`: Air density in kg/m³ (default: 1.225)
- `--wind-speed`: Average wind speed in m/s (default: 6.0)
- `--radius`: Blade radius in meters (default: 0.5)
- `--blades`: Number of blades (default: 3)
- `--generator`: Generator type (brushed/brushless, default: brushless)
- `--output`: Output file path (default: summary.json)

### Graphical User Interface

Launch the GUI:

```bash
wind-turbine-gui
```

### Python API

```python
import wind_calc

# Create configuration
env = wind_calc.PyEnv(air_density=1.225, wind_speed=6.0)
constraints = wind_calc.PyConstraints(
    blade_radius=0.5,
    num_blades=3,
    generator_type=wind_calc.PyGeneratorType.Brushless
)
config = wind_calc.PyTurbineConfig(
    target_wattage=50.0,
    env=env,
    constraints=constraints
)

# Generate design
solver = wind_calc.PySolver(config)
summary = solver.design_summary()
print(summary)
```

### Visualization

```python
from wind_turbine.visualize import plot_power_curve

# Plot power curve
config = {
    'blade_radius': 0.5,
    'air_density': 1.225,
    'cut_in': 2.5,
    'cut_out': 25.0
}
plot_power_curve(config)
```

## Output Format

The design summary includes:

```json
{
  "rotor_area": 0.785,
  "blade_length": 0.5,
  "tsr": 8.12,
  "rpm": 123.4,
  "gear_ratio": 1.0,
  "generator_type": "Brushless",
  "cut_in": 2.5,
  "cut_out": 25.0
}
```

## Testing

Run tests:

```bash
python build.py --test
```

Or manually:

```bash
# Rust tests
cd rust && cargo test

# Python tests
cd python && python -m pytest tests/
```

## Architecture

- **Rust Core** (`rust/src/`): Fast numerical calculations
  - `types.rs`: Data structures
  - `models.rs`: Physics models (Betz limit, TSR, Cp)
  - `core.rs`: Main solver logic
  - `lib.rs`: Python bindings (PyO3)

- **Python Layer** (`python/wind_turbine/`): User interface
  - `cli.py`: Command-line interface
  - `gui.py`: Graphical interface (PySide6)
  - `visualize.py`: Plotting and analysis

## Standards Compliance

This implementation follows IEC-61400-1 guidelines for wind turbine design, including:
- Betz limit calculations
- Tip speed ratio optimization
- Power coefficient modeling
- Cut-in and cut-out wind speeds

## License

MIT License - see LICENSE file for details.