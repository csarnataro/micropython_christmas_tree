import neopixel
import time
from random import uniform
from math import floor
from machine import Pin

import micropython

micropython.alloc_emergency_exception_buf(100)

NUM_PIXELS = 42

np = neopixel.NeoPixel(Pin(4), NUM_PIXELS)

button = Pin(13, Pin.IN, Pin.PULL_UP)

builtin_led = Pin(6, Pin.OUT)

current_effect = 0


def handle_interrupt(pin):
    global current_effect
    if pin.value() == 0:
        print("BUTTON PRESSED!")
        builtin_led.value(1)
        time.sleep(1)
        builtin_led.value(0)
        time.sleep(1)
        current_effect = (current_effect + 1) % 4


button.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)


def create_color(red, green, blue):
    return bytearray([red, green, blue])


def demo_1(np):
    global current_effect
    ANIMATION_DELAY = 0.2
    while True and current_effect == 1:
        for offset in range(3):
            for i in range(NUM_PIXELS):  # Amount of LEDs
                idx = (i + offset) % 3
                if idx == 0:
                    np[i] = (255, 0, 0)
                elif idx == 1:
                    np[i] = (0, 255, 0)
                elif idx == 2:
                    np[i] = (0, 0, 255)

                # np[j] = (0,0,0)     ] = (0, 0, 0)

            np.write()
            time.sleep(ANIMATION_DELAY)  # Delay between each frame


def demo_2(np):
    ANIMATION_DELAY = 0.1
    global current_effect
    while True and current_effect == 2:
        num_active_pixels = NUM_PIXELS // 10
        for i in range(NUM_PIXELS):
            np[i] = (0, 0, 0)

        for i in range(num_active_pixels):
            j = floor(uniform(0, NUM_PIXELS))
            np[j] = (255, 255, 255)

        np.write()
        time.sleep(ANIMATION_DELAY)  # Delay between each frame

def off(np):
    for i in range(NUM_PIXELS):
        np[i] = (0, 0, 0)
    np.write()

    
def demo_0(np):
    global current_effect
    n = np.n

    i = 0
    while True and current_effect == 0:
        i = i + 1
        factor = (i*10) % 255
        for j in range(n):
            np[j] = (0, 0, 0)
        for j in range(n):
            # just some random colors changing smoothly
            np[i % n] = (factor , (255 - factor) // 2, 255 - factor)
            np[(i - 1) % n] = (factor // 10 , ((255 - factor) // 4) // 10, (255 - factor) // 10)
            np[(i - 2) % n] = (factor // 40 , ((255 - factor) // 2) // 40, (255 - factor) // 40)

            opposite_pixel = NUM_PIXELS - i

            np[opposite_pixel % n] = (factor , (255 - factor) // 2, 255 - factor)
            np[(opposite_pixel + 1) % n] = (factor // 10 , ((255 - factor) // 4) // 10, (255 - factor) // 10)
            np[(opposite_pixel + 2) % n] = (factor // 40 , ((255 - factor) // 2) // 40, (255 - factor) // 40)

            np[(NUM_PIXELS - i) % n] = (factor , (255 - factor) // 2, 255 - factor)
        np.write()
        time.sleep_ms(30)

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


def initial_blink(np):
    for blink in range(3):

        for i in range(NUM_PIXELS):
            np[i] = (0, 0, 0)
        np.write()

        time.sleep(0.2)  # Delay between each frame

        for i in range(NUM_PIXELS):
            np[i] = (120, 0, 0)
        np.write()

        time.sleep(0.5)  # Delay between each frame

    for i in range(NUM_PIXELS):
        np[i] = (0, 0, 0)
    np.write()


def main():

    initial_blink(np)

    builtin_led.value(0)
    while True:
        time.sleep(0.1)
        if current_effect == 0:
            demo_0(np)
        elif current_effect == 1:
            demo_1(np)
        elif current_effect == 2:
            demo_2(np)
        elif current_effect == 3:
            off(np)
        else:
            print("Error")


if __name__ == "__main__":
    main()
