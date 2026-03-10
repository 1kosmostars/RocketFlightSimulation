# Student Rocket Flight Simulator

## Project Description

A software package for numerical modeling of student rocket trajectories, accounting for aerodynamics, gravity, and propulsion system operation. The project is designed for educational purposes and development of student rockets.

The current version implements a simplified flight model with 3 degrees of freedom (translational motion in a plane), allowing quick estimation of primary flight characteristics: apogee, range, and velocity.

## Current Version Capabilities (v1.0)

### Physical Model
- Ballistic trajectory with gravity
- Exponential atmosphere model (air density vs altitude)
- Aerodynamic drag (quadratic velocity dependence)
- Rocket mass variation during propellant consumption
- Constant thrust during engine burn time

### Functionality
- Configurable rocket parameters (geometry, mass, engine)
- Selectable launch angle
- Numerical integration of equations of motion (odeint method)
- Automatic landing detection
- Output of primary flight characteristics

### Visualization
- Flight trajectory in space
- Altitude vs time graph
- Velocity vs time graph
- Velocity component graphs (vertical and horizontal)

## Requirements

### Software
- Python 3.8 or higher
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Matplotlib >= 3.3.0

### Installing Dependencies

```bash
pip install numpy scipy matplotlib
```

## Usage

### Basic Launch

```python
# Create rocket with default parameters
rocket = Rocket()

# Initialize simulator
sim = RocketSimulator(rocket)

# Run simulation (vertical launch)
results = sim.simulate(launch_angle=90, duration=60)

# Print results
print_summary(results)

# Visualize
plot_results(results)
```

### Configuring Rocket Parameters

```python
rocket = Rocket()
rocket.diameter = 0.20        # 20 cm diameter
rocket.thrust = 2000.0        # 2000 N thrust
rocket.burn_time = 4.0        # 4 second burn
rocket.cd = 0.4               # Drag coefficient
```

### Angled Launch

```python
# Launch at 85 degrees
results = sim.simulate(launch_angle=85, duration=60)
```

## Project Structure

```
rocket-simulator/
├── rocket_sim.py          # Main simulator module
├── README.md              # Documentation
├── requirements.txt       # Project dependencies
└── examples/              # Usage examples
    └── basic_flight.py    # Basic example
```

## Theoretical Foundations

### Equations of Motion

First-order differential equation system:

```
dx/dt = vx
dy/dt = vy
dvx/dt = (Fx_thrust + Fx_drag) / m
dvy/dt = (Fy_thrust + Fy_drag) / m - g
```

### Aerodynamic Drag

```
F_drag = 0.5 * ρ * v² * Cd * A
```

where:
- ρ - air density
- v - rocket velocity
- Cd - drag coefficient
- A - reference area

### Atmosphere Model

```
ρ(h) = ρ₀ * exp(-h/H)
```

where:
- ρ₀ = 1.225 kg/m³ (sea level density)
- H = 8500 m (scale height)

## Development Roadmap

### Stage 2: Enhanced Physical Model (version 2.0)

**Priority: High**

#### Atmosphere
- Implementation of US Standard Atmosphere 1976
- Temperature and pressure accounting at different altitudes
- Speed of sound and Mach number calculation
- Drag coefficient variation with Mach number

#### Propulsion System
- Loading real thrust curves from files (.eng format)
- RASP engine file support
- Engine ignition delay
- Thrust instability modeling

#### Wind Loading
- Constant wind with specified direction
- Altitude-dependent wind profile
- Wind gusts (random perturbations)

#### Center of Mass Calculation
- Dynamic center of mass shift during propellant consumption
- Effect on flight stability

### Stage 3: 6 Degrees of Freedom (version 3.0)

**Priority: Medium**

#### Rotational Dynamics
- Implementation of quaternions or Euler angles
- Moment of inertia calculation (Ixx, Iyy, Izz)
- Euler equations for rotational motion
- Gyroscopic effects accounting

#### Aerodynamic Moments
- Center of pressure calculation
- Moment from center of mass and center of pressure misalignment
- Damping moments
- Fin influence

#### Stabilization
- Passive aerodynamic stabilization
- Barrowman stability criterion
- Stability margin analysis

