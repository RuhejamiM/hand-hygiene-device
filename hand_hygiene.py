# hand-hygiene.py

# define global variables

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

import time
import pygame as pg
import RPi.GPIO as GPIO
import sys
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7735

water_flow_pin = 4 # output of water flow sensor is BCM4
fan_pin = 18 # fan output is BCM18; change as needed
servo_pin = 23 # servo output is BCM23; change as needed

# change pin numbers as needed (these are for the capacitive touch input:)
out0 = 26 # output 0 is BCM26
out1 = 6 # output 1 is BCM6 (if BCM19, it conflicts with the speaker breakout)
out2 = 13 # output 2 is BCM13

flow_count = 0 # keep track of water flow count

lcd_cs_pin = digitalio.DigitalInOut(board.CE0) # LCD CS pin is CE0/BCM8; LCD uses SPI communication
lcd_dc_pin = digitalio.DigitalInOut(board.D25) # LCD DC pin is D25/BCM25; this can be changed as needed
lcd_reset_pin = digitalio.DigitalInOut(board.D24) # LCD reset pin is D24/BCM24; this can be changed as needed

GPIO.setmode(GPIO.BCM)

class LCD: # handles use of the LCD display. Adapted from provided by Ale Campos (acc726@nyu.edu).
    def __init__(self):
        self.display = None
        # TODO
        return

    def setup_display(self):
        global lcd_cs_pin 
        global lcd_dc_pin
        global lcd_reset_pin

        backlight = digitalio.DigitalInOut(lcd_dc_pin) 
        backlight.switch_to_output()
        backlight.value = True
        BAUDRATE = 24000000
        spi = board.SPI()

        disp = st7735.ST7735R(spi, rotation = 270, cs = lcd_cs_pin, dc = lcd_dc_pin, st = lcd_reset_pin, baudrate = BAUDRATE) # change display rotation as needed

        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0)) # clear display by sending black rectangle 
        disp.image(image)

    def clear_display(self):
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0)) # clear display by sending black rectangle 
        disp.image(image)
"""
    def image_to_display(self, imgfile)
        image = Image.open(imgfile)

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

        # Display image.
        disp.image(image)


    def text_to_display(self, message):
        # TODO
        return
"""
class FlowSensor: # handles use of the water flow sensor

    def __init__(self):
        # TODO
        return

    def setup_water_flow_sensor(self):
        global water_flow_pin
        GPIO.setup(water_flow_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def water_flow_counter(self):
        global flow_count

        if not GPIO.input(water_flow_pin):
            flow_count += 1

    def detect_water_flow_sensor(self): 
        global flow_count

        GPIO.add_event_detect(water_flow_pin, GPIO.FALLING, callback = water_flow_counter)

        flow_end = time.time() + 5 # check flow count for 5 seconds

        while time.time() < flow_end:
            time.sleep(.05) # slight delay before checking for flow again

        return flow_count # return flow count after 5 seconds of checking

class Bubbles: # handles use of the 5V fan/continuous rotation servo bubble system

    def __init__(self):
        # TODO
        return

    def setup_fan(self):
        
        global fan_pin

        GPIO.setup(fan_pin, GPIO.out)

    def start_fan(self):
        GPIO.output(fan_pin, True)

    def stop_fan(self):
        GPIO.output(fan_pin, False)

    def setup_servo(self):
        
        global servo_pin
        global servo
        servo = GPIO.PWM(servo_pin, 50)

    def start_servo(self):
        servo.start(0)
        duty = 0.05 # set duty cycle; change as needed
        servo.ChangeDutyCycle(duty)

    def stop_servo(self):
        servo.stop()

    def setup_bubbles(self):
        setup_fan()
        setup_servo()
    
    def start_bubbles(self):
        start_fan()
        start_servo()

    def stop_bubbles(self):
        stop_fan()
        stop_servo()

class CapTouch: # handles use of the AT42QT1070 capacitive touch sensor 
    def __init__(self):
        # TODO
        return

    def setup_captouch(self): # only using three touch sensors (power on/off, select, scroll)
        
        global out0
        global out1
        global out2

        GPIO.setup(out0, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # configure resistor on pin as pulldown
        GPIO.setup(out1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(out2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def out0_cb(self): # handle touch detection on first capacitive input
        print("First capacitive input touch detected")

    def out1_cb(self): # handle touch detection on second capacitive input
        print("Second capacitive input touch detected")

    def out2_cb(self): # handle touch detection on third capacitive input
        print("Third capacitive input touch detected")

    def detect_captouch(self): # detect falling edge (input touched)
        GPIO.add_event_detect(out0, GPIO.FALLING,  bouncetime = 200, callback = out0_cb) # add bouncetime to prevent false alarm
        GPIO.add_event_detect(out1, GPIO.FALLING,  bouncetime = 200, callback = out1_cb)
        GPIO.add_event_detect(out2, GPIO.FALLING,  bouncetime = 200, callback = out2_cb)


class Speaker: # library provided by Jerry Wu (zw1711@nyu.edu)
    def __init__(self, freq=32000, bitsize=-16, channels=2, buffer=2048): # note: change the frequency to match the frequency of the audio file to be played
        """
        initialize the speaker module
        freq: audio CD quality
        bitsize: unsigned 16 bit
        channels: 1 is mono, 2 is stereo
        buffer: number of samples (experiment to get right sound)
        """

        # initialize mixer (for playing sound)
        self.mixer = pg.mixer
        self.mixer.init(freq, bitsize, channels, buffer)

        # set volume to 20%
        self.mixer.music.set_volume(0.2)

        # pause status, stop is not paused, only pause will turn paused to True
        self.paused = False

    def set_sound(self, sound):
        """
        set the sound that will be play
        sound: the relative path to the sound file
        """

        self.sound = sound

    def play_sound(self):
        """
        stream music with mixer.music module in non-blocking manner
        this will stream the sound from disk while playing
        """

        try:
            self.mixer.music.load(self.sound)
        except pg.error:
            # TODO: maybe change to blink of led
            print("File {} not found! {}".format(self.sound, pg.get_error()))
            return

        self.mixer.music.play()

    def stop_sound(self):
        """
        stop playing sound if any
        """

        self.mixer.music.stop()
        # unload the file to free up resource
        self.mixer.music.unload()
        self.paused = False

    def is_stopped(self):
        """
        check if sound stopped, pause is not stop
        """

        return (not self.mixer.music.get_busy()) and (not self.paused)

    def is_paused(self):
        """
        check if sound paused
        """

        return self.paused

    def volume(self):
        """
        get the volume of the speaker
        """

        return round(self.mixer.music.get_volume(), 1)

    def set_volume(self, volume):
        """
        set volume
        """

        self.mixer.music.set_volume(volume)

    def increase_volume(self):
        """
        increase 10% of the total volume
        """

        # the set_volume function will auto truncate the input
        self.mixer.music.set_volume(self.volume() + 0.1)

    def decrease_volume(self):
        """
        decrease 10% of the total volume
        """

        self.mixer.music.set_volume(self.volume() - 0.1)

    def pause(self):
        """
        pause the sound
        """

        self.mixer.music.pause()
        self.paused = True

    def resume(self):
        """
        resume the sound
        """

        self.mixer.music.unpause()
        self.paused = False

    def __del__(self):
        pg.quit()
        
def clean_gpio(): # when finished, clean GPIO pins to avoid unwanted behavior after program ends
    GPIO.cleanup()