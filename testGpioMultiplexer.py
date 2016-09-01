import logging
import traceback
import datetime
import os
import sys
import pypboy.gpio.gpio as gpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LOGFILENAME = './testGpioMultiplexer.log'
DEBUG = True


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


def run_tests():
    # Setup 8 channel input on muxed GPIO pins 41-47, inclusive.
    g = gpio.gpio()
    for ch in range(40, 48):
        g.setup(ch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Switches are input

    # Setup 8 channel input on muxed GPIO pins 80-82, inclusive.
    for ch in range(80, 83):
        g.setup(ch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Setup 3 channel output on muxed GPIO pins 83-85
    for ch in range(83, 86):
        g.setup(ch, GPIO.OUT)

    sw1 = -1  # For display via print
    sw2 = -1  # For display via print
    led = -1  # LED portion of the LED-Button that was last pressed. (This will be the one that's lit up.)

    # Display a banner corresponding to the output of print statement below.
    print "\r\n\r\n{title1}{title2}".format(title1='Active Switch 40-48'.ljust(40),
                                            title2='Active Switch 80-83'.ljust(40))
    while (1):
        # Display the current values
        s1 = str(sw1).ljust(40)
        s2 = str(sw2).ljust(40)
        print "\r%s%s" % (s1, s2)

        for ch in range(40, 48):  # Check the "switch inputs" that are really a rotary switch
            if g.input(ch):
                sw1 = 39 - ch  # Calculate number for display, only
                break

        for ch in range(80, 83):  # Check "LED-Buttons"
            if g.input(ch):
                sw2 = 79 - ch
                if led != -1:
                    g.output(led, 0)  # Turn off the LED that went with previous switch
                led = ch + 3
                g.output(led, 1)  # Turn on LED that goes with this switch
                break


def main(argc, argv):
    error = None
    try:
        setup_log(LOGFILENAME, trace=DEBUG)
        run_tests()
    except:
        traceback.print_exc()  # Print the error
        error = traceback.format_exc()  # and format to log it (if possible)
    finally:
        GPIO.cleanup()
        if error:
            logging.error(error)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
