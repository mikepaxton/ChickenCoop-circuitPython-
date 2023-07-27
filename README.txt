
The purpose of this script is to control the chicken coop door and light using a Raspberry Pico and CircuitPython.
I'm using a L298N H-Bridge motor driver to control a Linear Actuator which opens and closes the coop door.
I'm using a Photocell Resistor to detect light levels outside the coop which then triggers the opening and closing of the door.

How the chicken door should work:
Opens at daylight hours and closes and dark (photo sensor).
Can press the open button to open the door at any time.  Door should remain open.
Can press the close button to keep the door open at any time.  Door should remain closed
Do I need a manual override to keep door in a certain position.
Manual Override of the photo sensor.

I've included my 3D files for both the 5mm photo cell and control panel.
The control panel is printed in two part for easy printing.  They are simply attached by inserting and securing
the buttons.  Coop Panel Door Insert - Part 2.stl is printed using two colors.  I printed the lettering in white as you can see in the photos.

The photocell holder allows you to insert a 5mm photocell into one end then attach wires and heatshrink them into place.
The holder itself is long enough to go through 3/8" plywood of the chicken coop siding.  You can use small screws and some silicon to secure it on the inside of siding.

I've included a couple photos to help visualize what the install looks like.  This is a working chicken coop so please
excuse the cobwebs and mess.  You will probably notice three holes drilled into control panel door.  Those are from my previous setup which was using a Raspberry Pi 3B.  I plan on 3d printing a couple of wooden inserts to plug those holes.
The previous system worked great but I had issues in the dead of winter.  The 100W solar panel couldn't keep the 12v deep cycle battery charged enough to run the Raspberry Pi, just not enough sunlight in the winter.
You can find my previous setup on my github page under StarClucks. It was written for the Raspberry Pi using Python 3.

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
  I'm using a length of CAT 5 Cable for the 6 strands of wire.  Might make for a clean install from inside panel to door.

Button function/color/Button Type/Wire Color/Physical Pin #

Open  -  Green  -  momentary  -  Green Wire  -  #4
Close  -  Green  -  momentary  -  Green White Wire -  #5
Manual Override  -  Red  -  Constant  -  Orange Wire  -  #9
Lights  -  White  -  Constant  -  Orange White Wire  -  #6

LED  -  Blue Wire  - #21
Ground - Brown Wire  - #3

Brown White & Blue White Wire not used.

