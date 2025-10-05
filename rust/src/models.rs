use crate::types::*;

/// Betz limit calculation
pub fn betz_limit(env: &Env) -> f64 {
    16.0 / 27.0 * 0.5 * env.air_density * env.wind_speed.powi(3)
}

/// Optimal tip speed ratio (empirical for IEC 61400‑1)
pub fn optimal_tsr(num_blades: u8) -> f64 {
    // Simplified empirical relation
    7.0 + 0.5 * (num_blades as f64)
}

/// Power coefficient (Cp) at given TSR – analytical Blasius model
pub fn cp_at_tsr(tsr: f64) -> f64 {
    // Example analytical form (not real)
    let a = 0.5;
    let b = 0.3;
    let c = 0.02;
    let tsr = tsr.max(0.0);
    a * tsr * (1.0 - b * tsr + c * tsr.powi(2))
}