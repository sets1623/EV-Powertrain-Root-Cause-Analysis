import sys
import os
import matplotlib.pyplot as plt

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

dt = 0.1
current = 50

time = []
speed = []
motor_torque_list = []

for step in range(1, 201):

    t = step * dt

    battery_voltage = battery.step(current=current, dt=dt)
    ac_power = inverter.dc_to_ac_power(battery_voltage, current)

    load_torque = vehicle.load_torque()

    motor_torque, motor_speed = motor.electrical_to_mechanical(
        ac_power=ac_power,
        load_torque=load_torque,
        dt=dt
    )

    vehicle_speed = vehicle.step(
        drive_torque=motor_torque,
        dt=dt
    )

    time.append(t)
    speed.append(vehicle_speed)
    motor_torque_list.append(motor_torque)

# -------- PLOTS --------

plt.figure()
plt.plot(time, speed)
plt.xlabel("Time (s)")
plt.ylabel("Vehicle Speed (m/s)")
plt.title("Vehicle Speed vs Time")
plt.grid(True)
plt.show()

plt.figure()
plt.plot(time, motor_torque_list)
plt.xlabel("Time (s)")
plt.ylabel("Motor Torque (Nm)")
plt.title("Motor Torque vs Time")
plt.grid(True)
plt.show()
