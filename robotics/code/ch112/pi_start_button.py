# pi_start_button.py - Rover's start button and status LED on the Raspberry Pi, with gpiozero
from signal import pause

from gpiozero import LED, Button                 # comes with Raspberry Pi OS

status = LED(27)                                 # GPIO 27 -> 330 ohm resistor -> LED -> GND
button = Button(17, bounce_time=0.05)            # GPIO 17 -> button -> GND (gpiozero turns on the pull-up)
running = False


def toggle_run():                                # gpiozero calls this when the button is pressed
    global running
    running = not running
    if running:
        status.on()                              # steady light: Rover is driving
        print("Rover: start")
    else:
        status.blink(on_time=0.2, off_time=0.8)  # short blinks: ready and waiting
        print("Rover: stop")


button.when_pressed = toggle_run
status.blink(on_time=0.2, off_time=0.8)
print("ready: press the button to start")
pause()                                          # wait for ever; gpiozero runs toggle_run in the background
