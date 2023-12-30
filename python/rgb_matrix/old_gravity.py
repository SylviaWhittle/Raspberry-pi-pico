import hub75
from time import ticks_ms
import time
import math
from machine import RTC
import random
from Vector2D import Vector2D

WIDTH, HEIGHT = 64, 64
hub = hub75.Hub75(64, 64, stb_invert=True)
hub.start()
hub.clear()
# def set_rgb(i, j, col):
#     hub.set_rgb(i, j, col[0], col[1], col[2])
def set_array_rgb(i, j, col):
    index = i + j * 64
    rgb_array[index] = 255
    
def update_display():
    for ii in range(64):
        for jj in range(64):
            val = rgb_array[ii + jj * 64]
            val = max(0, val-10)
            rgb_array[ii + jj * 64] = val
                
            col = rgb_array[ii + jj * 64]
    
#     hub.set_rgb(i, j, col[0], col[1], col[2])
            hub.set_rgb(ii, jj % 64, col, col, col)

global WORLD_SCALE
WORLD_SCALE = 1
global TIME_STEP
time_step = 0.1
global G
G = 1
global sun

bodies = []

rgb_array = []

for i in range(4096):
    rgb_array.append(0)

def set_up():
    global sun
    for i in range(10):
        posx = random.randint(0, 63*WORLD_SCALE)
        posy = random.randint(0, 63*WORLD_SCALE)
        angle = math.atan2(posy - 32, posx - 32)
        mag = random.randint(2, 6)
        vx = mag * math.cos(angle + math.pi/2)
        vy = mag * math.sin(angle + math.pi/2)
        bodies.append(Body(posx, posy, vx, vy, 1))
#		bodies.append(Body(32*WORLD_SCALE, 32*WORLD_SCALE, 0, 0, 5000))

        sun = Body(32, 32, 0, 0, 500)
    

class Body:
    def __init__(self, x, y, vx, vy, m):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(vx, vy)
        self.acc = Vector2D(0, 0)
        self.m = m
        self.col = (255, random.randint(0, 255), 10)
    
    def apply_force(self, force):
        f = force / self.m
        self.acc += f
        
    def attract(self, body):
        disp = self.pos - body.pos
        dist_sq = disp.length_square()
        if dist_sq > 1000:
            dist_sq = 1000
        if dist_sq < 100:
            dist_sq = 100
        
        strength = G * self.m * body.m / dist_sq
        body.apply_force(disp.unit() * strength)
    
    def update(self):
        self.vel += self.acc * time_step
        self.pos += self.vel * time_step
        self.acc = Vector2D(0, 0)
   
def draw_bodies():
    hub.clear()
    for body in bodies:
        set_array_rgb(int(body.pos.x/WORLD_SCALE), int(body.pos.y/WORLD_SCALE), body.col)
        set_array_rgb(int(body.pos.x/WORLD_SCALE)-1, int(body.pos.y/WORLD_SCALE), body.col)
        set_array_rgb(int(body.pos.x/WORLD_SCALE), int(body.pos.y/WORLD_SCALE)-1, body.col)
        set_array_rgb(int(body.pos.x/WORLD_SCALE)-1, int(body.pos.y/WORLD_SCALE)-1, body.col)
    update_display()
    hub.flip()

set_up()
while True:
    
    for body in bodies:
        sun.attract(body)
        for other in bodies:
            if body != other:
                pass
                body.attract(other)
    
    for body in bodies:
        body.update()
    
    draw_bodies()     
