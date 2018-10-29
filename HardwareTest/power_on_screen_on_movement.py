#!/usr/bin/env python
"""
	Detects motion and outputs a sound via a piezo buzzer. 
"""

import RPi.GPIO as GPIO
from subprocess import call 
import time


# https://pinout.xyz/pinout/pin16_gpio23   per trovare mappatura PIN
pir_sensor = 8

def GPIO_init():
    GPIO.setmode(GPIO.BOARD)

    # ------ INPUT PINS ------
    GPIO.setup(pir_sensor, GPIO.IN)

    # ------ OUTPUT PINS ------

def GPIO_destroy():
    GPIO.cleanup() #reset all GPIO

def pir_level():
    return GPIO.input(pir_sensor)

def main():
    try:
        GPIO_init()
        last_level = 0
        current_level = 0
        while True:
            current_time = time.ctime()
            current_level = pir_level()
            if  current_level==0 and not current_level==last_level:
                # PIR folling edge
                print(current_time + " schermo off, PIR value dropped to 0")
                call(["xset","dpms","force","off"]);

            if  current_level==1 and not current_level==last_level:
                # PIR reising edge
                print(current_time + " schermo on, PIR value reised to 1")
                call(["xset","dpms","force","on"]);

            # Remember last PIR value
            last_level = current_level
            time.sleep( 0.1) # wait 0.1 sec
            
            
    except KeyboardInterrupt: #Ctrl+c
        print("Ctrl+c caught exiting")
        pass #Do nothing, continue to finally

    finally:
        GPIO_destroy() #reset all GPIO
        print ("Program ended")  
  

  
if __name__== "__main__":   
         
        main()
        

