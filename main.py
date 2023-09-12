"""
main.py
Author: Mike Paxton
Creation Date: 08/01/2023
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

08/01/23 - Mike Paxton
Modified code to not tie up the while loop with the (actuator_run_time) which waited for actuator to open or close
before continuing to execute additional code. This prevented any button clicks or other code from executing until the
actuator_run_time expired.
The new code uses a variable (actuator_running) to check the status of the actuator.  If an event triggers the actuator
to run, an actuator_stop_time is calculated based on current time.(monotonic) plus duration(actuator_run_time).
The while loop then checks the current time.monotonic() of each consecutive iteration of the loop and if greater than
actuator_stop_time executes actuator_stop(). This allows the while loop to continue without pause.
Implemented the e-stop (emergency stop) button in case a chicken tries to dart through while door is closing.
"""

import board
import analogio
import time
from digitalio import DigitalInOut, Direction, Pull

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
light_relay = DigitalInOut(board.GP17)
light_relay.direction = Direction.OUTPUT

# Define photocell
photocell = analogio.AnalogIn(board.A0)

# Actuator-related variables
actuator_running = False
actuator_stop_time = 0
actuator_run_time = 15  # Time in seconds the linear actuator needs for opening and closing the door

# Photocell low & high value used for determining when the coop door should open/close.
# Note:  You must adjust these values for your specific installation location.  I 3D printed a photocell holder
# and drilled a hole in the side of the coop so the sensor takes readings from outside.
evening_threshold = 6000
day_threshold = 20000


def actuator_open(duration):
    """
    Open the chicken coop door by controlling the linear actuator.

    Parameters:
    - duration (float): The duration in seconds for which the actuator should run to open the door.

    This function sets the linear actuator to open the chicken coop door for the specified duration.
    It updates the global variables 'actuator_running' and 'actuator_stop_time' to track the
    actuator's status and stop time. Additionally, it controls the motor driver to open the door.

    Note:
    - 'actuator_running' is used to monitor the state of the actuator operation.
    - 'actuator_stop_time' is the time at which the actuator should automatically stop.

    """
    global actuator_running, actuator_stop_time

    # Calculate the time at which the actuator should stop
    actuator_stop_time = time.monotonic() + duration

    # Set 'actuator_running' to True to indicate that the actuator is in operation
    actuator_running = True

    # Control the motor driver to open the door
    in1.value = True
    in2.value = False


def actuator_close(duration):
    """
    Close the chicken coop door by controlling the linear actuator.

    Parameters:
    - duration (float): The duration in seconds for which the actuator should run to close the door.

    This function sets the linear actuator to close the chicken coop door for the specified duration.
    It updates the global variables 'actuator_running' and 'actuator_stop_time' to track the
    actuator's status and stop time. Additionally, it controls the motor driver to close the door.

    Note:
    - 'actuator_running' is used to monitor the state of the actuator operation.
    - 'actuator_stop_time' is the time at which the actuator should automatically stop.

    """
    global actuator_running, actuator_stop_time

    # Calculate the time at which the actuator should stop
    actuator_stop_time = time.monotonic() + duration

    # Set 'actuator_running' to True to indicate that the actuator is in operation
    actuator_running = True

    # Control the motor driver to close the door
    in1.value = False
    in2.value = True


def actuator_stop():
    """
    Stop the operation of the chicken coop door's linear actuator.

    This function stops the operation of the linear actuator responsible for opening and closing
    the chicken coop door. It sets the global variable 'actuator_running' to False to indicate
    that the actuator is no longer in operation. Additionally, it ensures that the motor driver
    is set to a neutral state, causing the door to stop moving.

    Note:
    - 'actuator_running' is used to monitor the state of the actuator operation.

    """
    global actuator_running

    # Set 'actuator_running' to False which indicates that the actuator is no longer in operation
    actuator_running = False

    # Ensure that the motor driver is set to a neutral state, stopping the door from moving
    in1.value = False
    in2.value = False


# On boot open door
actuator_open(actuator_run_time)
# We've opened door, set door_open to True for photocell value checking portion of code
door_open = True


while True:
    """
    Main loop for controlling the chicken coop door and light.

    This loop continuously monitors various buttons, including the "Open," "Close," "Emergency Stop," "Light," 
    and "Manual Override" buttons. Depending on button presses and light conditions, it controls the operation 
    of the chicken coop door and interior light.

    The loop consists of several sections:

    1. Button Press Handling:
       - Checks if the "Open," "Close," and "Emergency Stop" buttons are pressed and executes corresponding actions.

    2. Actuator Running Check:
       - Monitors the state of the actuator (door movement) and stops it when the set duration is reached.

    3. Coop Light Relay Control:
       - Controls the interior coop light based on the status of the "Light" button.

    4. Manual Override and Photocell Check:
       - Checks if the "Manual Override" button is pressed. If so, it enables manual override mode.
       - If manual override is not active, it reads the photocell value to determine light conditions.
       - Based on light conditions and the door's current state, it decides whether to open or close the door.

    5. Debug Output:
       - Provides debugging information, including door status, to the REPL.

    6. Delay:
       - Introduces a small delay for button debouncing and smoother button handling.

    """
    # Beginning of open, close and e-stop button code section
    # Check if the "Open" button was pressed
    if not button_open.value:  # Button is active LOW due to pull-up resistor
        print("Opening")
        time.sleep(1)
        actuator_open(actuator_run_time)
        door_open = True

    # Check if the "Close" button is pressed
    if not button_close.value:  # Button is active LOW due to pull-up resistor
        print("Closing")
        time.sleep(1)
        actuator_close(actuator_run_time)
        door_open = False

    # Check if the "Emergency Stop" button is pressed
    if not button_eStop.value:  # Button is active LOW due to pull-up resistor
        print("E Stop")
        actuator_stop()
    # End of open, close and e-stop code section

    # Beginning of actuator running check section of code
    # If the actuator is running and current time is greater than the calculated stop time then execute code
    if actuator_running and time.monotonic() > actuator_stop_time:
        print("actuator Stopped")
        actuator_stop()
    # End of actuator running check code section

    # Beginning of coop light relay code section
    if not button_light.value:  # Button is active LOW due to pull-up resistor
        light_relay.value = True
        print("Light On")
    else:
        light_relay.value = False
        print("Light Off")
    # End of coop light relay code section

    # Beginning of Manual override and photocell value checking code section.
    if not button_manualOverride.value:  # Check if manual override button is pressed (active LOW due to pull-up resistor)
        led_manualOverride.value = True  # Button is pressed enable manual override mode and turn on LED indicator
        print("In Manual Override")
    else:
        # Manual override button not pressed, get value from photocell
        print(photocell.value)
        led_manualOverride.value = False  # Turn off manual override LED

        if door_open:  # Check if the door is open
            if photocell.value < evening_threshold:  # Check if it's dark enough to close the door
                door_open = False  # Set door status to closed
                actuator_close(actuator_run_time)  # Close the door as it's dark enough

        else:  # Door is closed
            if photocell.value > day_threshold:  # Check if it's light enough to open the door
                door_open = True  # Set door status to open
                actuator_open(actuator_run_time)  # Open the door as it's light enough

    # End of manual override and photocell value checking code section

    time.sleep(0.1)  # Delay for debounce and smoother button handling

    # Send door status to REPL, this is just for debug purposes.
    if door_open:
        print("Door Open")
    else:
        print("Door Closed")

    time.sleep(1)
