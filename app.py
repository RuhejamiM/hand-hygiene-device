#app.py
#Implement application and user interface logic here
#Imports hand-hygiene.py and uses its library functions

import threading, time, os, board, sys, hand_hygiene

from cgitb import text
from flask import Flask, render_template, redirect, request

import RPi.GPIO as GPIO

global water_flow_pin
global fan_pin
global servo_pin

global flow_count

global temp_flow_count

global song_selection
global volume_level

global override

global settings_button_status
global scroll_button_status
global select_button_status

global freq # handle frequency of hand washing (average number of times washed in a day)
global dur # handle avg duration of each hand washing
global washcount

settings_button_status = False
scroll_button_status = False
select_button_status = False

fan_pin = 15 # fan output is BCM15 (Note: this has changed because BCM18 is already in use)
servo_pin = 23 # servo output is BCM23; change as needed

# change pin numbers as needed (these are for the capacitive touch input:)
out0 = 26 # output 0 is BCM26; this is the settings button
out1 = 6 # output 1 is BCM6 (if BCM19, it conflicts with the speaker breakout); this is the scroll button
out2 = 13 # output 2 is BCM13; this is the select button

override = True # override is active; no water flow needed to activate system while this is set to 'True'

song_selection = "audio/stereo_test.mp3" # default song selection; CHANGE THIS LATER
volume_level =  0.5 # default volume level on a scale from 0.0 to 1.0; this can be changed in settings

#TODO: Add function to keep track of device usage duration and other analytics; store device usage data into a list

def count_flow_increment(channel):
        global flow_count
        if not GPIO.input(channel):
                flow_count += 1

def settings_button(channel):
	global settings_button_status
	if not GPIO.input(channel):
		settings_button_status = True
		time.sleep(1)
		settings_button_status = False

def scroll_button(channel):
	global scroll_button_status
	if not GPIO.input(channel):
		scroll_button_status = True
		time.sleep(1)
		scroll_button_status = False

def select_button(channel):
	global select_button_status
	if not GPIO.input(channel):
		select_button_status = True
		time.sleep(1)
		select_button_status = False

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

def detect_flow(): # set up counter for flow detection and start watching for falling edge on water flow sensor to increment the counter
        global flow_count
        flow_count = 0
        GPIO.add_event_detect(water_flow_pin, GPIO.FALLING, callback = count_flow_increment)


        # be sure to remove event_detect later on in cleanup
def detect_button():
	GPIO.add_event_detect(out0, GPIO.FALLING, callback = settings_button, bouncetime = 200)
	GPIO.add_event_detect(out1, GPIO.FALLING, callback = scroll_button, bouncetime = 200)
	GPIO.add_event_detect(out2, GPIO.FALLING, callback = select_button, bouncetime = 200)


#TODO: run Flask web UI server

"""
Background Tasks That Run Always
"""
def water_is_running():
	global temp_flow_count
	while True:
		temp_flow_count = flow_count
		time.sleep(1.5) # sleep for 1.5s to allow flow_count to increase if water is flowing
		if(flow_count > temp_flow_count):
			return True
		else:
			return False

def interface():
	# do interface logic stuff here
	global override
	while True:
		while (water_is_running() or (override is True)):
			print("Either the water is running or the water checking override is active. Now starting device.")
			# override will turn itself off after system runs once
			lcd.image_to_display("img/welcome.png") # display "Welcome to the Hand Hygiene Device" screen
			# TODO: add TTS greeting here
			time.sleep(4)
			lcd.image_to_display("img/scrub_hands.png") # display "scrub hands" screen
			# TODO: add TTS instruction here
			bubbles.start_bubbles() # start servo and fan
			speaker.set_sound(song_selection) # set this in the settings page or choose one by default
			speaker.set_volume(volume_level)
			speaker.play_sound()
			time.sleep(20) # the scrubbing stage requires at least 20 seconds
			lcd.image_to_display("img/rinse_hands.png") # display "rinse hands" screen
			# TODO: add TTS instruction here
			time.sleep(10)  # pause while rinsing
			lcd.image_to_display("img/dry_hands.png") # display "dry hands" screen
			time.sleep(7) # pause while drying
			lcd.image_to_display("img/finished.png") # display "we're all done" screen
			# TODO: add TTS congratulations message here
			time.sleep(3)
			speaker.stop_sound()
			bubbles.stop_bubbles()
			override = False # disable water flow check override; override will only activate again the next time the program is restarted
			time.sleep(1)
			while(water_is_running()):
				print("Water is still running. Need to shut it off before the device can stop.")
				lcd.image_to_display("img/turn_water_off.png") # display reminder to shut water off before device can stop
				# TODO: TTS prompt to turn water
		# water not flowing; only settings menu is active now so we can now check for touch inputs
		while True:
			lcd.clear_display() # when water stops or if water is not running make sure LCD is clear, speaker is stopped, bubble system stopped
			speaker.stop_sound()
			bubbles.stop_bubbles()
			if settings_button_status is True:


def web_server():
	# function that will start Flask server and push the latest analytical data to it

	app = Flask(__name__, static_folder='assets')

	@app.route("/")
	def home():
    		return redirect("/templates/index")

	@app.route("/templates/index")
	def home_template():
    		return render_template("index.html")

	@app.route("/templates/statistics")
	def stats_template():
    		# set frequency and duration elsewhere
    		return render_template("statistics.html", frequency=freq, duration=dur)

    	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)


def usage_timer():

	# record start time of usage session (when water starts flowing)
	# record end time of usage session (when water stops flowing)
	# this will be used to save usage duration for analytics fed to Flask browser app 


#TODO: constantly read water flow sensor, keep device on while water is running 
#TODO: keep track of device usage duration; start and end time/date; feed usage data to Flask app


"""
Other functions
"""


# use LCD shape drawing library for progress bar?


if __name__ == "__main__": # main function; this runs when program is called
	try:
		print("Now initializing system. This will run indefinitely. Press Ctrl + C at any time to terminate system and clean up GPIO pins.")
		# one time tasks
		setup_GPIO()
		setup_parts()
		detect_flow()

		time.sleep(2) # allow water flow to be registered by sensor

		# background tasks
		background_tasks = [water_is_running, interface, web_server]

		# start background tasks with threading
		for task in background_tasks:
			thread = threading.Thread(target=task, daemon=True)
			thread.start()
	except KeyboardInterrupt:
		print("Cleaning up GPIO and quitting...")
		GPIO.cleanup()


# settings menu can be changed only when the water is off; button does nothing 
# turn the faucet on > start timing and immediately start bubble system > provide audio guidance at each stage
