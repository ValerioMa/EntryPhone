from flask import Flask, Response, request
import requests
import threading
import os

import RPi.GPIO as GPIO
from subprocess import call 
import time

app = Flask(__name__)
bell_pin = 17
pir_sensor = 18

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello World!</h1>"

@app.route("/api/entryphone", methods = ['GET', 'POST'])
def entryphone_api():
    url_args = request.args
    ring = 'ring' in url_args.keys()
    ring = ring and int(url_args['ring'].strip()) == 1
    if ring:
        hardware_ring_bell()
        
    return '{"status" : "ok", "ring" : %s}' % int(ring)

@app.before_first_request
def server_init():
    hardware_init()
    
    # start screen manager
    thread = threading.Thread(target=screen_manager)
    thread.start()

def screen_manager():
    last_level = 0
    current_level = 0
    while True:
        current_time = time.ctime()
        current_level = pir_level()
        if  current_level==0 and not current_level==last_level:
            # PIR folling edge
            #print(current_time + " schermo off, PIR value dropped to 0")
            call(["xset","dpms","force","off"]);

        if  current_level==1 and not current_level==last_level:
            # PIR reising edge
            #print(current_time + " schermo on, PIR value reised to 1")
            call(["xset","dpms","force","on"]);

        # Remember last PIR value
        last_level = current_level
        time.sleep( 0.1) # wait 0.1 sec
        
    
"""
	On and off the relay
"""
def hardware_init():
    # bell
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bell_pin,GPIO.OUT)
    # screen on movement
    GPIO.setup(pir_sensor, GPIO.IN)


def hardware_ring_bell():
    for i in range(0,3):
        GPIO.output(bell_pin,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(bell_pin,GPIO.LOW)

def pir_level():
    return GPIO.input(pir_sensor)

# TODO: call on shutdown
def GPIO_destroy():
    GPIO.cleanup() #reset all GPIO

        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
