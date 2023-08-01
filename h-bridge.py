""""
This is used for testing now h-bridge and linear actuator function with various code.
"""

import board
import analogio
import time
from digitalio import DigitalInOut, Direction, Pull


# Define the GPIO pins for the L298N H-bridge and set to output
in1 = DigitalInOut(board.GP0)
in2 = DigitalInOut(board.GP1)
in1.switch_to_output()
in2.switch_to_output()

# Define the GPIO pins and directions for buttons.
button_open = DigitalInOut(board.GP2)
button_close = DigitalInOut(board.GP3)
button_light = DigitalInOut(board.GP4)
button_manual_override = DigitalInOut(board.GP6)
button_eStop = DigitalInOut(board.GP18)
button_open.direction = Direction.INPUT
button_close.direction = Direction.INPUT
button_light.direction = Direction.INPUT
button_manual_override.direction = Direction.INPUT
button_eStop.direction = Direction.INPUT

# Set internal pull-ups for buttons.
button_open.pull = Pull.UP
button_close.pull = Pull.UP
button_light.pull = Pull.UP
button_manual_override.pull = Pull.UP
button_eStop.pull = Pull.UP

# Actuator-related variables
actuator_running = False
actuator_stop_time = 0
actuator_run_time = 15  # Time in seconds the linear actuator needs for opening and closing the door


def actuator_open(duration):
    global actuator_running, actuator_stop_time
    actuator_stop_time = time.monotonic() + duration
    actuator_running = True
    in1.value = True
    in2.value = False


def actuator_close(duration):
    global actuator_running, actuator_stop_time
    actuator_stop_time = time.monotonic() + duration
    actuator_running = True
    in1.value = False
    in2.value = True


def actuator_stop():
    global actuator_running
    in1.value = False
    in2.value = False
    actuator_running = False


actuator_open(14)  # Boot with door open


while True:
    # Check for button presses and perform relevant actions

    # Check if the "Open" button is pressed
    if not button_open.value:  # Button is active LOW due to pull-up resistor
        print("Opening")
        actuator_open(actuator_run_time)

    # Check if the "Close" button is pressed
    if not button_close.value:  # Button is active LOW due to pull-up resistor
        print("Closing")
        actuator_close(actuator_run_time)

    # Check if the "Emergency Stop" button is pressed
    if not button_eStop.value:  # Button is active LOW due to pull-up resistor
        print("Stop")
        actuator_stop()

    # If the actuator is running and current time is greater or equal to the calculated stop time then execute code
    if actuator_running and time.monotonic() >= actuator_stop_time:
        actuator_running = False
        print("actuator Stopped")
        actuator_stop()
    print("Main Loop")

    time.sleep(1)