import board
import analogio
import time
from digitalio import DigitalInOut, Direction, Pull


# Define the GPIO pins for the L298N H-bridge and set to output
in1 = DigitalInOut(board.GP0)
in2 = DigitalInOut(board.GP1)
in1.switch_to_output()
in2.switch_to_output()

actuator_running = False
actuator_stop_time = 0


def actuator_open(duration):
    global actuator_running, actuator_stop_time

    actuator_running = True
    actuator_stop_time = time.monotonic() + duration

    in1.value = True
    in2.value = False

def actuator_stop():
    global actuator_running

    in1.value = False
    in2.value = False
    actuator_running = False

actuator_open(14)

while True:
    # Your additional code here
    # For example, check for button presses and perform relevant actions

    # Check if the actuator is running and if it's time to stop
    if actuator_running and time.monotonic() >= actuator_stop_time:
        actuator_stop()  # Stop the actuator