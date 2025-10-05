use pyo3::prelude::*;
mod types;
mod models;
mod core;

#[cfg(test)]
mod tests;

use crate::core::Solver;
use crate::types::*;

/// Expose Rust structs to Python
#[pyclass]
#[derive(Clone)]
pub struct PyTurbineConfig {
    #[pyo3(get, set)]
    target_wattage: f64,
    #[pyo3(get, set)]
    env: Env,
    #[pyo3(get, set)]
    constraints: Constraints,
}

#[pymethods]
impl PyTurbineConfig {
    #[new]
    pub fn new(target_wattage: f64, env: Env, constraints: Constraints) -> Self {
        Self { target_wattage, env, constraints }
    }
}

/// Wrapper around Solver
#[pyclass]
pub struct PySolver {
    solver: Solver,
}

#[pymethods]
impl PySolver {
    #[new]
    pub fn new(cfg: PyTurbineConfig) -> Self {
        let cfg: TurbineConfig = cfg.into(); // implement From
        Self { solver: Solver::new(cfg) }
    }

    /// Return design summary as Python dict
    pub fn design_summary(&self) -> PyResult<PyObject> {
        let summary = self.solver.design_summary();
        Python::with_gil(|py| Ok(summary.into_py(py)))
    }
}

/// Implement conversion
impl From<PyTurbineConfig> for TurbineConfig {
    fn from(p: PyTurbineConfig) -> Self {
        TurbineConfig {
            target_wattage: p.target_wattage,
            env: p.env,
            constraints: p.constraints,
        }
    }
}

/// Module entry point
#[pymodule]
fn wind_calc(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyEnv>()?;
    m.add_class::<PyConstraints>()?;
    m.add_class::<PyGeneratorType>()?;
    m.add_class::<PyTurbineConfig>()?;
    m.add_class::<PySolver>()?;
    Ok(())
}