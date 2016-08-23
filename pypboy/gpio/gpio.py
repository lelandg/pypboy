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
import types

import RPi.GPIO as GPIO

import pypboy.gpio.multiplexer as multiplexer


class gpio(GPIO):
    # Defaults for multiplexer 1
    chselA1 = 4
    chselB1 = 17
    chselC1 = 27

    # Defaults for multiplexer 2
    chselA2 = 22
    chselB2 = 23
    chselC2 = -1

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
            The following keywords are recognized:
            chsel1 - A list of chselA, chselB, <chselC> for first multiplexer
            chsel2 - A list of chselA, chselB, <chselC> for second multiplexer

            chselA1 - Channel select A GPIO pin
            chselB1 - Channel Select B GPIO pin
            chselC1 - Channel Select C GPIO pin

            chselA2 - Channel select A GPIO pin
            chselB2 - Channel Select B GPIO pin
            chselC2 - Channel Select C GPIO pin

        """
        super(gpio, self).__init__(*args, **kwargs)
        if kwargs.has_key('chsel1'):
            self.chselA1 = kwargs['chsel1'][0]
            self.chselB1 = kwargs['chsel1'][1]
            self.chselC1 = kwargs['chsel1'][2]

        if kwargs.has_key('chselA1'):
            self.chselA1 = kwargs['chselA1']
        if kwargs.has_key('chselB1'):
            self.chselB1 = kwargs['chselB1']
        if kwargs.has_key('chselC1'):
            self.chselC1 = kwargs['chselC1']

        self.muxer1 = multiplexer.multiplexer(self.chselA1, self.chselB1, self.chselC1)

        if kwargs.has_key('chsel2'):
            self.chselA2 = kwargs['chsel2'][0]
            self.chselB2 = kwargs['chsel2'][1]
            self.chselC2 = kwargs['chsel2'][2]

        if kwargs.has_key('chselA2'):
            self.chselA2 = kwargs['chselA2']
        if kwargs.has_key('chselB2'):
            self.chselB2 = kwargs['chselB2']
        if kwargs.has_key('chselC2'):
            self.chselC2 = kwargs['chselC2']

        self.muxer2 = multiplexer.multiplexer(self.chselA2, self.chselB2, self.chselC2)

    def setup(self, channel, direction, pull_up_down=GPIO.PUD_OFF, initial=()):
        """
        Set up a GPIO channel or list of channels with a direction and (optional) pull/up down control.
        Note that if channel is a list, all of direction, pull_up_down and initial must be lists (or tuples)
        **of the same length**. Failure to meet this requirement will throw an exception and this class
        will not be usable for your entire session! This can possibly cause some confusing errors later if you
        trap and ignore the exception from this method (setup).

        channel        - Either board pin number or BCM number depending on which mode is set.
                            Can be either an int, or a list of them!
        direction      - IN or OUT
        [pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN
        [initial]      - Initial value for an output channel
        """
        if type(channel) == types.ListType or type(channel) == types.TupleType:
            for n in range(0, len(channel)):
                ch = channel[n]
                d = direction[n]
                pud = pull_up_down[n]
                init = initial[n]
                self._setup(ch, direction, pud, init)
        else:
            self._setup(channel, direction, pull_up_down, initial)

    def _setup(self, channel, direction, pull_up_down=GPIO.PUD_OFF, initial=0):
        """
        Set up a GPIO channel or list of channels with a direction and (optional) pull/up down control.

        trap and ignore the exception from this method (setup).

        channel        - Either board pin number or BCM number depending on which mode is set.
                            Must be int type or exception will be thrown.
        direction      - IN or OUT
        [pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN
        [initial]      - Initial value for an output channel
        """
        self._setchan(channel)

        super(gpio, self).setup(channel, direction, pull_up_down, initial)

    def _setchan(self, channel):
        if type(channel) != types.IntType:
            raise Exception("Type of channel must be int for gpio._setup()! "
                            "This class is now unusable in your current python session!")
        if channel >= 40:
            # A special channel number for a multiplexer
            muxer = self.muxer1
            if channel > 80:
                muxer = self.muxer2

            nch = channel
            while nch >= 40:
                nch -= 40
            muxer.setchan(nch)
            return muxer.GPIOPort[nch]
        else:
            return channel

    def output(self, channel, value):
        if channel >= 40:
            channel = self._setchan(channel)

        super(gpio, self).output(channel, value)

    def input(self, channel):
        if channel >= 40:
            channel = self._setchan(channel)

        return super(gpio, self).input(channel)
