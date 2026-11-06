import numpy as np
from scipy.integrate import solve_ivp

from Atmosphere import Atmosphere


class RocketSimulator:

    def __init__(self, rocket, rail_length=3.0):
        """
        Initialize the simulator

        Parameters:
        ----------
        rocket : Rocket
            Rocket object to simulate
        rail_length : float
            Length of the launch rail in meters. While on the rail the rocket
            moves strictly along the launch direction.
        """
        self.rocket = rocket
        self.atm = Atmosphere()
        self.rail_length = rail_length
        self.launch_angle_rad = np.pi / 2

    def get_mass(self, t):
        """
        Calculates the current mass of the rocket accounting for propellant burnoff

        Parameters:
        ----------
        t : float
            Current time in seconds

        Returns:
        -----------
        mass : float
            Current mass in kg
        """
        # If propellant has already burned out
        if t >= self.rocket.burn_time:
            return self.rocket.dry_mass

        # Current mass = initial mass - burned propellant
        return self.rocket.total_mass - self.rocket.mass_flow_rate * t

    def get_thrust(self, t):
        """
        Returns engine thrust at time t

        Parameters:
        ----------
        t : float
            Current time in seconds

        Returns:
        -----------
        thrust : float
            Thrust in Newtons
        """
        if t < self.rocket.burn_time:
            return self.rocket.thrust
        return 0.0  # Engine off

    def derivatives(self, t, state):
        """
        KEY FUNCTION: computes derivatives for the ODE system

        This is the heart of the simulator! Physics laws are applied here.

        Parameters:
        ----------
        t : float
            Current time (s)
        state : array [x, y, vx, vy]
            x, y   - rocket coordinates (m)
            vx, vy - velocity components (m/s)

        Returns:
        -----------
        derivatives : array [dx/dt, dy/dt, dvx/dt, dvy/dt]
        """
        x, y, vx, vy = state

        # === GET CURRENT PARAMETERS ===
        m = self.get_mass(t)
        thrust = self.get_thrust(t)
        g = self.atm.gravity(y)
        rho = self.atm.density(max(y, 0.0))
        cd_a = self.rocket.cd * self.rocket.area

        v = np.hypot(vx, vy)

        # === ON THE LAUNCH RAIL ===
        # The rail holds the rocket on the launch line: only forces along the
        # rail matter, and the rail does not let the rocket slide backwards.
        if np.hypot(x, y) < self.rail_length:
            ux, uy = np.cos(self.launch_angle_rad), np.sin(self.launch_angle_rad)
            drag = 0.5 * rho * v ** 2 * cd_a
            a = (thrust - drag) / m - g * uy
            if v < 1e-9 and a < 0:
                a = 0.0  # Thrust not enough to lift off yet
            return [vx, vy, a * ux, a * uy]

        # === FREE FLIGHT ===
        # Drag: F_drag = 0.5 * ρ * v² * Cd * A, directed against velocity
        # Thrust: directed along velocity (gravity turn, no attitude model)
        if v > 1e-9:
            ux, uy = vx / v, vy / v
        else:
            ux, uy = 0.0, 1.0
        drag = 0.5 * rho * v ** 2 * cd_a

        # === NEWTON'S SECOND LAW: a = F/m ===
        ax = (thrust - drag) * ux / m
        ay = (thrust - drag) * uy / m - g

        return [vx, vy, ax, ay]

    def simulate(self, launch_angle=90, duration=None, n_points=1000):
        """
        Runs the flight simulation until landing (or until `duration` elapses)

        Parameters:
        ----------
        launch_angle : float
            Launch angle in degrees (90 = straight up)
        duration : float
            Maximum simulation time in seconds (defaults to rocket.sim_duration)
        n_points : int
            Number of output points

        Returns:
        -----------
        results : dict
            Dictionary with simulation results. 'landed' is False if the
            rocket was still in the air when the time limit was reached.
        """
        if not 0 < launch_angle <= 90:
            raise ValueError("launch_angle must be in (0, 90] degrees")
        if duration is None:
            duration = self.rocket.sim_duration

        print(f"Starting simulation (angle: {launch_angle}°)...")
        self.launch_angle_rad = np.radians(launch_angle)

        # Rocket starts at rest at the base of the rail
        initial_state = [0.0, 0.0, 0.0, 0.0]

        # Landing event: altitude crosses zero going down
        def hit_ground(t, state):
            return state[1]
        hit_ground.terminal = True
        hit_ground.direction = -1

        # Integrate burn and coast phases separately so the solver never
        # steps across the thrust/mass discontinuity at burnout.
        burn_end = min(self.rocket.burn_time, duration)
        phases = [(0.0, burn_end), (burn_end, duration)]

        segments = []  # (t_start, t_end, solution)
        landed = False
        state = initial_state
        for t0, t1 in phases:
            if t1 <= t0:
                continue
            sol = solve_ivp(self.derivatives, (t0, t1), state,
                            events=hit_ground, dense_output=True,
                            rtol=1e-8, atol=1e-6, max_step=0.5)
            if not sol.success:
                raise RuntimeError(f"Integration failed: {sol.message}")
            segments.append((t0, sol.t[-1], sol))
            state = sol.y[:, -1]
            if sol.status == 1:  # Terminated by landing event
                landed = True
                break

        # Sample n_points evenly over the actual flight time
        t = np.linspace(0.0, segments[-1][1], n_points)
        x, y, vx, vy = np.empty((4, n_points))
        for t0, t_end, sol in segments:
            mask = (t >= t0) & (t <= t_end)
            x[mask], y[mask], vx[mask], vy[mask] = sol.sol(t[mask])
        if landed:
            y[-1] = 0.0  # Exact ground contact
        y = np.maximum(y, 0.0)

        if landed:
            print("Simulation complete!")
        else:
            print(f"Warning: rocket did not land within {duration} s — "
                  "increase duration to see the full flight.")

        return {
            'time': t,
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'velocity': np.hypot(vx, vy),
            'altitude': y,
            'landed': landed,
        }
