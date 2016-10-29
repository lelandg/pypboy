"""
A GPIO abstraction class used to "add logical pins" to the physical GPIO structure.
Simply import this class instead of RPi.GPIO (or GPIO).
If your GPIO pin number is a "normal" GPIO number, the normal underlying routines will be called, completely
transparent to you.

Initially written to encapsulate  multiplexer functionality transparently. This module simulates an "extended GPIO" by
adding "extended pin numbers" using a simple scheme of binary packing. That is, since  the number 40 (the number of
physical GPIO pins) will fit into six bits, we use the other two bits of an eight-bit number to store a
"multiplexer number", which is actually an encoded address. A value of 1 will be the first multiplexer, 2 is the
second one, and so forth.

(See custom Eagle schematic in github project at https://github.com/lelandg/pypboy)

Written by Leland Green... (Boogieman/aBoogieman)
Contact me via Section9.space , on Google+ or Facebook.
"""

import RPi.GPIO as _GPIO

BCM = _GPIO.BCM

from RPi.GPIO import *

from gpio import *

#from pypboy.gpio import gpio
#from pypboy.gpio import multiplexer
