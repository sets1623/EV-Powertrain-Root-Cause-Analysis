class Vehicle:
    """
    Vehicle longitudinal dynamics model WITH inertia
    """

    def __init__(self,
                 mass=1500,
                 wheel_radius=0.3,
                 rolling_resistance_coeff=0.015,
                 drag_coeff=0.29,
                 frontal_area=2.2,
                 air_density=1.225):
        """
        mass                     : vehicle mass (kg)
        wheel_radius             : wheel radius (m)
        rolling_resistance_coeff : rolling resistance coefficient
        drag_coeff               : aerodynamic drag coefficient
        frontal_area             : frontal area (m^2)
        air_density              : air density (kg/m^3)
        """
        self.mass = mass
        self.wheel_radius = wheel_radius
        self.Crr = rolling_resistance_coeff
        self.Cd = drag_coeff
        self.A = frontal_area
        self.rho = air_density

        self.speed = 0.0  # vehicle speed (m/s)

    def step(self, drive_torque, dt):
        """
        Update vehicle speed using force balance

        drive_torque : torque applied at wheels (Nm)
        dt           : time step (s)
        """

        g = 9.81

        # Forces
        rolling_force = self.mass * g * self.Crr
        drag_force = 0.5 * self.rho * self.Cd * self.A * self.speed ** 2

        drive_force = drive_torque / self.wheel_radius

        # Net force
        net_force = drive_force - (rolling_force + drag_force)

        # Acceleration
        acceleration = net_force / self.mass

        # Speed update
        self.speed += acceleration * dt
        self.speed = max(0.0, self.speed)

        return self.speed

    def load_torque(self):
        """
        Load torque reflected to motor
        """

        g = 9.81
        rolling_force = self.mass * g * self.Crr
        drag_force = 0.5 * self.rho * self.Cd * self.A * self.speed ** 2

        total_force = rolling_force + drag_force
        return total_force * self.wheel_radius