#### Perturbations
- Engine thrust asymmetry
- Engine misalignment
- Manufacturing defects
- Landing accuracy impact

### Stage 4: Advanced Features (version 4.0)

**Priority: Medium**

#### Recovery System
- Parachute model (constant descent rate)
- Deployment at apogee or by timer
- Multi-stage system (drogue + main)
- Landing kinetic energy calculation

#### Monte Carlo Analysis
- Multiple simulations with parameter variation
- Statistical analysis of landing point dispersion
- Landing zone estimation (dispersion ellipse)
- Factor influence analysis on accuracy

#### Multi-stage Rockets
- Stage separation
- Inter-stage delay
- Separate stage trajectories after separation

#### Optimization
- Optimal launch angle search for maximum range
- Design optimization for target apogee
- Flight time minimization with constraints

### Stage 5: Active Control (version 5.0)

**Priority: Low**

#### Control Systems
- TVC (Thrust Vector Control)
- Canards
- Reaction Control System (RCS)

#### Control Algorithms
- PID controllers for stabilization
- Trajectory following control
- Guidance systems

#### Navigation
- GPS modeling
- Inertial navigation
- Kalman filter for state estimation

### Stage 6: Interface and Integration (version 6.0)

**Priority: Low**

#### User Interface
- GUI based on PyQt or Tkinter
- Visual rocket parameter editor
- Interactive scalable graphs

#### Visualization
- Real-time 3D flight animation
- Using VPython or Three.js
- Rocket orientation visualization in space
- Telemetry dashboard

#### Import/Export
- Configuration loading from OpenRocket
- Results export in various formats (CSV, JSON, HDF5)
- API for integration with other tools

#### Validation
- Automatic comparison with OpenRocket
- Test case suite
- Modeling accuracy metrics

## Known Limitations

### Current Version
- Simplified atmosphere model (does not account for temperature and pressure)
- Constant engine thrust (real thrust varies with time)
- No rotational motion
- Thrust always directed along velocity vector
- Wind not accounted for
- Simplified gravity model (constant)

### Applicability Range
- Altitudes up to 10 km
- Subsonic and transonic velocities (up to M = 2)
- Single-stage rockets
- Ballistic flight without active control

## Usage Examples

### Comparing Two Rockets

```python
rocket1 = Rocket()
rocket1.thrust = 1500

rocket2 = Rocket()
rocket2.thrust = 2000

sim1 = RocketSimulator(rocket1)
sim2 = RocketSimulator(rocket2)

results1 = sim1.simulate()
results2 = sim2.simulate()

# Compare on one graph
plt.plot(results1['time'], results1['altitude'], label='Rocket 1')
plt.plot(results2['time'], results2['altitude'], label='Rocket 2')
plt.legend()
plt.show()
```

### Launch Angle Optimization

```python
angles = range(70, 91, 5)
max_altitudes = []

for angle in angles:
    results = sim.simulate(launch_angle=angle)
    max_altitudes.append(np.max(results['altitude']))

optimal_angle = angles[np.argmax(max_altitudes)]
print(f"Optimal angle: {optimal_angle}°")
```

## Validation

To verify simulation correctness, it is recommended to:

1. Compare results with OpenRocket for identical configuration
2. Verify conservation laws (energy, momentum)
3. Test against known analytical solutions
4. Compare with experimental data from real launches

## Contributing

The project is open for improvements. Welcomed contributions:
- Bug fixes
- Implementation of new features from the roadmap
- Documentation improvements
- Adding examples
- Performance optimization

## Literature and Resources

### Books
- Sutton, George P. "Rocket Propulsion Elements"
- Stine, Harry. "Handbook of Model Rocketry"
- NASA SP-8066 "Space Vehicle Design Criteria"

### Online Resources
- OpenRocket - http://openrocket.info
- RASP Engine Database - http://nar.org/SandT/NARenglist.shtml
- NASA Beginner's Guide to Rockets - https://www.grc.nasa.gov/www/k-12/rocket/

### Academic Courses
- MIT 16.50 Introduction to Propulsion Systems
- Stanford AA284A Rocket Propulsion

## License

MIT License

## Authors

Student rocket flight modeling project

## Contact

For questions and suggestions, please create issues in the project repository.
