"""
A multiplexer encapsulation class for the Raspberry Pi.

Written by Leland Green... (Boogieman/aBoogieman)
Contact me via Section9.space , on Google+ or Facebook.

This class is concerned only with the Channel Select pins on the multiplexer. You initialize it by passing the
two or three pins you'll use (for 8-channel and 16 channel, respectively) as channel select pins (A, B and optionally C).

Then the multiplexer.setchan() method lets you set a channel number, 0 through NChannels.

***Important***: This class does not persist any data. However, it *does* change the affected GPIO ports!
(I.e., sets the mode: it changes modes on each port during setchan() calls, as needed.)
"""
import logging
import types

import RPi.GPIO as GPIO

# Constants
__version__ = "0.0.1"
__author__ = "Leland Green..."


class multiplexer:
    def __init__(self, chsela, chselb, chselc=-1, ports={}, setup=True):
        """
        :param chsela: GPIO pin number (BCM) for bit 0 of channel select A.
        :param chselb: GPIO pin number (BCM) for bit 0 of channel select B.
        :param chselc: GPIO pin number (BCM) for bit 0 of channel select C (if 8-channel or greater, zero otherwise).
        :param chvalmap: A map of channel numbers to channel direction. Channel numbers must be either ints or strings
                            that can be converted to ints (in base 10 format).
        :param ports: A map of gpiox instances, keyed on extended GPIO port #.
        :type ports: Dictionary

        :param setup: When True, each port will be initialized with corresponding gpioaction
        :type setup: bool
        """
        logging.debug('multiplexer.__init__(chsela={0}, chselb={1}, chselc={2}, ports={3}, setup={4}'.
                      format(chsela, chselb, chselc, ports, setup))
        GPIO.setwarnings(False)  # This is needed to allow "multiple I/O ports" on the same physical GPIO pin.
        self.chsela = chsela
        self.chselb = chselb
        self.chselc = chselc
        GPIO.setup(self.chsela, GPIO.OUT)
        GPIO.setup(self.chselb, GPIO.OUT)
        if self.chselc >= 0:
            GPIO.setup(self.chselc, GPIO.OUT)
        self.ports = ports

        unique_gpio = {}
        for key in self.ports.keys():
            x = self.ports[key]
            if not unique_gpio.has_key(x.gpio):
                unique_gpio[x.gpio] = [x, ]
            else:
                x1 = unique_gpio[x.gpio]
                x1.append(x)
                unique_gpio[x.gpio] = x1

            # Todo: Optimize so that setup is called *only* when it is different than what was previously called.
            logging.debug('calling GPIO.setup(port={0}, mode={1})'.format(x.gpio, x.mode))
            # x will be gpiox instance
            GPIO.setup(x.gpio, x.mode)

        logging.debug('unique_gpio = {0}'.format(unique_gpio))
        self.multimode = False
        # Now check unique_gpio go see if any of the modes for a given port are all the same or not.
        # If any of them are different, we'll need to call GPIO.setup() on them **EVERY time they're accessed**:
        # Otherwise, we can set the mode once and forget it! (We'd like that, but sometimes you just can't do it.)
        for key in unique_gpio.keys():
            ax = unique_gpio[key]
            x1 = ax[0]
            for x in ax[1:]:
                if x1.mode != x.mode:
                    self.multimode = True
        logging.debug('multiplexer._multimode = {0}'.format(self.multimode))

    def setchan(self, chan):
        """
        :param chan: Zero-based channel number to set as active. Must be within the range of valid channels for
          this instance! If you initialize an 8-channel and try to write to a 16-channel, you will crash.
        """
        assert types.IntType == type(chan)
        if chan & 0x01:
            n1 = 1
        else:
            n1 = 0

        if chan & 0x02:
            n2 = 1
        else:
            n2 = 0

        if chan & 0x04:
            n3 = 1
        else:
            n3 = 0

        if not self.ports.has_key(chan):
            # Typically this only happens during class initialization, and always it's harmless to skip in this case.
            return None

        logging.debug('multiplexer.setchan(): n1={n1}, n2={n2}, n3={n3}, chan={chan}, chsela={chsela}, chselb={chselb} chselc={chselc}'.
                      format(n1=n1, n2=n2, n3=n3, chan=chan, chsela=self.chsela, chselb=self.chselb, chselc=self.chselc))
        GPIO.output(self.chsela, n1)
        GPIO.output(self.chselb, n2)
        if self.chselc >= 0:
            GPIO.output(self.chselc, n3)

        if self.multimode:
            x = self.ports[chan]
            logging.debug('multimode: x = {0}'.format(x))
            GPIO.setup(x.gpio, x.mode)

    def __repr__(self):
        return 'chsela = {chsela}, chselb = {chselb}, chselc = {chselc}, ports = {ports}'. \
            format(chsela=self.chsela, chselb=self.chselb, chselc=self.chselc,
                   ports=self.ports)
