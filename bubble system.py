# Bubble System
# triggered by water flow sensor which starts the fan and servo

import RPi.GPIO as GPIO
import time
import sys

# water flow sensor

global pin_water_flow_sensor
global count

pin_water_flow_sensor = 4
count = 0

# servo

global pin_servo
global servo

pin_servo = 18

# fan

global pin_fan

pin_fan = 19

# water flow sensor

def setup_water_flow_sensor():
    print('setup water flow sensor')
    global pin_water_flow_sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_water_flow_sensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def flow_count(pin_water_flow_sensor):
    global count
    if not GPIO.input(pin_water_flow_sensor):
        count += 1
    print('turns: ' + str(count))

def detect_water_flow_sensor():
    print('water flow detected')
    GPIO.add_event_detect(pin_water_flow_sensor, GPIO.FALLING, callback = flow_count)

def reset_count():
    global count
    count = 0

# servo

def setup_servo():
    global servo
    print('setup servo')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_servo, GPIO.OUT)
    servo = GPIO.PWM(pin_servo,10)

def start_servo():
    global servo
    print('start servo')
    servo.start(0)
    duty = 0.05
    servo.ChangeDutyCycle(duty)

def stop_servo():
    global servo
    print('stop servo')
    servo.stop()

# fan

def setup_fan():
    print('setup fan')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_fan, GPIO.OUT)
    GPIO.setwarnings(False)

def start_fan():
    print('start fan')
    GPIO.output(pin_fan, True)

def stop_fan():
    print('stop fan')
    GPIO.output(pin_fan, False)

setup_water_flow_sensor()
detect_water_flow_sensor()
setup_servo()
setup_fan()

try:
    while True:
        if count == 0:
            start_servo()
            start_fan()
            time.sleep(20)
            stop_servo()
            stop_fan()
            reset_count()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
