README

The purpose of this script is to control the chicken coop door and light using a Raspberry Pico and CircuitPython.
I'm using a L298N H-Bridge motor driver to control a Linear Actuator which opens and closes the coop door.
I'm using a Photocell Resistor to detect light levels outside the coop which then triggers the opening and closing
of the door.

How the chicken door should work:
Opens at daylight hours and closes and dark (photo sensor).
Can press the open button to open the door at any time.  Door should remain open.
Can press the close button to keep the door open at any time.  Door should remain closed
Do I need a manual override to keep door in a certain position.
    Manual Override of the photo sensor.

 Current wiring to panel door.
 Buttons - 4: Manual Override, Light switch, open button and close button.
             1 Ground wire/each But all can be tied to one ground wire going to panel
             4 GPIO wires
 LED - 1     1 Ground wired tied to common panel ground.
            1 GPIO wire and a resistor

 Current wiring inside panel itself
 Relay - 1  1 Ground wire will not be in panel so has its own ground or tied to H-Bridge.
            1 3.3v positive wire
            1 GPIO wire
 H-Bridge - 1: 1 Ground wire will not be in panel so has its own ground or tied to Relay.
               1 12v wire running tied to 12v circuit.
               2 wires running to linear actuator
               2 wires running to Pico GPIO
  Photocell - 1 3.3v wire inside panel
              1 ground wire inside panel
              1 GPIO wire inside panel
``
  Total number of wires running from inside panel to panel door: 6  -  5 GPIO wires and 1 ground wire
  Lets use a section of CAT 5 Cable.  Might make for a clean install from inside panel to door.

Button function/color/Button Type/Wire Color/Physical Pin #

Open  -  Green  -  momentary  -  Green Wire  -  #4
Close  -  Green  -  momentary  -  Green White Wire -  #5
Manual Override  -  Red  -  Constant  -  Orange Wire  -  #9
Lights  -  White  -  Constant  -  Orange White Wire  -  #6

LED  -  Blue Wire  - #21
Ground - Brown Wire  - #3

Brown White & Blue White Wire not used.

