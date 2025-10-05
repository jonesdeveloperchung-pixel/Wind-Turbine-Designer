import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'wind_turbine'))
import wind_calc

def test_env_creation():
    """Test environmental conditions creation"""
    env = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    assert env.air_density == 1.225
    assert env.wind_speed == 6.0

def test_constraints_creation():
    """Test design constraints creation"""
    constraints = wind_calc.Constraints(
        blade_radius=0.5,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    assert constraints.blade_radius == 0.5
    assert constraints.num_blades == 3

def test_turbine_config_creation():
    """Test turbine configuration creation"""
    env = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    constraints = wind_calc.Constraints(
        blade_radius=0.5,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    cfg = wind_calc.PyTurbineConfig(
        target_wattage=50.0,
        env=env,
        constraints=constraints
    )
    assert cfg.target_wattage == 50.0

def test_solver_design_summary():
    """Test solver design summary generation"""
    env = wind_calc.Env(air_density=1.225, wind_speed=6.0)
    constraints = wind_calc.Constraints(
        blade_radius=0.5,
        num_blades=3,
        generator_type=wind_calc.GeneratorType.Brushless
    )
    cfg = wind_calc.PyTurbineConfig(
        target_wattage=50.0,
        env=env,
        constraints=constraints
    )
    solver = wind_calc.PySolver(cfg)
    summary = solver.design_summary()
    
    # Check that all expected keys are present
    expected_keys = [
        "rotor_area", "blade_length", "tsr", "rpm", 
        "gear_ratio", "generator_type", "cut_in", "cut_out"
    ]
    for key in expected_keys:
        assert key in summary
    
    # Check some basic constraints
    assert summary["rotor_area"] > 0
    assert summary["blade_length"] == 0.5
    assert summary["tsr"] > 0
    assert summary["rpm"] > 0
    assert summary["cut_in"] == 2.5
    assert summary["cut_out"] == 25.0