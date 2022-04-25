"""
demo.py

Tests the libraries implemented in hand-hygiene.py
"""

import time
import sys
import RPi.GPIO as GPIO
from hand-hygiene import LCD, FlowSensor, Bubbles, CapTouch, Speaker


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

print("Now testing capacitive touch sensor input. Press Ctrl + C to skip.")

try:
	ct_end = time.time() + 10
	ct.detect_captouch()
	print("Test all of the capacitive inputs by triggering them. The input that is triggered will be displayed.")

	while(time.time() < ct_end):
		time.sleep(.005)
	
	print("Check if all touches have registered. Continuing to next test in 5 seconds...")
	time.sleep(5)
except KeyboardInterrupt:
	print("Ctrl + C was pressed. Terminating capacitive touch test and continuing...")

"""
Bubble System Tests
"""

b1 = Bubbles() # initialize bubble object

b1.setup_bubbles()

print("Now testing the bubble system. This will run the fan and start the servo for 10 seconds. Press Ctrl + C to skip.")

try:
	b1.start_bubbles()
	time.sleep(10)
	b1.stop_bubbles()
except KeyboardInterrupt:
	print("Ctrl + C was pressed. Terminating bubble system test and continuing...")

"""
Flow Sensor Tests
"""

fs = FlowSensor() # initialize flow sensor object

fs.setup_water_flow_sensor()
print("Now testing the flow sensor. This will take about 5 seconds. Press Ctrl + C to skip.")

try:
	fs.detect_water_flow_sensor()
	if fs.flow_count > 2: # adjust flow count detection threshold as needed
		print("Water flow has been detected.")
	else:
		print("No water flow detected.")
	print("Final flow count: ", fs.flow_count)
except KeyboardInterrupt:
	print("Ctrl + C was pressed. Terminating flow sensor test and continuing...")

"""
LCD Tests
"""

lcd1 = LCD() # initialize LCD object

lcd1.setup_display()

#TODO: add remaining LCD test

