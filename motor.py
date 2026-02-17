class Motor:
    """
    Electric motor model (PMSM/BLDC - system level)
    """

    def __init__(self,
                 torque_constant=0.5,
                 efficiency=0.92):
        """
        torque_constant : Nm/A
        efficiency      : motor efficiency (0 to 1)
        """
        self.torque_constant = torque_constant
        self.efficiency = efficiency
        self.speed = 0.0  # rad/s

    def electrical_to_mechanical(self, ac_power, load_torque, dt):
        """
        Convert electrical power to mechanical output

        ac_power   : electrical power from inverter (W)
        load_torque: mechanical load torque (Nm)
        dt         : time step (s)
        """

        # Available mechanical power after losses
        mech_power = ac_power * self.efficiency

        # Avoid division by zero
        if self.speed < 1e-3:
            self.speed = 1.0

        # Produced torque
        motor_torque = mech_power / self.speed

        # Net torque
        net_torque = motor_torque - load_torque

        # Speed update WITH DAMPING (this stabilizes system)
        damping = 0.1 * self.speed
        self.speed += (net_torque - damping) * dt

        # Speed cannot be negative
        self.speed = max(0.0, self.speed)

        return motor_torque, self.speed
