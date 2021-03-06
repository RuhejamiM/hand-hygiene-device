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

global height
global width

global disp

global BORDER
global FONTSIZE

global spi

import time
import pygame as pg
import RPi.GPIO as GPIO
import sys
import os
import time
import busio
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7735

water_flow_pin = 4 # output of water flow sensor is BCM4
fan_pin = 15 # fan output is BCM15 (Note: this has changed because BCM18 is already in use)
servo_pin = 23 # servo output is BCM23; change as needed

# change pin numbers as needed (these are for the capacitive touch input:)
out0 = 26 # output 0 is BCM26
out1 = 6 # output 1 is BCM6 (if BCM19, it conflicts with the speaker breakout)
out2 = 13 # output 2 is BCM13

flow_count = 0 # keep track of water flow count

lcd_cs_pin = digitalio.DigitalInOut(board.CE0) # LCD CS pin is CE0/BCM8; LCD uses SPI communication
lcd_dc_pin = digitalio.DigitalInOut(board.D25) # LCD DC pin is D25/BCM25; this can be changed as needed
lcd_reset_pin = digitalio.DigitalInOut(board.D24) # LCD reset pin is D24/BCM24; this can be changed as needed

BORDER = 5
FONTSIZE = 14


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

        global height
        global width
        global disp
        global spi

        backlight = lcd_dc_pin 
        backlight.switch_to_output()
        backlight.value = True
        BAUDRATE = 24000000
        spi = board.SPI()

        disp = st7735.ST7735R(spi, rotation = 90, cs = lcd_cs_pin, dc = lcd_dc_pin, rst = lcd_reset_pin, baudrate = BAUDRATE) # change display rotation as needed

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

    def backlight_toggle(self):
        if lcd_dc_pin.value is True:
            lcd_dc_pin.value = False
        else:
            lcd_dc_pin.value = True

    def clear_display(self):
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0)) # clear display by sending black rectangle 
        disp.image(image)

    def image_to_display(self, imgfile):
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
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), fill=(252, 186, 3))
        disp.image(image)

        # Draw a smaller inner rectangle
        draw.rectangle((BORDER, BORDER, width - BORDER - 1, height - BORDER - 1), fill=(111, 186, 252))
 
        # Load a TTF Font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
 
        # Draw Some Text
        text = message
        (font_width, font_height) = font.getsize(text)
        draw.text((width // 2 - font_width // 2, height // 2 - font_height // 2), text, font=font, fill=(0, 0, 0))
        disp.image(image)

class FlowSensor: # handles use of the water flow sensor

    def __init__(self):
        # TODO
        return

    def setup_water_flow_sensor(self):
        global water_flow_pin
        GPIO.setup(water_flow_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def water_flow_counter(self, pin):
        global flow_count

        if not GPIO.input(water_flow_pin):
            flow_count += 1

    def detect_water_flow_sensor(self): 
        global flow_count

        GPIO.add_event_detect(water_flow_pin, GPIO.FALLING, callback = self.water_flow_counter)

        flow_end = time.time() + 5 # check flow count for 5 seconds

        while time.time() < flow_end:
            time.sleep(.05) # slight delay before checking for flow again
            print("Water flow sensor turns: " + str(flow_count))
        print("Final flow count: ", flow_count ) # return flow count after 5 seconds of checking

class Bubbles: # handles use of the 5V fan/continuous rotation servo bubble system

    def __init__(self):
        # TODO
        return

    def setup_fan(self):
        
        global fan_pin

        GPIO.setup(fan_pin, GPIO.OUT)

    def start_fan(self):
        GPIO.output(fan_pin, True)

    def stop_fan(self):
        GPIO.output(fan_pin, False)

    def setup_servo(self):
        
        global servo_pin
        global servo
        GPIO.setup(servo_pin, GPIO.OUT)
        servo = GPIO.PWM(servo_pin, 10)

    def start_servo(self):
        global servo
        global servo_pin
        servo.start(0)
        duty = 0.05 # set duty cycle; change as needed
        servo.ChangeDutyCycle(duty)

    def stop_servo(self):
        global servo
        global servo_pin
        servo.stop()

    def setup_bubbles(self):
        self.setup_fan()
        self.setup_servo()
    
    def start_bubbles(self):
        self.start_fan()
        self.start_servo()

    def stop_bubbles(self):
        self.stop_fan()
        self.stop_servo()

class CapTouch: # handles use of the AT42QT1070 capacitive touch sensor 
    def __init__(self):
        # TODO
        return

    def setup_captouch(self): # only using three touch sensors (power on/off, select, scroll)
        
        global out0
        global out1
        global out2

        GPIO.setup(out0, GPIO.IN, pull_up_down = GPIO.PUD_UP) # configure resistor on pin as pullup
        GPIO.setup(out1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(out2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def out0_cb(self, pin): # handle touch detection on first capacitive input
        print("First capacitive input touch detected")

    def out1_cb(self, pin): # handle touch detection on second capacitive input
        print("Second capacitive input touch detected")

    def out2_cb(self, pin): # handle touch detection on third capacitive input
        print("Third capacitive input touch detected")

    def detect_captouch(self): # detect falling edge (input touched)
        global out0 
        global out1
        global out2
        GPIO.add_event_detect(out0, GPIO.FALLING, callback = self.out0_cb, bouncetime = 200) # add bouncetime to prevent false alarm
        GPIO.add_event_detect(out1, GPIO.FALLING, callback = self.out1_cb, bouncetime = 200)
        GPIO.add_event_detect(out2, GPIO.FALLING, callback = self.out2_cb, bouncetime = 200)
        
        captouch_end = time.time() + 20
        while time.time() < captouch_end:
                time.sleep(.01)

class Speaker: # library provided by Jerry Wu (zw1711@nyu.edu)
    def __init__(self, freq=44100, bitsize=-16, channels=2, buffer=2048):
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
        pg.init()

        # set volume to 10% initially so the audio is not too loud
        self.mixer.music.set_volume(0.1)

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
        

