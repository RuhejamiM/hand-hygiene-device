# hand-hygiene.py

# define global variables
global DISPLAY_ADDRESS

# TODO: DISPLAY_ADDRESS = 

import time
import pygame as pg
import RPi.GPIO as GPIO
import sys

class OLED: # handles use of the OLED display (we have not received the part yet; fill in library after specific part is received)
    def __init__(self):
        self.display = None
        # TODO
        return

    def setup_display(self, address = DISPLAY_ADDRESS):
        # TODO
        return

    def clear_display(self):
        # TODO
        return

    def text_to_display(self, message):
        # TODO
        return

    def clear_display(self):
        # TODO
        return

class FlowSensor: # handles use of the water flow sensor

    def __init__(self):
        # TODO
        return

    def setup_water_flow_sensor(self):
        global water_flow_pin

        water_flow_pin = 4 # output of water flow sensor is BCM4

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(water_flow_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def detect_water_flow_sensor(self): 

        """
        note: in app logic program, use "if GPIO.event_detected(water_flow_pin)" to run code on falling edge (when water flows, output goes low then high then low continuously) 
        """

        GPIO.add_event_detect(water_flow_pin, GPIO.FALLING)

class Bubbles: # handles use of the 5V fan/continuous rotation servo bubble system

    def __init__(self):
        # TODO
        return

    def setup_fan(self):
        GPIO.setmode(GPIO.BCM)
        global fan_pin

        fan_pin = 18 # fan output is BCM18; change as needed

        GPIO.setup(fan_pin, GPIO.out)

    def start_fan(self):
        GPIO.output(fan_pin, True)

    def stop_fan(self):
        GPIO.output(fan_pin, False)

    def setup_servo(self):
        GPIO.setmode(GPIO.BCM)
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

    def setup_captouch(): # only using three touch sensors (power on/off, select, scroll)
        GPIO.setmode(GPIO.BCM)
        global out0
        global out1
        global out2

        # change pin numbers as needed

        out0 = 26 # output 0 is BCM26
        out1 = 19 # output 1 is BCM19
        out2 = 13 # output 2 is BCM13


        GPIO.setup(out0, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # configure resistor on pin as pulldown
        GPIO.setup(out1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(out2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def detect_captouch(): # detect falling edge (input touched)
        """
        note: in app logic program, use "if GPIO.event_detected(out0)" to run code when an input is touched

        """
        GPIO.add_event_detect(out0, GPIO.FALLING,  bouncetime = 200) # add bouncetime to prevent false alarm
        GPIO.add_event_detect(out1, GPIO.FALLING,  bouncetime = 200)
        GPIO.add_event_detect(out2, GPIO.FALLING,  bouncetime = 200)


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