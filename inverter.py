class Inverter:
    """
    Inverter model for EV powertrain simulation
    Converts DC power from battery to AC power for motor
    """

    def __init__(self, efficiency=0.95):
        """
        efficiency : inverter efficiency (0 to 1)
        """
        self.efficiency = efficiency

    def dc_to_ac_power(self, dc_voltage, dc_current):
        """
        Convert DC input to AC output power

        dc_voltage : Battery voltage (V)
        dc_current : Battery current (A)
        """
        dc_power = dc_voltage * dc_current
        ac_power = dc_power * self.efficiency

        return ac_power
