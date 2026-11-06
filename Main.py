import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Rocket import Rocket, PRESETS
from RocketSimulator import RocketSimulator


def plot_results(results):
    """Plots simulation result graphs"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Rocket Flight Simulation Results', fontsize=16)

    # Plot 1: Flight trajectory
    axes[0, 0].plot(results['x'], results['y'], 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Horizontal distance (m)', fontsize=12)
    axes[0, 0].set_ylabel('Altitude (m)', fontsize=12)
    axes[0, 0].set_title('Flight Trajectory', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim(bottom=0)

    # Plot 2: Altitude vs Time
    axes[0, 1].plot(results['time'], results['altitude'], 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Altitude (m)', fontsize=12)
    axes[0, 1].set_title('Altitude vs Time', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)

    # Mark the apogee
    max_alt_idx = np.argmax(results['altitude'])
    axes[0, 1].plot(results['time'][max_alt_idx], results['altitude'][max_alt_idx],
                    'ro', markersize=10, label='Apogee')
    axes[0, 1].legend()

    # Plot 3: Velocity vs Time
    axes[1, 0].plot(results['time'], results['velocity'], 'g-', linewidth=2)
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[1, 0].set_title('Velocity vs Time', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Velocity components
    axes[1, 1].plot(results['time'], results['vx'], 'b-', linewidth=2, label='Vx (horizontal)')
    axes[1, 1].plot(results['time'], results['vy'], 'r-', linewidth=2, label='Vy (vertical)')
    axes[1, 1].axhline(y=0, color='k', linestyle='--', alpha=0.5)
    axes[1, 1].set_xlabel('Time (s)', fontsize=12)
    axes[1, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[1, 1].set_title('Velocity Components', fontsize=14)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def print_summary(results):
    """Prints the main flight characteristics"""
    print("\n" + "=" * 60)
    print("           FLIGHT SIMULATION RESULTS")
    print("=" * 60)
    print(f"Maximum altitude (apogee):  {np.max(results['altitude']):.2f} m")
    print(f"Maximum velocity:           {np.max(results['velocity']):.2f} m/s")

    # Time to apogee
    apogee_time = results['time'][np.argmax(results['altitude'])]
    print(f"Time to apogee:             {apogee_time:.2f} s")

    if results['landed']:
        print(f"Total flight time:          {results['time'][-1]:.2f} s")
        print(f"Range:                      {results['x'][-1]:.2f} m")
        print(f"Landing velocity:           {results['velocity'][-1]:.2f} m/s")
    else:
        print(f"Rocket still in the air at  {results['time'][-1]:.2f} s "
              f"(altitude {results['y'][-1]:.2f} m)")
    print("=" * 60 + "\n")


def animate_flight(results):
    """Animates the rocket flight trajectory"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(results['x'].min() - 10, results['x'].max() + 10)
    ax.set_ylim(0, results['altitude'].max() * 1.1)
    ax.set_xlabel('Horizontal distance (m)')
    ax.set_ylabel('Altitude (m)')
    ax.set_title('Rocket Flight Animation')
    ax.grid(True, alpha=0.3)

    trail, = ax.plot([], [], 'b-', linewidth=1, alpha=0.4)
    rocket_dot, = ax.plot([], [], 'ro', markersize=10)

    def update(frame):
        trail.set_data(results['x'][:frame], results['y'][:frame])
        rocket_dot.set_data([results['x'][frame]], [results['y'][frame]])
        return trail, rocket_dot

    anim = FuncAnimation(fig, update, frames=len(results['time']), interval=20, blit=True)
    plt.show()


def select_preset():
    """Interactive preset selection menu"""
    print("\n" + "=" * 60)
    print("    ROCKET FLIGHT SIMULATOR v1.0")
    print("=" * 60)
    print("\nSelect a rocket preset:\n")
    for key, p in PRESETS.items():
        print(f"  [{key}] {p['name']:<20} — {p['description']}")
    print()

    while True:
        try:
            choice = int(input(f"Enter number (1–{len(PRESETS)}): "))
            if choice in PRESETS:
                return PRESETS[choice]
            print(f"Please enter a number between 1 and {len(PRESETS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_launch_angle(default=90.0):
    """Asks for the launch angle in degrees (Enter = default)"""
    while True:
        raw = input(f"Launch angle in degrees (0–90, Enter = {default:g}): ").strip()
        if not raw:
            return default
        try:
            angle = float(raw)
            if 0 < angle <= 90:
                return angle
            print("Angle must be greater than 0 and at most 90.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    preset = select_preset()
    launch_angle = select_launch_angle()

    # Create rocket
    print("\nStep 1: Creating rocket...")
    my_rocket = Rocket(preset)
    my_rocket.info()

    # Create simulator
    print("Step 2: Initializing simulator...")
    simulator = RocketSimulator(my_rocket)

    # Run simulation
    print("Step 3: Running simulation...")
    results = simulator.simulate(launch_angle=launch_angle, duration=my_rocket.sim_duration)

    # Analyze results
    print("\nStep 4: Analyzing results...")
    print_summary(results)

    # Plot graphs
    print("Step 5: Plotting graphs (close the window to continue)...\n")
    plot_results(results)

    # Animate flight
    print("Step 6: Animating flight (close the window to exit)...\n")
    animate_flight(results)

    print("Done!")
