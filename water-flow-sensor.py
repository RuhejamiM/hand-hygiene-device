# Part: Water Flow Sensor

import RPi.GPIO as GPIO
import time
import sys

global pin
global count

pin = 4
count = 0

def setup_water_flow_sensor():
    global pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def flow_count(pin):
    global count
    if not GPIO.input(pin):
        count += 1
    print(count)

def detect_water_flow_sensor():
    GPIO.add_event_detect(pin, GPIO.FALLING, callback = flow_count)

setup_water_flow_sensor()
detect_water_flow_sensor()

try:
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()