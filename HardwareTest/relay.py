#!/usr/bin/env python
"""
	On and off the relay
"""
import RPi.GPIO as GPIO
import time

bell_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(bell_pin,GPIO.OUT)
print("Drin")
GPIO.output(bell_pin,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(bell_pin,GPIO.LOW)

