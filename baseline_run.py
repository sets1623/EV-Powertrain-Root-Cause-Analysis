import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.battery import Battery
from models.inverter import Inverter
from models.motor import Motor
from models.vehicle import Vehicle

# Create model objects
battery = Battery()
inverter = Inverter()
motor = Motor()
vehicle = Vehicle()

dt = 0.1               # time step (s)
current = 50           # battery current (A)

print("t | Batt_V | AC_Pwr | Motor_T | Speed")

for step in range(1, 201):

    # Battery
    battery_voltage = battery.step(current=current, dt=dt)

    # Inverter
    ac_power = inverter.dc_to_ac_power(battery_voltage, current)

    # Vehicle load torque (no arguments now)
    load_torque = vehicle.load_torque()

    # Motor
    motor_torque, motor_speed = motor.electrical_to_mechanical(
        ac_power=ac_power,
        load_torque=load_torque,
        dt=dt
    )

    # Vehicle dynamics WITH inertia
    vehicle_speed = vehicle.step(
        drive_torque=motor_torque,
        dt=dt
    )

    print(
        round(step * dt, 1),
        round(battery_voltage, 1),
        round(ac_power, 1),
        round(motor_torque, 1),
        round(vehicle_speed, 2)
    )
