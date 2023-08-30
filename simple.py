#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Configuration of the KY-040 rotary encoder pins
CLK_PIN = 17   # Connect CLK pin to GPIO17
DT_PIN = 18    # Connect DT pin to GPIO18
SW_PIN = 27    # Connect SW pin to GPIO27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("GPIO pins configured.")

last_CLK_state = GPIO.input(CLK_PIN)

def volume_control(channel):
    global last_CLK_state

    CLK_state = GPIO.input(CLK_PIN)
    DT_state = GPIO.input(DT_PIN)
    print("Volume control event detected.")
    print("CLK:", CLK_state)
    print("DT:", DT_state)
    if CLK_state != last_CLK_state:
        if DT_state != CLK_state:
            print("Clockwise rotation (increase volume)")
        else:
            print("Counter-clockwise rotation (decrease volume)")
    last_CLK_state = CLK_state

def switch_pressed(channel):
    print("Switch pressed!")

# Attach switch press event
GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=switch_pressed, bouncetime=300)
print("Switch event attached to pin.")

# Attach volume control event
GPIO.add_event_detect(CLK_PIN, GPIO.FALLING, callback=volume_control, bouncetime=50)
print("Volume control attached to pins.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
