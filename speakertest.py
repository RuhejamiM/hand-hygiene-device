import time, sys
import pygame as pg

pg.mixer.init()
pg.init()

sounda = pg.mixer.Sound("piano2.wav")

sounda.play()
time.sleep(10)
