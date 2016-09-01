# See GitHub history for authoring history. This file had no history when I (Leland Green) needed
# to fix all problems with the code *and* add support for multiplexers, all to build a more realistic
# Pip Boy! (It's all for my brother Noel!)
import pygame
import sys

import config
import os

# Init framebuffer/touchscreen environment variables
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

try:
    import pypboy.gpio as gpio
    import RPi.GPIO as GPIO
    gpio.setmode(gpio.BCM)
    config.GPIO_AVAILABLE = True
except Exception, e:
    print "*** GPIO UNAVAILABLE (%s)! ***" % e
    config.GPIO_AVAILABLE = False

from pypboy.core import Pypboy

print "config.GPIO_AVAILABLE = {GPIO_AVAILABLE}".format(GPIO_AVAILABLE = config.GPIO_AVAILABLE)

try:
    pygame.mixer.init(44100, -16, 2, 2048)
    config.SOUND_ENABLED = True
except:
    config.SOUND_ENABLED = False

print "config.SOUND_ENABLED = {SOUND_ENABLED}".format(SOUND_ENABLED = config.SOUND_ENABLED)

def main(argc, argv):
    boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)
    print "RUN"
    boy.run()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
