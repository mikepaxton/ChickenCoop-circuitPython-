# Chicken Coop Controller

## Features:
The purpose of this script is to control the chicken coop door and light using a Raspberry Pico and CircuitPython.
I'm using a L298N H-Bridge motor driver to control a linear actuator which opens and closes the coop door.
I'm using a photocell resistor to detect light levels outside the coop which then triggers the opening and closing of the door.

## How the chicken door should work:
Opens at daylight hours and closes and dark (photocell resistor).
If needed a way to manually open and close the coop door.
Install a manual override button (constant on switch)
When in manual mode can press open or close to keep the door in the desired state.

## 3D Printer Files:
I've included my 3D printer .stl files for both the 5mm photo cell and control panel.
The control panel is printed in two part for easy printing.  They are simply attached by inserting and securing
the buttons.  Coop Panel Door Insert - Part 2.stl is printed using two colors.  I printed the lettering in white as 
you can see in the photos.

The photocell holder allows you to insert a 5mm photocell into one end then attach wires and heatshrink them into place.
The holder itself is long enough to go through 3/8" plywood of the chicken coop siding.  You can use small screws 
and some silicon to secure it on the inside of siding.

## Additional Info:
I've included a couple photos to help visualize what the install looks like.  This is a working chicken coop so 
please excuse the cobwebs and mess.  You will probably notice three holes drilled into control panel door.
Those are from my previous setup which was using a Raspberry Pi 3B.  I plan on 3d printing a couple of wooden 
inserts to plug those holes.
The previous system worked great, but I had issues in the dead of winter.  The 100W solar panel couldn't keep the 
12v deep cycle battery charged enough to run the Raspberry Pi, just not enough sunlight in the winter.
You can find my previous setup on my GitHub page under StarClucks. It was written for the Raspberry Pi using Python 3.

I'm using a 12v to 5 volt DC converter to power the Raspberry Pico directly off of the battery.  I'm bypassing the 
solar controllers output connectors. I've had issues in the past using the outputs including the USB ports.
To the right of the Pico you will see a red and yellow wire.  This is the photocell holder attached to it.
You will also see some speaker wire coiled up on the left side.  When I was running with a Raspberry Pi 3b I had 
Airplay installed on it and could play music in the backyard through the speakers attached to the chicken coop.

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
* 1 GPIO wire 


* H-Bridge - 1 
* 1 Ground wire will not be in panel so has its own ground or tied to Relay. 
* 1 12v wire running tied to 12v circuit. 
* 2 wires running to linear actuator 
* 2 wires running to Pico GPIO 


* Photocell - 1
* 3.3v wire inside panel 
* 1 ground wire inside panel 
* 1 GPIO wire inside panel


Total number of wires running from inside panel to panel door: 6  -  5 GPIO wires and 1 ground wire

I'm using a length of CAT 6 Cable for the 6 strands of wire.  Makes for a clean install inside panel to door.

* Button function/Button color/Button Type/Wire Color/Physical Pin #

* Open  -  Green  -  momentary  -  Green Wire  -  #4
* Close  -  Green  -  momentary  -  Green White Wire -  #5
* Manual Override  -  Red  -  Constant  -  Orange Wire  -  #9
* Lights  -  White  -  Constant  -  Orange White Wire  -  #6


* LED  -  Blue Wire  - #21
* Ground - Brown Wire  - #3

Brown White & Blue White Wire not used.

###  TODO: Implement a hardware reset button incase the Pico ever locks up.  Pin # 30 (run) tied to ground via a momentary button will do the trick.
