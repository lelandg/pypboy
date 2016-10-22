import logging
import sys
import traceback

#import RPi.gpio as gpio
import time

#import pypboy.gpio as gpio
from pypboy import gpio
#from pypboy import config

gpio.setmode(gpio._GPIO.BCM)

LOGFILENAME = './testGpioMultiplexer.log'
DEBUG = True

gpio.DEBUG = DEBUG

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

def my_log(msg):
    logging.info(msg)
    print msg


def run_tests():
    # Setup 8 channel input on muxed gpio pins 41-47, inclusive.
    ports = []
    # 1st, for a multiplexed rotary switch.
    for j in range(40, 45):
        x = gpio.gpiox(extended=j, actual=3, mode=gpio.IN, pud=gpio.PUD_DOWN)
        ports.append(x)

    # Then for the 3 "LED switches", the switches first...
    for j in range(80,83):
        x = gpio.gpiox(extended=j, actual=15, mode=gpio.IN, pud=gpio.PUD_DOWN)
        ports.append(x)

    # ... and then LEDs.
    for j in range(83,86):
        x = gpio.gpiox(extended=j, actual=14)
        ports.append(x)

    chsel1 = [4, 17, 27]
    chsel2 = [22, 23, -1]

    g = gpio.gpio(chsel1 = chsel1, chsel2 = chsel2, ports=ports)

    # Initialize a few things for our loop below:
    sw1 = -1  # For display via log/print
    sw2 = -1  # For display via log/print
    led = -1  # LED portion of the LED-Button that was last pressed. (This will be the one that's lit up.)

    # Display a banner corresponding to the output of print statement below.
    s = "{title1}{title2}".format(title1='Active Switch 40-48'.ljust(40),
                                            title2='Active Switch 80-83'.ljust(40))
    logging.info(s)

    while 1:
        for portnum in range(40, 45):  # Check the "switch inputs" that are really a rotary switch
            if gpio.HIGH == g.input(portnum):
                sw1 = 40 - portnum  # Calculate number for display, only
                if DEBUG: my_log('Active switch on extended GPIO port# {0}'.format(portnum))
                break

        for portnum in range(80, 83):  # Check "LED-Buttons"
            if g.input(portnum):
                sw2 = 80 - portnum  # Calculate number for display, only
                if DEBUG: my_log('Active switch on extended GPIO port# {0}'.format(portnum))
                if led != -1:
                    g.output(led, 0)  # Turn off the LED that went with previous switch
                led = portnum + 3
                g.output(led, 1)  # Turn on LED that goes with this switch
                break

        # Display the current values
        s1 = str(sw1).ljust(40)
        s2 = str(sw2).ljust(40)
        my_log("{0}{1}".format(s1, s2))

        # And then sleep on it a while... :)
        time.sleep(0.5)


def main(argc, argv):
    error = None
    try:
        setup_log(LOGFILENAME, trace=DEBUG)
        run_tests()
    except:
        logging.error(traceback.format_exc())  # Log the error
        error = traceback.format_exc()  # and format to log it (if possible)
    finally:
        gpio.cleanup()
        if error:
            logging.error(error)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
