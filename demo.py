"""
demo.py

Tests the libraries implemented in hand-hygiene.py
"""

import time
import sys
import RPi.GPIO as GPIO
import hand-hygiene import OLED, FlowSensor, Bubbles, CapTouch, Speaker


"""
Speaker Tests
"""
print("Now testing the speaker...")

speaker = Speaker() # initialize a speaker object
speaker.set_sound("stereo-test.mp3") # set audio file to play

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
Capacitive Touch Tests
"""

ct = CapTouch() # initialize capacitive touch object

ct.setup_captouch()
ct.detect_captouch()



