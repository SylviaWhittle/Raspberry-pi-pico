import hub75
from time import ticks_ms
import time
import math
from machine import RTC
import random

WIDTH, HEIGHT = 64, 64
hub = hub75.Hub75(64, 64, stb_invert=True)
hub.start()
hub.clear()
def set_rgb(i, j, col):
    hub.set_rgb(i, j, col[0], col[1], col[2])

px, py = -0.7746806106269039, -0.1374168856037867 #Tante Renate
R = 3
max_iteration = 100
w, h = 1024,1024
mfactor = 0.5

def mandelbrot(x, y, max_iteration, minx, maxx, miny, maxy):
    zx = 0
    zy = 0
    RX1, RX2, RY1, RY2 = px-R/2, px+R/2,py-R/2,py+R/2
    cx = (x-minx)/(maxx-minx)*(RX2-RX1)+RX1
    cy = (y-miny)/(maxy-miny)*(RY2-RY1)+RY1
    i=0
    while zx**2 + zy**2 <= 4 and i < max_iteration:
        temp = zx**2 - zy**2
        zy = 2*zx*zy + cy
        zx = temp + cx
        i += 1
    return i

def gen_mandelbrot_image(sequence):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = mandelbrot(x, y, max_iteration, 0, WIDTH-1, 0, HEIGHT-1)
            v = c**mfactor/max_iteration**mfactor
            hv = 0.67-v
            if hv<0: hv+=1
            hub.set_hsv(x, y, hv,1,1-(v-0.1)**2/0.9**2)
        hub.flip()
            
R=3
f = 0.975
RZF = 1/1000000000000
k=1
while R>RZF:
  if k>100: break
  mfactor = 0.5 + (1/1000000000000)**0.1/R**0.1
  print(k,mfactor)
  gen_mandelbrot_image(k)
  R *= f
  k+=1
    
    
    

