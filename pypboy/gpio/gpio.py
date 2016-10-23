"""
A GPIO abstraction class used to "add logical pins" to the physical GPIO structure.
By simply importing this class instead of RPi.GPIO (or GPIO), simply import from this class.
If your GPIO pin number is a "normal" GPIO number, the normal underlying routines will be called, completely
transparent to you.

Initially written to encapsulate  multiplexer functionality transparently. This module simulates an "extended GPIO" by
adding "extended pin numbers" using a simple scheme of binary packing. That is, since  the number 40 (the number of
physical GPIO pins) will fit into six bits, we use the other two bits of an eight-bit number to store a
"multiplexer number", which is actually an encoded address. A value of 1 will be the first multiplexer, 2 is the
second one, and so forth.

Written by Leland Green... (Boogieman/aBoogieman)
Contact me via Section9.space , on Google+ or Facebook.
"""
import types
import logging
import RPi.GPIO as _GPIO
from pypboy.gpio import multiplexer

BCM = _GPIO.BCM
BOARD = _GPIO.BOARD

_GPIO.setwarnings(False)

# chsel1 = [4, 17, 27]
# chsel2 = [22, 23, -1]

CHSELA1 = 4
CHSELB1 = 17
CHSELC1 = 27

CHSELA2 = 22
CHSELB2 = 23
CHSELC2 = -1    # Signifies not in use.

class gpiox:
    """
    "GPIO extender" class. Allows association of extended GPIO port (anything >= 40) to physical GPIO port,
    as well as specifying an input/output mode.

    Subclasses can add anything they need.
    """

    def __init__(self, extended, actual, mode=_GPIO.OUT, pud=_GPIO.PUD_OFF):
        """
        :param extended: An extended port number. The system expects >= 40, but this class does no validation.
        :param actual: The actual, physical GPIO port to use
        :param mode: One of _GPIO.IN or _GPIO.OUT
        """
        assert mode in [_GPIO.IN, _GPIO.OUT]
        self.extended = extended
        self.gpio = actual
        self.mode = mode
        self.pud = pud

    def __repr__(self):
        s1 = 'IN'
        if self.mode == 0:
            s1 = 'OUT'

        s2 = "PUD_OFF"
        if self.pud != _GPIO.PUD_OFF:
            if self.pud == _GPIO.PUD_UP:
                s2 = 'PUD_UP'
            if self.pud == _GPIO.PUD_DOWN:
                s2 = 'PUD_DOWN'

        return 'gpiox class: extended={0}, gpio={1}, mode={2}, pud={3}'.format(self.extended, self.gpio, s1, s2)

    def __eq__(self, other):
        if self.extended == other.extended and self.gpio == other.gpio and \
                        self.mode == other.mode and self.pud == other.pud:
            return True
        return False


