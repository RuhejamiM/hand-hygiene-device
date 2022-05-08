import digitalio
import board
import time
import sys
import RPi.GPIO as GPIO
from hand_hygiene import LCD, FlowSensor, Bubbles, CapTouch, Speaker
import pyttsx3


"""
LCD Tests
"""

print("Now testing the LCD. Press Ctrl + C to skip.")

lcd1 = LCD()

try:
        lcd1.setup_display()
        time.sleep(5)

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

