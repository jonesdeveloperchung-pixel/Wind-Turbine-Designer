import sys
import json
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFileDialog, QMessageBox)
from . import wind_calc

class DesignApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wind Turbine Designer")
        layout = QVBoxLayout()

        self.wattage = QLineEdit("50")
        self.air_density = QLineEdit("1.225")
        self.wind_speed = QLineEdit("6")
        self.radius = QLineEdit("0.5")
        self.blades = QLineEdit("3")

        for label, widget in [("Target Wattage:", self.wattage),
                              ("Air Density:", self.air_density),
                              ("Wind Speed (m/s):", self.wind_speed),
                              ("Blade Radius (m):", self.radius),
                              ("Number of Blades:", self.blades)]:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        btn = QPushButton("Generate")
        btn.clicked.connect(self.generate)
        layout.addWidget(btn)

        self.setLayout(layout)

    def generate(self):
        try:
            cfg = wind_calc.PyTurbineConfig(
                target_wattage=float(self.wattage.text()),
                env=wind_calc.Env(air_density=float(self.air_density.text()),
                                  wind_speed=float(self.wind_speed.text())),
                constraints=wind_calc.Constraints(
                    blade_radius=float(self.radius.text()),
                    num_blades=int(self.blades.text()),
                    generator_type=wind_calc.GeneratorType.Brushless
                )
            )
            solver = wind_calc.PySolver(cfg)
            summary = solver.design_summary()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        # Pretty print
        msg = json.dumps(summary, indent=2)
        QMessageBox.information(self, "Design Summary", msg)

def run_gui():
    app = QApplication(sys.argv)
    w = DesignApp()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()