#[cfg(test)]
mod tests {
    use crate::core::Solver;
    use crate::types::*;

    #[test]
    fn test_rotor_area() {
        let cfg = TurbineConfig {
            target_wattage: 50.0,
            env: Env { air_density: 1.225, wind_speed: 6.0 },
            constraints: Constraints {
                blade_radius: 0.5,
                num_blades: 3,
                generator_type: GeneratorType::Brushless,
            },
        };
        let s = Solver::new(cfg);
        assert!((s.rotor_area() - std::f64::consts::PI * 0.25).abs() < 1e-6);
    }

    #[test]
    fn test_design_summary() {
        let cfg = TurbineConfig {
            target_wattage: 100.0,
            env: Env { air_density: 1.225, wind_speed: 8.0 },
            constraints: Constraints {
                blade_radius: 0.6,
                num_blades: 3,
                generator_type: GeneratorType::Brushless,
            },
        };
        let s = Solver::new(cfg);
        let summary = s.design_summary();
        
        assert!(summary.rotor_area > 0.0);
        assert_eq!(summary.blade_length, 0.6);
        assert!(summary.tsr > 0.0);
        assert!(summary.rpm > 0.0);
        assert_eq!(summary.cut_in, 2.5);
        assert_eq!(summary.cut_out, 25.0);
    }
}