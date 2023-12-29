import plasma
from plasma import plasma2040
import time

from pimoroni import RGBLED, Button, Analog

NUM_LEDS = 96
DEFAULT_SPEED = 400
UPDATES_PER_SECOND = 30

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)

user_sw = Button(plasma2040.USER_SW)
button_a = Button(plasma2040.BUTTON_A)
button_b = Button(plasma2040.BUTTON_B)
led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)
sense = Analog(plasma2040.CURRENT_SENSE, plasma2040.ADC_GAIN, plasma2040.SHUNT_RESISTOR)

led_strip.start()

speed = DEFAULT_SPEED
offset = 0.0

colour_0 = (252, 0, 111)
colour_1 = (252, 136, 0)
PERIOD = 20

while True:

    a = button_a.read()
    b = button_b.read()

    if a:
        speed -= 10
    if b:
        speed += 10

    for i in range(NUM_LEDS):
        ratio = abs((((i+1 + offset) % (2*PERIOD)) - PERIOD) / PERIOD)
        inv_ratio = 1 - ratio
        
        colour_0_ratio = (colour_0[0] * ratio, colour_0[1] * ratio, colour_0[2] * ratio)
        colour_1_ratio = (colour_1[0] * inv_ratio, colour_1[1] * inv_ratio, colour_1[2] * inv_ratio)
        
        colour = (int(colour_0_ratio[0] + colour_1_ratio[0]), int(colour_0_ratio[1] + colour_1_ratio[1]), int(colour_0_ratio[2] + colour_1_ratio[2]))
        
        led_strip.set_rgb(i, colour[0], colour[1], colour[2])
        
    offset += float(speed) / 1000

    time.sleep(1.0 / UPDATES_PER_SECOND)
