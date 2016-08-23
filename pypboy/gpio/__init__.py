"""
A GPIO abstraction class used to "add logical pins" to the physical GPIO structure.
By simply importing this class instead of RPi.GPIO (or GPIO), simply import from this class.
If your GPIO pin number is a "normal" GPIO number, the normal underlying routines will be called, completely
transparent to you.

Initially written to encapsulate  multiplexer functionality transparently. This module simulates an "extended GPIO" by
adding "extended pin numbers" using a simple scheme of binary packing. That is, since  the number 40 (the number of
physical GPIO pins) will fit into six bits, we use the other two bits of an eight-bit number to store a
"multiplexer number", which is actually an encoded address. A value of 1 will be the first multiplexer, 2to is the
second one, and so forth.

Written by Leland Green... (Boogieman/aBoogieman)
Contact me via Section9.space , on Google+ or Facebook.
"""

# This is the preferred way to code __init__.py. By using __all__, you support "from pypboy.gpio import *" syntax.
__all__ = ['gpio', 'multiplexer']

