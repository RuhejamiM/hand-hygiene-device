"""
demo.py

Tests the libraries implemented in hand-hygiene.py
"""

import digitalio
import board
import time
import sys
import RPi.GPIO as GPIO
from hand_hygiene import LCD, FlowSensor, Bubbles, CapTouch, Speaker

GPIO.setmode(GPIO.BCM)

"""
Capacitive Touch Tests
"""
print("Now testing capacitive touch input")
c1 =  CapTouch()
c1.setup_captouch()
c1.detect_captouch()

print("All done. cleaning up now")

