import json
import click
import pandas as pd
from . import wind_calc  # Rust extension

@click.group()
def cli():
    """Wind Turbine Design CLI"""

@cli.command()
@click.option("--wattage", type=float, required=True, help="Target output wattage")
@click.option("--air-density", type=float, default=1.225, help="Air density kg/m³")
@click.option("--wind-speed", type=float, default=6.0, help="Average wind speed m/s")
@click.option("--radius", type=float, default=0.5, help="Blade radius m")
@click.option("--blades", type=int, default=3, help="Number of blades")
@click.option("--generator", type=click.Choice(["brushed", "brushless"]), default="brushless")
@click.option("--output", type=click.Path(), default="summary.json")
def design(wattage, air_density, wind_speed, radius, blades, generator, output):
    """Generate a turbine design for the given wattage."""
    cfg = wind_calc.PyTurbineConfig(
        target_wattage=wattage,
        env=wind_calc.Env(air_density=air_density, wind_speed=wind_speed),
        constraints=wind_calc.Constraints(
            blade_radius=radius,
            num_blades=blades,
            generator_type=wind_calc.GeneratorType.Brushless if generator == "brushless" else wind_calc.GeneratorType.Brushed
        )
    )
    solver = wind_calc.PySolver(cfg)
    summary = solver.design_summary()
    # Save to JSON
    with open(output, "w") as f:
        json.dump(summary, f, indent=2)
    click.echo(f"Design written to {output}")

    # Optional CSV
    df = pd.DataFrame([summary])
    df.to_csv(output.replace(".json", ".csv"), index=False)
    click.echo(f"CSV written to {output.replace('.json', '.csv')}")

if __name__ == "__main__":
    cli()