#!/usr/bin/env python
"""
        Detects motion and outputs a sound via a piezo buzzer.
"""

import RPi.GPIO as GPIO
import time


# https://pinout.xyz/pinout/pin16_gpio23   per trovare mappatura PIN
pir_sensor = 18



GPIO.setmode(GPIO.BCM)

GPIO.setup(pir_sensor, GPIO.IN)

try:
    while True:
        pir_level = GPIO.input(pir_sensor)
        print(pir_level)

#        if  pir_level == True: #If PIR pin goes high, motion is detected
#            print ("Motion Detected!")
#            time.sleep(4) #Keep LED on for 4 seconds

    time.sleep(0.2)

except KeyboardInterrupt: #Ctrl+c
    pass #Do nothing, continue to finally

finally:
    GPIO.cleanup() #reset all GPIO
    print ("Program ended")
