import hub75
from time import ticks_ms
import time
from machine import RTC
import random
from Vector2D import Vector2D
import math
from math import sin
from math import cos

WIDTH, HEIGHT = 64, 64
hub = hub75.Hub75(64, 64, stb_invert=True)
hub.start()
hub.clear()

def set_rgb(i, j, col):
    hub.set_rgb(i, j, col[0], col[1], col[2])
    
def draw_wave(points, col):

    
    for index, value in enumerate(points):
        
        set_rgb(index, 31 + int(value), col)
    

mapping = (0, 2*math.pi)
xs = [i/64 * 2 * math.pi for i in range(0, 63)]
xs2 = xs.copy()

while True:
    hub.clear()
    for index, value in enumerate(xs):
        xs[index] += 0.3
        xs2[index] += 0.6
    wave = [15*sin(i) + 10*cos(math.pi*i) for i in xs]
    wave2 = [10*cos(i) + 8*sin(math.e*i) for i in xs2]
    draw_wave(wave, [255, 100, 0])
    draw_wave(wave2, [0, 150, 200])
#     draw_wave(ys_2, [0, 100, 200])
    hub.flip()
    time.sleep(0.05)