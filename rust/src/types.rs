use serde::{Deserialize, Serialize};
use pyo3::prelude::*;

/// Environmental conditions
#[pyclass]
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Env {
    #[pyo3(get, set)]
    pub air_density: f64, // kg/m³
    #[pyo3(get, set)]
    pub wind_speed: f64,  // m/s
}

#[pymethods]
impl Env {
    #[new]
    pub fn new(air_density: f64, wind_speed: f64) -> Self {
        Self { air_density, wind_speed }
    }
}

/// Design constraints supplied by the user
#[pyclass]
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Constraints {
    #[pyo3(get, set)]
    pub blade_radius: f64, // m
    #[pyo3(get, set)]
    pub num_blades: u8,
    #[pyo3(get, set)]
    pub generator_type: GeneratorType,
}

#[pymethods]
impl Constraints {
    #[new]
    pub fn new(blade_radius: f64, num_blades: u8, generator_type: GeneratorType) -> Self {
        Self { blade_radius, num_blades, generator_type }
    }
}

/// Supported generator types
#[pyclass]
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub enum GeneratorType {
    Brushed,
    Brushless,
}

/// Complete turbine configuration
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TurbineConfig {
    pub target_wattage: f64,  // W
    pub env: Env,
    pub constraints: Constraints,
}

// Python wrapper types
pub type PyEnv = Env;
pub type PyConstraints = Constraints;
pub type PyGeneratorType = GeneratorType;