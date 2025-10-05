#!/usr/bin/env python3
"""
Build script for the wind turbine project.
Compiles Rust library and sets up Python package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and handle errors"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def build_rust():
    """Build the Rust library"""
    print("Building Rust library...")
    rust_dir = Path("rust")
    
    if not rust_dir.exists():
        print("Error: rust directory not found")
        return False
    
    # Build in release mode
    if not run_command(["cargo", "build", "--release"], cwd=rust_dir):
        return False
    
    # Find the built library
    target_dir = rust_dir / "target" / "release"
    
    # Look for the library file (different extensions on different platforms)
    lib_patterns = ["wind_calc.dll", "libwind_calc.so", "libwind_calc.dylib"]
    lib_file = None
    
    for pattern in lib_patterns:
        potential_lib = target_dir / pattern
        if potential_lib.exists():
            lib_file = potential_lib
            break
    
    if not lib_file:
        print("Error: Could not find built library")
        return False
    
    # Copy to Python package
    python_pkg_dir = Path("python") / "wind_turbine"
    if not python_pkg_dir.exists():
        python_pkg_dir.mkdir(parents=True)
    
    # Copy with the correct name for Python import
    dest_name = "wind_calc.pyd" if sys.platform == "win32" else lib_file.name
    dest_path = python_pkg_dir / dest_name
    
    print(f"Copying {lib_file} to {dest_path}")
    shutil.copy2(lib_file, dest_path)
    
    return True

def install_python_package():
    """Install the Python package in development mode"""
    print("Installing Python package...")
    python_dir = Path("python")
    
    if not python_dir.exists():
        print("Error: python directory not found")
        return False
    
    return run_command([sys.executable, "-m", "pip", "install", "-e", "."], cwd=python_dir)

def run_tests():
    """Run tests"""
    print("Running Rust tests...")
    if not run_command(["cargo", "test"], cwd="rust"):
        return False
    
    print("Running Python tests...")
    return run_command([sys.executable, "-m", "pytest", "tests/"], cwd="python")

def main():
    """Main build function"""
    print("Wind Turbine Designer Build Script")
    print("=" * 40)
    
    # Change to project root
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Build steps
    steps = [
        ("Building Rust library", build_rust),
        ("Installing Python package", install_python_package),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"Failed at step: {step_name}")
            return 1
        print(f"✓ {step_name} completed")
    
    print("\n" + "=" * 40)
    print("Build completed successfully!")
    print("\nYou can now run:")
    print("  wind-turbine design --wattage 50 --radius 0.5")
    print("  wind-turbine-gui")
    
    # Optionally run tests
    if "--test" in sys.argv:
        print("\nRunning tests...")
        if run_tests():
            print("✓ All tests passed")
        else:
            print("✗ Some tests failed")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())