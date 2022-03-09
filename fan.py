# Part: Fan

import RPi.GPIO as GPIO
import time
import sys

global pin

pin = 18

def setup_fan():
    print('setup fan')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)

def start_fan():
    print('start fan')
    GPIO.output(pin, True)

def stop_fan():
    print('stop fan')
    GPIO.output(pin, False)

setup_fan()

try:
    while True:
        time.sleep(1)
        start_fan()
        time.sleep(5)
        stop_fan()
        time.sleep(5)
      
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
