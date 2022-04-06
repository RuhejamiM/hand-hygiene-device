import RPi.GPIO as GPIO
import time
import sys

def setup_captouch():
 GPIO.setmode(GPIO.BCM)

 global out0
 global out1
 global out2
 global out3
 global out4

 out0 = 26 # output 0 is BCM26
 out1 = 19 # output 1 is BCM19
 out2 = 13 # output 2 is BCM13
 out3 = 6 # output 3 is BCM6
 out4 = 5 # output 4 is BCM5

 GPIO.setup(out0, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # configure resistor on pin as pulldown
 GPIO.setup(out1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 GPIO.setup(out2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 GPIO.setup(out3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 GPIO.setup(out4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def notify_user(pin):
 print("Pin", pin, "has been pressed.")

def detect_captouch():
 GPIO.add_event_detect(out0, GPIO.FALLING, callback = notify_user, bouncetime = 200) # add bouncetime to prevent false alarm
 GPIO.add_event_detect(out1, GPIO.FALLING, callback = notify_user, bouncetime = 200)
 GPIO.add_event_detect(out2, GPIO.FALLING, callback = notify_user, bouncetime = 200)
 GPIO.add_event_detect(out3, GPIO.FALLING, callback = notify_user, bouncetime = 200)
 GPIO.add_event_detect(out4, GPIO.FALLING, callback = notify_user, bouncetime = 200)

setup_captouch()
detect_captouch()

try:
 while True:
  time.sleep(0.01)
except KeyboardInterrupt:
 GPIO.cleanup()
 sys.exit()