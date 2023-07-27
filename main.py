"""
main.py
Author: Mike Paxton
Creation Date: 07/20/2023
CircuitPython Version 8.2

The purpose of this script is to control the chicken coop door and light using a Raspberry Pico and CircuitPython.
I'm using a L298N H-Bridge motor driver to control a Linear Actuator which opens and closes the coop door.
I'm using a Photocell Resistor to detect light levels outside the coop which then triggers the opening and closing
of the door.

Additionally, I'm also using a pair of buttons to manually open or close the door in conjunction with a manual
override button.  This was added so the photocell could be overriden in order to clean the coop and have the door remain
closed.
Added an LED to indicate if Manual Override Mode is in effect.
A relay has been added along with a constant on switch which turns on a light inside the chicken coop.
NOTE:  The relay I'm using is triggered in a High state.
"""
import board
import analogio
import time
from digitalio import DigitalInOut, Direction, Pull

#  TODO:  Find a way to emulate the Python gpiozero's motor.forward() function so I don't have to use the time.sleep()
#   function which ties up the script for x (linActuatorRunTime) number of seconds.


# Define GPIO pins and directions for LED's
led_manualOverride = DigitalInOut(board.GP16)
led_manualOverride.direction = Direction.OUTPUT

# Define the GPIO pins for the L298N H-bridge and set to output
in1 = DigitalInOut(board.GP0)
in2 = DigitalInOut(board.GP1)
in1.switch_to_output()
in2.switch_to_output()

# Define the GPIO pins and directions for buttons.
button_open = DigitalInOut(board.GP2)
button_close = DigitalInOut(board.GP3)
button_light = DigitalInOut(board.GP4)
button_manualOverride = DigitalInOut(board.GP6)
button_eStop = DigitalInOut(board.GP18)
button_open.direction = Direction.INPUT
button_close.direction = Direction.INPUT
button_light.direction = Direction.INPUT
button_manualOverride.direction = Direction.INPUT
button_eStop.direction = Direction.INPUT

# Set internal pull-ups for buttons.
button_open.pull = Pull.UP
button_close.pull = Pull.UP
button_light.pull = Pull.UP
button_manualOverride.pull = Pull.UP
button_eStop.pull = Pull.UP

# Define GPIO pin and direction for relay
lightRelay = DigitalInOut(board.GP17)
lightRelay.direction = Direction.OUTPUT

# Define photocell
photocell = analogio.AnalogIn(board.A0)

# Time in seconds the linear actuator needs for opening and closing the door.
# Maybe add a second or two just to make sure it's completed its cycle.
linActuatorRunTime = 15

# Photocell low & high value used for determining when the coop door should open/close.
# Note:  You must adjust these values for your specific installation location.  I 3D printed a photocell holder
# and drilled a hole in the side of the coop so the sensor takes readings from outside.
eveningThreshold = 6000
dayThreshold = 20000


#  Open door routine
def actuator_open(duration):
    start_time = time.monotonic()
    while (time.monotonic() - start_time) < duration:
        in1.value = True
        in2.value = False


# Close door routine
def actuator_close(duration):
    start_time = time.monotonic()
    while (time.monotonic() - start_time) < duration:
        in1.value = False
        in2.value = True


# Stop the door.
def actuator_stop():
    in1.value = False
    in2.value = False


# On boot open door and set its status to True.
actuator_open(linActuatorRunTime)
doorStatusOpen = True


while True:
    if not button_open.value:
        actuator_open(linActuatorRunTime)  # Move the actuator backward for X number of seconds
        doorStatusOpen = True # Set doorStatus to Open
    elif not button_close.value:
        actuator_close(linActuatorRunTime)  # Move the actuator forward for X number of seconds
        doorStatusOpen = False # Set door status to closed
    else:
        actuator_stop()

    if not button_light.value:
        lightRelay.value = True
        print("Light On")
    else:
        lightRelay.value = False
        print("Light Off")

    # If the Manual Override button is pressed (turned on) then we can't let the photo sensor run.
    if not button_manualOverride.value:
        led_manualOverride.value = True
        print("In Manual Override")
    else:
        # Since the Manual Override button is not pressed we can let the photo sensor check for light conditions.
        print(photocell.value)
        led_manualOverride.value = False  # Turn on manual override LED
        if doorStatusOpen == True:
            if photocell.value < eveningThreshold:
                actuator_close(linActuatorRunTime)
                doorStatusOpen = False  # Set door status to closed

        # if we find the photocell has light we open the door.
        if doorStatusOpen == False:
            if photocell.value > dayThreshold:
                actuator_open(linActuatorRunTime)
                doorStatusOpen = True  # Set door status to open

    time.sleep(0.1)  # Delay for debounce and smoother button handling

    # Send door status to REPL
    if doorStatusOpen:
        print("Door Open")
    else:
        print("Door Closed")

    time.sleep(1)
