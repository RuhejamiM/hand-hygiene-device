import digitalio
import board
import time
import sys
import RPi.GPIO as GPIO
from hand_hygiene import LCD, FlowSensor, Bubbles, CapTouch, Speaker

GPIO.setmode(GPIO.BCM)

"""
Water Flow Sensor Tests
"""

f1 = FlowSensor()

try:
        f1.setup_water_flow_sensor()
        f1.detect_water_flow_sensor()

except KeyboardInterrupt:
        print("Ctrl + C was pressed. Terminating Water Flow sensor test...")