class gpio(object):
    instance = None

    def __new__(cls, *args, **kwargs):  # __new__ always a classmethod
        if not gpio.instance:
            gpio.instance = gpio.__gpio(args, kwargs)
        return gpio.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    class __gpio:
        def __repr__(self):
            s = '__gpio class:'
            s += "chselA1 = {0}, chselB1 = {1}, chselC1 = {2}, chselA2 = {3}, chselB2 = {4}, chselC2 = {5}\r\n" \
                .format(self.chselA1, self.chselB1, self.chselC1, self.chselA2, self.chselB2, self.chselC2, )
            for j in range(0, len(self.ports)):
                x = self.ports[j]
                s += '{0}: {1}\r\n'.format(j, str(x))
            s += '<end instance>\r\n'
            return s

        def __init__(self, *args, **kwargs):
            """
            :param args:
            :param kwargs:
                The following keywords are recognized:

                Initialize multiplexers by passing a list of CHSEL GPIO pins...
                chsel1 - A list of chselA, chselB, <chselC> for first multiplexer
                chsel2 - A list of chselA, chselB, <chselC> for second multiplexer

                ... OR specify individual chselA1 - chselC2 (but don't do both).
                chselA1 - Channel select A GPIO pin
                chselB1 - Channel Select B GPIO pin
                chselC1 - Channel Select C GPIO pin

                chselA2 - Channel select A GPIO pin
                chselB2 - Channel Select B GPIO pin
                chselC2 - Channel Select C GPIO pin

                If you DO specify BOTH, then the chsel1 and chsel2 parameters will take precedence and the others
                will be ignored.
            """

            self.ports = {}
            # TODO: Refactor all of this so default initialization is pulled from a config file.
            # Defaults for multiplexer 1 -- We need the channel-select pins (named to correspond to datasheet),
            # and the GPIO port numbers along with corresponding "extended-GPIO" port numbers.
            self.chselA1 = CHSELA1
            self.chselB1 = CHSELB1
            self.chselC1 = CHSELC1

            # Defaults for multiplexer 2 -- for 4 channels (with or without dual) you only need 2 selectors, so...
            self.chselA2 = CHSELA2
            self.chselB2 = CHSELB2
            self.chselC2 = CHSELC2  # ... we set the last one to -1 which indicates it's not used.

            # This map contains the extended-GPIO port number as the key and the actual GPIO port used as value.

            if kwargs.has_key('chsel1'):
                self.chselA1 = kwargs['chsel1'][0]
                self.chselB1 = kwargs['chsel1'][1]
                self.chselC1 = kwargs['chsel1'][2]
            else:
                if kwargs.has_key('chselA1'):
                    self.chselA1 = kwargs['chselA1']
                if kwargs.has_key('chselB1'):
                    self.chselB1 = kwargs['chselB1']
                if kwargs.has_key('chselC1'):
                    self.chselC1 = kwargs['chselC1']

            if kwargs.has_key('chsel2'):
                self.chselA2 = kwargs['chsel2'][0]
                self.chselB2 = kwargs['chsel2'][1]
                self.chselC2 = kwargs['chsel2'][2]
            else:
                if kwargs.has_key('chselA2'):
                    self.chselA2 = kwargs['chselA2']
                if kwargs.has_key('chselB2'):
                    self.chselB2 = kwargs['chselB2']
                if kwargs.has_key('chselC2'):
                    self.chselC2 = kwargs['chselC2']

            if kwargs.has_key('ports'):
                self.ports = kwargs['ports']
            else:
                logging.debug('Using defaults for gpio class')
                # Set defaults for ports if not found in args.
                # 1st, for a multiplexed rotary switch.
                for j in range(40, 45):
                    x = gpiox(j, 3, _GPIO.IN, _GPIO.PUD_DOWN)
                    self.ports[j] = x

                # Then for the 3 "LED switches", switches first...
                for j in range(80, 83):
                    x = gpiox(j, 15, _GPIO.IN, _GPIO.PUD_DOWN)
                    self.ports[j] = x

                # ... and then LED's.
                for j in range(83, 86):
                    x = gpiox(j, 14)
                    self.ports[j] = x

            if -1 != self.chselC1:
                n = 8
            else:
                n = 4

            self.ports1 = {}
            self.ports2 = {}
            for key, value in self.ports.iteritems():
                if 40 <= key <= 79:
                    self.ports1[key] = value
                else:
                    if 80 <= key <= 120:
                        self.ports2[key] = value

            self.muxer1 = multiplexer.multiplexer(self.chselA1, self.chselB1, self.chselC1, ports=self.ports1)
            if -1 != self.chselC1:
                n = 8
            else:
                n = 4
            logging.debug('muxer1 = {0}'.format(self.muxer1))

            if -1 != self.chselC1:
                n = 8
            else:
                n = 4
            self.muxer2 = multiplexer.multiplexer(self.chselA2, self.chselB2, self.chselC2, ports=self.ports2)
            logging.debug('muxer2 = {0}'.format(self.muxer2))

            self.setupall()

        def setup(self, channel, direction, pull_up_down=_GPIO.PUD_OFF, initial=None):
            """
            Set up a GPIO channel or list of channels with a direction and (optional) pull/up down control.
            Note that if channel is a list, all of direction, pull_up_down and initial must be lists (or tuples)
            **of the same length**. Failure to meet this requirement will throw an exception and this class
            will not be usable for your entire session! This can possibly cause some confusing errors later if you
            trap and ignore the exception from this method (setup).

            :param channel: Either board pin number or BCM number depending on which mode is set.
                                Can be either an int, tuple or list of ints.

                                Note that if this param is a list or tuple type, then all of
                                direction, pull_up_down and initial may also be list or tuple types!

                                This means you can quite effectively initialize ALL your GPIO I/O in
                                ONE setup() call (i.e., this function, NOT the RPi.GPIO!) This class
                                handles it all for you.
            :type channel: Int, Tuple or List

            :param direction:       IN or OUT
            :type direction: Int, Tuple or List

            :param pull_up_down:    PUD_OFF (default), PUD_UP or PUD_DOWN
            :type pull_up_down: Int, Tuple or List

            :param initial:         Initial value(s) for an output channel
            :type initial: Int, Tuple or List

            """
            logging.debug('gpio.setup(channel={0}, direction={1}, pull_up_down={2}, initial={3})'.
                          format(channel, direction, pull_up_down, initial))
            if type(channel) in [types.ListType, types.TupleType]:
                for n in range(0, len(channel)):
                    ch = channel[n]
                    d = None
                    d = direction
                    if type(direction) in (types.TupleType, types.ListType):
                        d = direction[n]

                    pud = pull_up_down
                    if type(pull_up_down) in (types.TupleType, types.ListType):
                        pud = pull_up_down[n]

                    init = initial
                    if type(initial) in (types.TupleType, types.ListType):
                        init = initial[n]

                    self._setup(ch, d, pud, init)
            else:
                if type(channel) in [types.DictionaryType, types.DictType]:
                    # Assume we have values for gpiox as key=extended port, val = [gpioport, <_GPIO.IN or _GPIO.OUT>]
                    for key, val in types.iteritems():
                        if isinstance(val, gpiox):
                            self.ports[key] = val
                        else:
                            if isinstance(val, types.ListType):
                                x = gpiox(key, val[0], val[1], val[3])
                                self.ports[key] = x
                    self._setup(x.gpio, x.mode, x.pud)
                else:
                    self._setup(channel, direction, pull_up_down, initial)

        def _setup(self, channel, direction, pull_up_down=_GPIO.PUD_OFF, initial=None):
            """
            Set up a GPIO channel or list of channels with a direction and (optional) pull/up down control.

            trap and ignore the exception from this method (setup).

            channel        - Either board pin number or BCM number depending on which mode is set.
                                Must be int type or exception will be thrown.
            direction      - IN or OUT
            [pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN
            [initial]      - **UNSUPPORTED** Not supported in all cases!!
                             TODO: Add support for this parameter in all cases (specifically when using a dict of
                             gpiox instances).
                             Initial value for an output channel.
            """
            logging.debug('gpio._setup(channel={0}, direction={1}, pull_up_down={2}, initial={3})'.
                          format(channel, direction, pull_up_down, initial))
            channel = self._setchan(channel)
            logging.debug('gpio._setup() adjusted channel = {0}'.format(channel))

            if initial and _GPIO.OUT == direction:
                _GPIO.setup(channel, direction, pull_up_down, initial)
            else:
                _GPIO.setup(channel, direction, pull_up_down)

        def _setchan(self, channel):
            logging.debug('gpio._setchan({0})'.format(channel))
            if type(channel) != types.IntType:
                raise Exception("Type of channel must be int for gpio._setup()! "
                                "This class is now unusable in your current python session!")

            if channel >= 40:
                # A special channel number for a multiplexer
                muxer = self.muxer1

                if channel >= 80:
                    logging.debug('Using muxer2')
                    muxer = self.muxer2
                else:
                    logging.debug('Using muxer1')

                nch = channel

                return muxer.setchan(nch)
            else:
                return channel

        def output(self, channel, value):
            logging.debug('__gpio.output({0})'.format(channel))
            pin = self._setchan(channel)
            if pin:
                return _GPIO.output(pin, value)
            else:
                return _GPIO.output(channel, value)

        def input(self, channel):
            logging.debug('__gpio.input({0})'.format(channel))
            pin = self._setchan(channel)
            logging.debug('pin = {p}'.format(p=pin))
            if pin:
                return _GPIO.input(pin)
            else:
                return _GPIO.input(channel)

        def setupall(self):
            logging.debug('__gpio.setupall()')
            for key in self.ports.keys():
                x = self.ports[key]
                logging.debug('... GPIO.setup(port={0}, mode={1})'.format(x.gpio, x.mode))
                _GPIO.setup(x.gpio, x.mode)


def setup(channel, direction, pull_up_down=_GPIO.PUD_OFF, initial=None):
    logging.debug('setup(channel={0}, direction={1}, pull_up_down={2}, initial={3})'.
                  format(channel, direction, pull_up_down, initial))
    g = gpio()
    logging.debug('g = {0}'.format(g))
    if initial:
        return g.setup(channel, direction, pull_up_down, initial)
    else:
        return g.setup(channel, direction, pull_up_down)


def output(channel, value):
    g = gpio()
    # logging.debug('g = {0}'.format(g))
    return g.output(channel, value)


def input(channel):
    g = gpio()
    # logging.debug('g = {0}'.format(g))
    return g.input(channel)


def setmode(mode):
    _GPIO.setmode(mode)


def getmode():
    return _GPIO.getmode()
