import warnings

import numpy as np

G0 = 9.80665  # Standard gravity used in the Isp definition, m/s²

# Propellant masses are consistent with thrust, burn time and Isp:
#   propellant_mass ≈ thrust * burn_time / (isp * G0)
PRESETS = {
    1: {
        "name": "Student Rocket",
        "description": "Small amateur rocket, low thrust",
        "diameter": 0.1, "length": 1.2,
        "dry_mass": 8.0, "propellant_mass": 1.27,
        "cd": 0.45, "thrust": 400.0, "burn_time": 5.0, "isp": 160.0,
        "sim_duration": 120,
    },
    2: {
        "name": "Sport Rocket",
        "description": "Mid-size high-power rocket",
        "diameter": 0.15, "length": 2.0,
        "dry_mass": 40.0, "propellant_mass": 8.39,
        "cd": 0.35, "thrust": 1800.0, "burn_time": 8.0, "isp": 175.0,
        "sim_duration": 180,
    },
    3: {
        "name": "Heavy Rocket",
        "description": "Large rocket, high thrust, slow acceleration",
        "diameter": 0.3, "length": 2.5,
        "dry_mass": 100.0, "propellant_mass": 17.0,
        "cd": 0.4, "thrust": 3000.0, "burn_time": 10.0, "isp": 180.0,
        "sim_duration": 180,
    },
    4: {
        "name": "Racing Dart",
        "description": "Ultralight dart, minimal drag, extreme acceleration",
        "diameter": 0.05, "length": 0.8,
        "dry_mass": 3.0, "propellant_mass": 0.51,
        "cd": 0.2, "thrust": 250.0, "burn_time": 3.0, "isp": 150.0,
        "sim_duration": 120,
    },
}


class Rocket:
    def __init__(self, preset: dict = None):
        p = preset or PRESETS[1]

        # === GEOMETRY ===
        self.diameter = p["diameter"]
        self.length = p["length"]

        # === MASSES ===
        self.dry_mass = p["dry_mass"]
        self.propellant_mass = p["propellant_mass"]

        # === AERODYNAMICS ===
        self.cd = p["cd"]

        # === ENGINE ===
        self.thrust = p["thrust"]
        self.burn_time = p["burn_time"]
        self.isp = p["isp"]

        self.preset_name = p["name"]
        self.sim_duration = p["sim_duration"]  # Max simulation time, s

        self.check_engine_consistency()

    # Derived values are properties so they stay correct
    # when parameters are changed after creation.
    @property
    def area(self):
        """Cross-sectional (reference) area, m²"""
        return np.pi * (self.diameter / 2) ** 2

    @property
    def total_mass(self):
        """Lift-off mass, kg"""
        return self.dry_mass + self.propellant_mass

    @property
    def mass_flow_rate(self):
        """Propellant consumption rate, kg/s"""
        return self.propellant_mass / self.burn_time

    def check_engine_consistency(self, tolerance=0.1):
        """Warn if propellant mass does not match thrust * burn_time / (Isp * g0)"""
        expected = self.thrust * self.burn_time / (self.isp * G0)
        if abs(self.propellant_mass - expected) > tolerance * expected:
            warnings.warn(
                f"{self.preset_name}: propellant mass {self.propellant_mass:.2f} kg "
                f"does not match thrust/Isp/burn time (expected ≈ {expected:.2f} kg)"
            )

    def info(self):
        """Print rocket parameters"""
        print(f"\n=== ROCKET PARAMETERS: {self.preset_name} ===")
        print(f"Diameter:       {self.diameter} m")
        print(f"Length:         {self.length} m")
        print(f"Total mass:     {self.total_mass:.2f} kg")
        print(f"Thrust:         {self.thrust} N")
        print(f"Burn time:      {self.burn_time} s")
        print(f"Isp:            {self.isp} s")
        print(f"Thrust/Weight:  {self.thrust / (self.total_mass * G0):.2f}")
        print("=" * (28 + len(self.preset_name)) + "\n")
