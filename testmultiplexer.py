#!/usr/bin/python
# Script to test the functionality I need from the CD405xB CMOS Single 8-Channel Analog Multiplexer/Demultiplexer.
# Hardware & tech docs here: http://www.ti.com/product/CD4051B?dcmp=dsproject&hqs=pf
# See http://www.ti.com/lit/ds/symlink/cd4051b.pdf for example of datasheet

# Wire the following CD405 to these GPIO pins:
# chsela=4, chselb=17, chselc=27
# Wire the COM pin to GPIO 1

import logging
import traceback
import types
import RPi.GPIO as gpio
import time

import sys

gpio.setmode(gpio.BCM)

LOGFILENAME = './testmultiplexer.log'
DEBUG = True
DATAPIN = 3 # or I2C SCL

CHSELA = 4
CHSELB = 17
CHSELC = 27

def setup_log_colors():
    logging.addLevelName(logging.DEBUG, '\033[1;37m%s\033[1;0m' % logging.getLevelName(logging.DEBUG))
    logging.addLevelName(logging.INFO, '\033[1;36m%s\033[1;0m' % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.WARNING, '\033[1;31m%s\033[1;0m' % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, '\033[1;41m%s\033[1;0m' % logging.getLevelName(logging.ERROR))


def setup_log(log, trace):
    # if log is None:
    setup_log_colors()
    fmt = "%(asctime)s.%(msecs)03d %(levelname)s: %(message)s"
    datefmt = "%H:%M:%S"
    if trace:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(filename=log, level=level, format=fmt, datefmt=datefmt)


def log_handler(level, msg):
    method = getattr(logging, level)
    method(msg)


def setchan(chan=1, chsela=CHSELA, chselb=CHSELB, chselc=CHSELC):
    """
    :param chan: Zero-based channel number to set as active. Must be within the range of valid channels for
      this instance! If you initialize an 8-channel and try to write to a 16-channel, you will crash.
    """
    assert types.IntType == type(chan)
    # I'm sure this "bit-wise" logic is working. This is only one way to do this, of course. (and below)
    # if DEBUG: logging.debug('setchan(chan = {c}, chsela = {a}, chselb = {b}, chselc = {cc}'.format(c=chan, a=chsela, b=chselb, cc=chselc))
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
    #if DEBUG: logging.debug('n1 = {n1}, n2 = {n2}, n3 = {n3}'.format(n1=n1, n2=n2, n3=n3))

    gpio.output(chsela, n1)
    gpio.output(chselb, n2)
    if chselc >= 0:
        gpio.output(chselc, n3)

def mylog(msg, *args, **kwargs):
    print msg
    if args or kwargs:
        logging.info(msg.format('args = {a}, kwargs = {k}'), a=args, k=kwargs)
    else:
        logging.info(msg)

def run_tests():
    while 1:
        for j in range(0, 5):
            setchan(j)
            r = gpio.input(DATAPIN)
            s = '{j} = {r}'.format(j=j, r=r)
            mylog(s)

        mylog("\r\n")
        time.sleep(0.5)


def setup_multiplexer(chsela=CHSELA, chselb=CHSELB, chselc=CHSELC):
    gpio.setup(chselb, gpio.OUT)
    gpio.setup(chsela, gpio.OUT)
    if chselc != -1:
        gpio.setup(chselc, gpio.OUT)


def main(argc, argv):
    error = None
    try:
        setup_log(LOGFILENAME, trace=DEBUG)
        setup_multiplexer()
        gpio.setup(DATAPIN, gpio.IN)
        # for j in range(0, 7):
        #     setchan(j)
        #     gpio.setup(DATAPIN, gpio.IN)
        run_tests()
    except:
        #logging.error(traceback.format_exc())  # Log the error
        error = traceback.format_exc()  # and format to log it (if possible)
    finally:
        gpio.cleanup()
        if error:
            logging.error(error)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
