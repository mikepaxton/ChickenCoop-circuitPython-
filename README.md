# Coop Controller Software

The Chicken Coop Controller software is designed to automate the operation of a chicken coop door and interior light 
using a Raspberry Pico and CircuitPython. It offers a combination of automatic control based on light levels outside 
the coop, manual override capabilities, and a convenient interface for chicken coop management.

## Features:

* Automatic Coop Door Operation: The software uses a Raspberry Pico and an L298N H-Bridge motor driver to control a 
linear actuator that opens and closes the chicken coop door based on the ambient light levels. This is achieved 
using a photocell resistor to detect the outdoor light conditions.
* Manual Override: In situations where manual intervention is required, the system provides a Manual Override button. 
This button allows you to manually open or close the coop door and lock it in the desired state.
* Interior Coop Light Control: The software also includes functionality to control an interior light within the 
chicken coop. A relay is used to turn the light on or off, and this can be manually activated using a dedicated button.
* Emergency Stop: While the Emergency Stop (E-Stop) functionality is implemented in the code, it's important to note 
that it may not be physically wired to the control panel in your setup. The E-Stop button is designed to halt all 
operations in case of an emergency.

## How the Chicken Coop Door Works:

* The coop door automatically opens during daylight hours and closes at night based on the readings from the photocell 
resistor.
* In manual mode, you can press the "Open" or "Close" button to control the coop door's position. The Manual Override 
button and Constant On/Off button allow you to manually operate the door and interior light.

## Installation:

### Required Files on the Raspberry Pico:
/main.py
** Note: All necessary libraries are included in the CircuitPython.uf2 file, so there's no need to add libraries to 
the /lib folder.


## 3D Printer Files:

Included in this repository are 3D printer .stl files for the 5mm photocell holder and the control panel. The 
control panel consists of two parts for ease of printing, and they can be securely attached by inserting and 
securing the buttons. The "Coop Panel Door Insert - Part 2.stl" is printed using two colors, with the lettering 
typically printed in white.

The photocell holder is designed to accommodate a 5mm photocell, allowing you to attach wires and secure them in 
place with heat shrink tubing. It's long enough to pass through 3/8" plywood on the chicken coop's siding, and you 
can use small screws and silicone to secure it from the inside.

## Additional Info:
The provided photos in this repository offer a visual representation of the installation process. Please note that 
the coop in the images is a working chicken coop, so some mess and cobwebs are expected.

The setup includes a 12V to 5V DC converter to power the Raspberry Pico directly from the battery, bypassing the 
solar controller's output connectors. In the images, you'll also see a red and yellow wire connected to the 
photocell holder, along with coiled speaker wire. These were used for audio playback in the backyard when a 
Raspberry Pi 3B was previously installed.

## Basic Hardware List for Pico:
* 1 - Raspberry Pico
* 1 - L298 H-Bridge motor controller
* 1 - Single channel relay (Coop light relay)
* 1 - 12v to 5v  voltage regulator
* 2 - Momentary buttons (Open/Close buttons)
* 2 - Constant On/Off button (Manual Override and Coop Light)
* 2 - 100 ohm resistors (LED and photocell)
* 1 - Photocell resistor
* 2 - 20 pin single row headers (for mounting Pico to prototype board)  Makes for easley removing Pico and plugging it 
into my computer for upgrades of software.
* 1 - Prototype board solderable w/connected traces to Pico headers
* 5 - 3 pin terminal blocks
* 1 - 12v linear actuator.  I used a 12" stroke with a run speed of 20mm/s.
Various color 28 gauge wire for connecting small electronics hardware together. I used a small section of cat6 
ethernet cable to run from main board to the door panel for buttons.
Heavier gauge wire to run from h-bridge to actuator.

## Basic Hardware List for Solar Setup:
* 1 - 12v Deep cycle battery
* 1 - 20-30amp solar charger controller
* 1 - 100w solar panel
Enough heavier gauge wire to run from solar panel to controller to battery.

### NOTE: I've implemented an E-Stop (emergency stop) button in code but have not wired it up in my panel.  It's not pictured or mentioned here.


## Wiring to panel door:
* Buttons -  4: Manual Override, Light switch, open button and close button.
* 1 Ground wire/each But all can be tied to one ground wire going to panel
* 4 GPIO wires


* LED - 1   
* 1 Ground wired tied to common panel ground. 
* 1 GPIO wire and a resistor


### Current wiring inside panel itself:
* Relay - 1 
* 1 Ground wire will not be in panel so has its own ground or tied to H-Bridge. 
* 1 3.3v positive wire 
* 1 GPIO wire - GPIO #17


* H-Bridge - 1 
* 1 Ground wire will not be in panel so has its own ground or tied to Relay. 
* 1 12v wire running tied to 12v circuit. 
* 2 wires running to linear actuator 
* 2 wires running to Pico GPIO - GPIO #0 and #1


* Photocell - 1
* 3.3v wire inside panel 
* 1 ground wire inside panel 
* 1 GPIO wire inside panel - GPIO A0


Total number of wires running from inside panel to panel door: 6  -  5 GPIO wires and 1 ground wire

I'm using a length of CAT 6 Cable for the 6 strands of wire.  Makes for a clean install inside panel to door.

* Button function/Button color/Button Type/Wire Color/GPIO Pin #

* Open  -  Green  -  momentary  -  Green Wire  -  #2
* Close  -  Green  -  momentary  -  Green White Wire -  #3
* Manual Override  -  Red  -  Constant  -  Orange Wire  -  #6
* Lights  -  White  -  Constant  -  Orange White Wire  -  #4

### Additional Wiring:
* LED  -  Blue Wire  - #16
* Ground - Brown Wire

Brown White & Blue White Wire not used.

###  TODO: Implement a hardware reset button incase the Pico ever locks up.  Pin # 30 (run) tied to ground via a momentary button will do the trick.
