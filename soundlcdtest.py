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

print("Speaker and LCD tests complete")
