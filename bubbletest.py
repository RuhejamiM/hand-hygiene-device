import digitalio
import board
import time
import sys
import RPi.GPIO as GPIO
from hand_hygiene import LCD, FlowSensor, Bubbles, CapTouch, Speaker

GPIO.setmode(GPIO.BCM)

"""
Bubble System Tests
"""

print("Now testing bubble system. Press Ctrl + C to skip.")

b1 = Bubbles()

try:
        b1.setup_fan()
        b1.setup_servo()
        print("Running fan and servo for 5 seconds.")
        b1.start_fan()
        b1.start_servo()
        time.sleep(5)
        b1.stop_fan()
        b1.stop_servo()
except KeyboardInterrupt:
        print("Ctrl + C was pressed. Terminating bubble system test and continuing...")
