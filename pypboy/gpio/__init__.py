"""
A GPIO abstraction class used to "add logical pins" to the physical GPIO structure.
By simply importing this class instead of RPi.GPIO (or GPIO), you get free multiplexing for (currently) two
distinct multiplexers. (The code does not limit the number that you could add, it has only automated support
for two because that's the most I can use in my current project. Stay tuned, kids!)

If your GPIO pin number is a "normal" GPIO number, the normal underlying routines will be called, completely
transparent to you. If it

Initially written to encapsulate  multiplexer functionality transparently. This module simulates an "extended GPIO" by
adding "extended pin numbers" using a simple scheme of binary packing. That is, since  the number 40 (the number of
physical GPIO pins) will fit into six bits, we use the other two bits of an eight-bit number to store a
"multiplexer number", which is actually an encoded address. A value of 1 will be the first multiplexer, 2to is the
second one, and so forth.

Written by Leland Green... (Boogieman/aBoogieman)
Contact me via Section9.space , on Google+ or Facebook.
"""

import RPi.GPIO as _GPIO

BCM = _GPIO.BCM

from RPi.GPIO import *

from gpio import *

#from pypboy.gpio import gpio
#from pypboy.gpio import multiplexer
