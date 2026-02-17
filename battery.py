class Battery:
    """
    Thevenin equivalent battery model for EV powertrain simulation
    """

    def __init__(self,
                 capacity_ah=60,
                 nominal_voltage=360,
                 internal_resistance=0.08):
        """
        capacity_ah        : Battery capacity in Ah
        nominal_voltage    : Nominal battery voltage (V)
        internal_resistance: Internal resistance (Ohm)
        """
        self.capacity_coulomb = capacity_ah * 3600
        self.nominal_voltage = nominal_voltage
        self.internal_resistance = internal_resistance

        self.soc = 1.0  # State of Charge (1 = 100%)

    def open_circuit_voltage(self):
        """
        Simple SOC-dependent OCV model
        """
        return self.nominal_voltage * (0.9 + 0.1 * self.soc)

    def step(self, current, dt):
        """
        Update battery state for one time step

        current : Battery current (A)
        dt      : Time step (s)
        """
        terminal_voltage = (
            self.open_circuit_voltage()
            - current * self.internal_resistance
        )

        # SOC update
        self.soc -= (current * dt) / self.capacity_coulomb
        self.soc = max(0.0, min(1.0, self.soc))

        return terminal_voltage
