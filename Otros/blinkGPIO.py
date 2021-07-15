import RPi.GPIO as gpio

import time

pin_switch = 11

gpio.setmode(gpio.BOARD)
gpio.setup(pin_switch, gpio.OUT)

for x in range ( 0, 10):

    gpio.output(pin_switch, True)
    time.sleep(0.5)

    gpio.output(pin_switch, False)
    time.sleep(0.5)

print ("Ejecución finalizada")

gpio.cleanup() 