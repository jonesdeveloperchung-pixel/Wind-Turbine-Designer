import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def power_curve(cfg, min_v=0.0, max_v=25.0, steps=200):
    """Generate power curve data for visualization"""
    v = np.linspace(min_v, max_v, steps)
    area = np.pi * cfg['blade_radius']**2
    # Simplified: Cp = 0.4, rotor speed ~ TSR * V / R
    tsr = 7.0
    cp = 0.4
    power = cp * 0.5 * cfg['air_density'] * area * v**3
    # Cut‑in/out clipping
    power[(v < cfg['cut_in']) | (v > cfg['cut_out'])] = 0
    return pd.DataFrame({"wind_speed": v, "power": power})

def plot_power_curve(cfg):
    """Plot power curve for the turbine configuration"""
    df = power_curve(cfg)
    plt.figure(figsize=(10, 6))
    plt.plot(df['wind_speed'], df['power'] / 1000, label="Power (kW)", linewidth=2)
    plt.xlabel("Wind speed (m/s)")
    plt.ylabel("Power (kW)")
    plt.title("Wind Turbine Power Curve")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 25)
    plt.ylim(0, None)
    plt.show()

def plot_design_comparison(designs):
    """Compare multiple turbine designs"""
    plt.figure(figsize=(12, 8))
    
    for i, (name, cfg) in enumerate(designs.items()):
        df = power_curve(cfg)
        plt.plot(df['wind_speed'], df['power'] / 1000, 
                label=f"{name} ({cfg['blade_radius']:.1f}m radius)", 
                linewidth=2)
    
    plt.xlabel("Wind speed (m/s)")
    plt.ylabel("Power (kW)")
    plt.title("Wind Turbine Design Comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 25)
    plt.ylim(0, None)
    plt.show()

def plot_tsr_analysis(blade_radius=0.5, wind_speeds=[4, 6, 8, 10]):
    """Analyze TSR vs power coefficient"""
    tsr_range = np.linspace(1, 15, 100)
    
    plt.figure(figsize=(12, 5))
    
    # Plot Cp vs TSR
    plt.subplot(1, 2, 1)
    cp_values = []
    for tsr in tsr_range:
        # Simplified Cp model
        a, b, c = 0.5, 0.3, 0.02
        cp = a * tsr * (1.0 - b * tsr + c * tsr**2)
        cp_values.append(max(0, cp))
    
    plt.plot(tsr_range, cp_values, 'b-', linewidth=2)
    plt.xlabel("Tip Speed Ratio (TSR)")
    plt.ylabel("Power Coefficient (Cp)")
    plt.title("Power Coefficient vs TSR")
    plt.grid(True, alpha=0.3)
    
    # Plot RPM vs wind speed for different TSRs
    plt.subplot(1, 2, 2)
    wind_speeds_range = np.linspace(2, 20, 100)
    
    for tsr in [6, 7, 8, 9, 10]:
        rpm_values = []
        for v in wind_speeds_range:
            omega = tsr * v / blade_radius  # rad/s
            rpm = omega * 60.0 / (2.0 * np.pi)
            rpm_values.append(rpm)
        plt.plot(wind_speeds_range, rpm_values, label=f"TSR={tsr}")
    
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Generator RPM")
    plt.title(f"RPM vs Wind Speed (R={blade_radius}m)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()