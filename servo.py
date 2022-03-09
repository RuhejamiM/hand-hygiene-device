# Part: Servo

import RPi.GPIO as GPIO
import time
import sys

global pin
global servo

pin = 18

def setup_servo():
    print('setup servo')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin,50)

def start_servo():
    print('start servo')
    servo.start(0)
    duty = 0.05
    servo.ChangeDutyCycle(duty)

def stop_servo():
    print('stop servo')
    servo.stop()

setup_servo()

try:
    while True:
        time.sleep(1)
        start_servo()
        stop_servo()
      
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
