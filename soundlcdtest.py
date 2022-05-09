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
import pyttsx3

GPIO.setmode(GPIO.BCM)
file = "audio/stereo-test.mp3"
vol = 0.5

"""
Speaker Tests
"""
print("Now testing the speaker. Press Ctrl + C to skip.")

speaker = Speaker() # initialize a speaker object

voice_engine = pyttsx3.init()
voice_engine.setProperty('volume', vol)
voice_engine.setProperty('voice', "english-us")
voice_engine.setProperty('rate', 150)
voice_engine.say("Fifty Percent Volume")
voice_engine.runAndWait()

speaker.set_sound(file) # set audio file to play
speaker.set_volume(vol)
time.sleep(1)
print("Playing speaker test audio file")
speaker.play_sound()
print(speaker.self.sound())
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
        lcd1.image_to_display("img/welcome.png")
        time.sleep(5)
        lcd1.image_to_display("img/scrub_hands.png")
        time.sleep(5)
        lcd1.image_to_display("img/rinse_hands.png")
        time.sleep(5)
        lcd1.image_to_display("img/dry_hands.png")
        time.sleep(5)
        lcd1.image_to_display("img/finished.png")
        time.sleep(5)
        lcd1.text_to_display("Testing to see if text wrapping does indeed work")
        time.sleep(5)
        lcd1.clear_display()
except KeyboardInterrupt:
        print("Ctrl + C was pressed. Terminating LCD test and continuing...")
lcd1.clear_display()
print("Speaker and LCD tests complete")
