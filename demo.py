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

print("Now testing capacitive touch sensor input. Follow the prompts or press Ctrl + C to skip.")

ct.detect_captouch()

try:
	while not GPIO.event_detected(ct.out0):
		print("Touch the first capacitive input")
	while not GPIO.event_detected(ct.out1):
		print("Touch the second capacitive input")
	while not GPIO.event_detected(ct.out2):
		print("Touch the third/last capacitive input")
	print("Success. All capacitive inputs are working.")
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

print("Now testing the flow sensor. This will start a counter from 0 and increase if water is flowing, else it will stay constant. Press Ctrl + C to skip.")
time.sleep(3)

flowcount = 0

try:
	flow_end = time.time() + 10
	while time.time() < flow_end:
		fc2 = flowcount
		time.sleep(0.25)
		if(flowcount == fc2):
			print("No water flow detected.")
		else:
			print("Water flow detected.")
		print("Current flow count: ", flowcount)
except KeyboardInterrupt:
	print("Ctrl + C was pressed. Terminating flow sensor test and continuing...")


