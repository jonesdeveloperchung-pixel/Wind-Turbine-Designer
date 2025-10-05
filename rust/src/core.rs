use crate::models::*;
use crate::types::*;
use serde::Serialize;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::f64::consts::PI;

/// Main solver struct exposed to Python
#[derive(Debug)]
pub struct Solver {
    cfg: TurbineConfig,
}

impl Solver {
    pub fn new(cfg: TurbineConfig) -> Self {
        Self { cfg }
    }

    /// Swept area A = π r²
    pub fn rotor_area(&self) -> f64 {
        PI * self.cfg.constraints.blade_radius.powi(2)
    }

    /// Blade length (simple equal to radius)
    pub fn blade_length(&self) -> f64 {
        self.cfg.constraints.blade_radius
    }

    /// Determine required TSR for target wattage
    pub fn required_tsr(&self) -> f64 {
        let area = self.rotor_area();
        let _betz = betz_limit(&self.cfg.env);
        let mut tsr = optimal_tsr(self.cfg.constraints.num_blades);
        // Iterate until power matches target
        for _ in 0..20 {
            let cp = cp_at_tsr(tsr);
            let power = cp * 0.5 * self.cfg.env.air_density * area
                * self.cfg.env.wind_speed.powi(3);
            let err = (power - self.cfg.target_wattage) / self.cfg.target_wattage;
            if err.abs() < 0.01 { break; }
            tsr += -err * tsr * 0.1;
        }
        tsr
    }

    /// Generator RPM = (TSR * wind_speed) / radius * 60/(2π)
    pub fn generator_rpm(&self, tsr: f64) -> f64 {
        let omega = tsr * self.cfg.env.wind_speed / self.cfg.constraints.blade_radius; // rad/s
        omega * 60.0 / (2.0 * PI)
    }

    /// Estimate gearbox ratio if generator is low‑speed
    pub fn gearbox_ratio(&self, rpm: f64, desired_gen_rpm: f64) -> f64 {
        if rpm <= desired_gen_rpm { 1.0 } else { rpm / desired_gen_rpm }
    }

    /// Cut‑in and cut‑off wind speeds (simple)
    pub fn cut_in(&self) -> f64 { 2.5 } // m/s
    pub fn cut_out(&self) -> f64 { 25.0 } // m/s

    /// Full design summary
    pub fn design_summary(&self) -> DesignSummary {
        let tsr = self.required_tsr();
        let rpm = self.generator_rpm(tsr);
        let gear = self.gearbox_ratio(rpm, 1500.0); // 1.5 kRPM typical
        DesignSummary {
            rotor_area: self.rotor_area(),
            blade_length: self.blade_length(),
            tsr,
            rpm,
            gear_ratio: gear,
            generator_type: self.cfg.constraints.generator_type,
            cut_in: self.cut_in(),
            cut_out: self.cut_out(),
        }
    }
}

/// Result struct – serialisable to JSON/CSV
#[derive(Debug, Serialize)]
pub struct DesignSummary {
    pub rotor_area: f64,
    pub blade_length: f64,
    pub tsr: f64,
    pub rpm: f64,
    pub gear_ratio: f64,
    pub generator_type: GeneratorType,
    pub cut_in: f64,
    pub cut_out: f64,
}

impl IntoPy<PyObject> for DesignSummary {
    fn into_py(self, py: Python) -> PyObject {
        let dict = PyDict::new(py);
        dict.set_item("rotor_area", self.rotor_area).unwrap();
        dict.set_item("blade_length", self.blade_length).unwrap();
        dict.set_item("tsr", self.tsr).unwrap();
        dict.set_item("rpm", self.rpm).unwrap();
        dict.set_item("gear_ratio", self.gear_ratio).unwrap();
        dict.set_item("generator_type", format!("{:?}", self.generator_type)).unwrap();
        dict.set_item("cut_in", self.cut_in).unwrap();
        dict.set_item("cut_out", self.cut_out).unwrap();
        dict.into()
    }
}