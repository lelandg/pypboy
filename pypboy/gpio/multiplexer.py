"""
A multiplexer encapsulation class for the Raspberry Pi.

Written by Leland Green... (Boogieman/aBoogieman)
Contact me via Section9.space , on Google+ or Facebook.

This class is concerned only with the Channel Select pins on the multiplexer. You initialize it by passing the
two or three pins you'll use (for 8-channel and 16 channel, respectively) as channel select pins (A, B and optionally C).

Then the multiplexer.setchan() method lets you set a channel number, 0 through NChannels.
"""
import types

import RPi.GPIO

# Constants
__version__ = "0.0.1"
__author__ = "Leland Green..."

class multiplexer:

    def __init__(self, chsela, chselb, chselc=-1, gpioport=(), gpioaction=(), multimode=True):
        """
        :param chsela: GPIO pin number (BCM) for bit 0 of channel select A.
        :param chselb: GPIO pin number (BCM) for bit 0 of channel select B.
        :param chselc: GPIO pin number (BCM) for bit 0 of channel select C (if 8-channel or greater, zero otherwise).
        :param chvalmap: A map of channel numbers to channel direction. Channel numbers must be either ints or strings
                            that can be converted to ints (in base 10 format).
        :param gpioport: A list or tuple containing actual GPIO port numbers to use for I/O from this instance.
        :param gpioaction: A list or tuple containing actual GPIO actions to set on each gpioport.
        :param multimode: When True, each time setchan() is called, it will set the GPIO mode. You should set this
                            to False when you have devices connected which should not be reinitialized on each
                            channel change.
                            Default = True.
        :type gpioport: List or Tuple of actual GPIO Ports this will operate on. Items should be of type int.
        :type gpioaction: List or Tuple of matching actions, one for each port. Items should be of
            type RPi.GPIO.IN or RPi.GPIO.OUT
        :type multimode: bool
        """
        self.chsela = chsela
        self.chselb = chselb
        self.chselc = chselc
        RPi.GPIO.setup(self.chsela, RPi.GPIO.OUT)
        RPi.GPIO.setup(self.chselb, RPi.GPIO.OUT)
        if self.chselc >= 0:
            RPi.GPIO.setup(self.chselc, RPi.GPIO.OUT)
        self.GPIOPort = tuple(gpioport)
        self.GPIOAction = tuple(gpioaction)
        self._multimode = multimode

    def setchan(self, chan):
        """
        :param chan: Zero-based channel number to set as active. Must be within the range of valid channels for
          this instance! If you initialize an 8-channel and try to write to a 16-channel, you will crash.
        """
        assert type(chan) == types.IntType
        if chan & 0x01: n1 = 1
        else: n1 = 0

        if chan & 0x02: n2 = 1
        else: n2 = 0

        if chan & 0x04: n3 = 1
        else: n3 = 0

        RPi.GPIO.output(self.chsela, n1)
        RPi.GPIO.output(self.chselb, n2)
        if self.chselc >= 0:
            RPi.GPIO.output(self.chselc, n3)

        if self._multimode:
            RPi.GPIO.setup(self.GPIOPort[chan], self.GPIOAction[chan])
