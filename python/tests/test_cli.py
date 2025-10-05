import subprocess
import json
import pathlib

def test_cli_design(tmp_path):
    out = tmp_path / "summary.json"
    cmd = [
        "wind-turbine",
        "design",
        "--wattage", "100",
        "--air-density", "1.225",
        "--wind-speed", "8",
        "--radius", "0.6",
        "--blades", "4",
        "--output", str(out)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert out.exists()
    data = json.loads(out.read_text())
    assert "rotor_area" in data
    # Note: target_wattage is not in output, it's an input parameter