#app.py
#Implement application and user interface logic here
#Imports hand-hygiene.py and uses its library functions

import threading
import time
import os

import digitalio
import board
import sys

import RPi.GPIO as GPIO

import hand_hygiene

global water_flow_pin
global fan_pin
global servo_pin

global out0
global out1
global out2

global flow_count

global lcd_cs_pin 
global lcd_dc_pin
global lcd_reset_pin

water_flow_pin = 4 # output of water flow sensor is BCM4
fan_pin = 15 # fan output is BCM15 (Note: this has changed because BCM18 is already in use)
servo_pin = 23 # servo output is BCM23; change as needed

# change pin numbers as needed (these are for the capacitive touch input:)
out0 = 26 # output 0 is BCM26
out1 = 6 # output 1 is BCM6 (if BCM19, it conflicts with the speaker breakout)
out2 = 13 # output 2 is BCM13

lcd_cs_pin = digitalio.DigitalInOut(board.CE0) # LCD CS pin is CE0/BCM8; LCD uses SPI communication
lcd_dc_pin = digitalio.DigitalInOut(board.D25) # LCD DC pin is D25/BCM25; this can be changed as needed
lcd_reset_pin = digitalio.DigitalInOut(board.D24) # LCD reset pin is D24/BCM24; this can be changed as needed


#TODO: Add function to keep track of device usage duration and other analytics; store device usage data into a list


"""
Tasks that run once
"""
def setup_parts():

	lcd = hand_hygiene.LCD()
	lcd.setup_display()
	lcd.clear_display()

	captouch = hand_hygiene.CapTouch()
	captouch.setup_captouch()

	speaker = hand_hygiene.Speaker() # initializing a new speaker object also sets it up

	bubbles = hand_hygiene.Bubbles()
	bubbles.setup_bubbles()

	flowsensor = hand_hygiene.FlowSensor()
	flowsensor.setup_water_flow_sensor()

def setup_GPIO():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fan_pin, GPIO.LOW) # set fan output to LOW/off by default
        GPIO.setup(servo_pin, GPIO.LOW) # set servo output to LOW/off by default
        # all other GPIO setups are inside hand_hygiene.py

#TODO: run Flask web UI server

"""
Background Tasks That Run Always
"""

def web_server():
	# function that will start Flask server and push the latest analytical data to it

def count_flow_increment(pin):
	global water_flow_pin
	global flow_count
	if not GPIO.input(water_flow_pin):
		flow_count += 1

def detect_flow():
	global water_flow_pin
	global flow_count
	flow_count = 0
	GPIO.add_event_detect(water_flow_pin, GPIO.FALLING, callback = count_flow_increment)
		
	# initialize flow counter to 0
	# increase counter if flow is detected
	# this will be used to determine if device should turn on or not

	# be sure to remove event_detect later on in cleanup

def usage_timer():
	# record start time of usage session (when water starts flowing)
	# record end time of usage session (when water stops flowing)
	# this will be used to save usage duration for analytics fed to Flask browser app 


#TODO: constantly read water flow sensor, keep device on while water is running 
#TODO: keep track of device usage duration; start and end time/date; feed usage data to Flask app


"""
Other functions
"""

# first check if water is flowing, don't continue until water is flowing; 

def write_state_to_LCD(state):
	if state == "initial":
		# do initial state things (print "Let's wash our hands!" to display)
		# wait a few seconds then 

# use LCD shape drawing library for progress bar




if __name__ == "__main__":
	# one time tasks
	setup_GPIO()
	setup_parts()

	# background tasks    
	# background_tasks = [detect_flow]
    
	# start background tasks with threading
	for task in background_tasks:
		thread = threading.Thread(target=task, daemon=True)
		thread.start()


  
# settings menu can be changed only when the water is off; button does nothing 
# turn the faucet on > start timing and immediately start bubble system > provide audio guidance at each stage
