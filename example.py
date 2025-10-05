#!/usr/bin/env python3
"""
Example usage of the Wind Turbine Designer
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python', 'wind_turbine'))
import wind_calc
from wind_turbine.visualize import plot_power_curve, plot_tsr_analysis

def basic_design_example():
    """Basic turbine design example"""
    print("=== Basic Wind Turbine Design ===")
    
    # Create environmental conditions
    env = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    print(f"Environment: {env.air_density} kg/m³, {env.wind_speed} m/s")
    
    # Define design constraints
    constraints = wind_calc.Constraints(
        blade_radius=0.5,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    print(f"Constraints: {constraints.blade_radius}m radius, {constraints.num_blades} blades")
    
    # Create turbine configuration
    config = wind_calc.PyTurbineConfig(
        target_wattage=50.0,
        env=env,
        constraints=constraints
    )
    print(f"Target: {config.target_wattage}W")
    
    # Generate design
    solver = wind_calc.PySolver(config)
    summary = solver.design_summary()
    
    print("\n--- Design Results ---")
    print(f"Rotor area: {summary['rotor_area']:.2f} m²")
    print(f"Blade length: {summary['blade_length']:.2f} m")
    print(f"Optimal TSR: {summary['tsr']:.1f}")
    print(f"Generator RPM: {summary['rpm']:.0f}")
    print(f"Gear ratio: {summary['gear_ratio']:.1f}")
    print(f"Generator type: {summary['generator_type']}")
    print(f"Cut-in speed: {summary['cut_in']} m/s")
    print(f"Cut-out speed: {summary['cut_out']} m/s")
    
    return summary

def comparison_example():
    """Compare different turbine designs"""
    print("\n=== Design Comparison ===")
    
    designs = {}
    
    # Small turbine
    env1 = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    constraints1 = wind_calc.Constraints(
        blade_radius=0.4,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    config1 = wind_calc.PyTurbineConfig(target_wattage=25.0, env=env1, constraints=constraints1)
    solver1 = wind_calc.PySolver(config1)
    designs['Small (25W)'] = solver1.design_summary()
    
    # Medium turbine
    env2 = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    constraints2 = wind_calc.Constraints(
        blade_radius=0.6,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    config2 = wind_calc.PyTurbineConfig(target_wattage=75.0, env=env2, constraints=constraints2)
    solver2 = wind_calc.PySolver(config2)
    designs['Medium (75W)'] = solver2.design_summary()
    
    # Large turbine
    env3 = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    constraints3 = wind_calc.Constraints(
        blade_radius=0.8,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    config3 = wind_calc.PyTurbineConfig(target_wattage=150.0, env=env3, constraints=constraints3)
    solver3 = wind_calc.PySolver(config3)
    designs['Large (150W)'] = solver3.design_summary()
    
    for name, design in designs.items():
        print(f"\n{name}:")
        print(f"  Rotor area: {design['rotor_area']:.2f} m²")
        print(f"  TSR: {design['tsr']:.1f}")
        print(f"  RPM: {design['rpm']:.0f}")
    
    return designs

def visualization_example():
    """Demonstrate visualization capabilities"""
    print("\n=== Visualization Examples ===")
    
    # Power curve for a specific design
    config = {
        'blade_radius': 0.6,
        'air_density': 1.225,
        'cut_in': 2.5,
        'cut_out': 25.0
    }
    
    print("Generating power curve plot...")
    try:
        plot_power_curve(config)
        print("✓ Power curve plotted successfully")
    except Exception as e:
        print(f"✗ Power curve plotting failed: {e}")
    
    print("Generating TSR analysis plot...")
    try:
        plot_tsr_analysis(blade_radius=0.6, wind_speeds=[4, 6, 8, 10])
        print("✓ TSR analysis plotted successfully")
    except Exception as e:
        print(f"✗ TSR analysis plotting failed: {e}")

def main():
    """Main example function"""
    print("Wind Turbine Designer - Example Usage")
    print("=" * 50)
    
    try:
        # Basic design
        basic_summary = basic_design_example()
        
        # Comparison
        designs = comparison_example()
        
        # Visualization (optional - requires display)
        if "--plot" in sys.argv:
            visualization_example()
        else:
            print("\nNote: Add --plot flag to see visualization examples")
        
        print("\n" + "=" * 50)
        print("Example completed successfully!")
        print("\nTry running:")
        print("  python example.py --plot")
        print("  wind-turbine design --wattage 100 --radius 0.7")
        print("  wind-turbine-gui")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())