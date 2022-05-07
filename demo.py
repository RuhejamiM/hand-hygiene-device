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

c1 =  CapTouch()
c1.setup_captouch()

"""
Speaker Tests
"""
print("Now testing the speaker. Press Ctrl + C to skip.")

speaker = Speaker() # initialize a speaker object
speaker.set_sound("stereo-test.mp3") # set audio file to play
time.sleep(1)
print("Playing speaker test audio file")
speaker.play_sound()
print("The initial volume setting is: ", speaker.volume())

try:
	while not speaker.is_stopped():
		time.sleep(0.01)
	print("Speaker test has completed.")
except KeyboardInterrupt:
	print("Ctrl + C was pressed. Terminating speaker test and continuing...")
	speaker.stop_sound()

"""
LCD Tests
"""

print("Now testing the LCD. Press Ctrl + C to skip.")

lcd1 = LCD()

try:
        lcd1.setup_display()
        lcd1.image_to_display("blinka.jpg")
        time.sleep(5)
        lcd1.text_to_display("Testing")
        time.sleep(5)
        lcd1.clear_display()
except KeyboardInterrupt:
        print("Ctrl + C was pressed. Terminating LCD test and continuing...")

"""
Capacitive Tests
"""

print("Now testing capacitive touch input for 20 seconds. Touch an input and the respective input will be printed.")
c1 =  CapTouch()
c1.setup_captouch()
try:
        c1.detect_captouch()
except KeyboardInterrupt:
        print("Ctrl + C was pressed. Terminating capacitive touch test and continuing...")


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


"""
Water Flow Sensor Tests
"""

f1 = FlowSensor()

try:
        f1.setup_water_flow_sensor()
        f1.detect_water_flow_sensor()

except KeyboardInterrupt:
        print("Ctrl + C was pressed. Terminating Water Flow sensor test...")

print("All tests complete.")
