from subprocess import call
import RPi.GPIO as GPIO
import time
import os


class HardwareInterface:

    def __log_hw_info(self, msg):
        print("{} - {}".format(time.ctime(), msg))

    def __init__(self):
        """   Pin definition   """
        # pairs: pid_id, initial_value.
        self.out_pins = {"bell" : {"id" : 17, "init" : GPIO.HIGH} }
        self.in_pins  = {"pir" : {"id" : 27}  }
        # to avoid multiple bell rings.
        self.bell_last_ring = 0

        self.__log_hw_info("init HardwareInterface")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Output pin initialization
        for name, config in self.out_pins.items():
            pin_id = config["id"]
            init_value = config["init"]
            self.__log_hw_info("out: {} pin number {}, initial value: {}".format(name, pin_id, init_value))
            GPIO.setup(pin_id, GPIO.OUT) # , initial=init_value

        # Input pin initialization
        for name, config in self.in_pins.items():
            pin_id = config["id"]
            self.__log_hw_info("in: {} pin number {}".format(name, pin_id))
            GPIO.setup(pin_id, GPIO.IN)

        def toggle_screen(channel):
            state = self.pir_status()
            if state:
                self.screen_on()
            else:
                self.screen_off()

        pir_pin = self.in_pins["pir"]["id"]
        GPIO.add_event_detect(pir_pin, GPIO.BOTH, callback=toggle_screen,
                              bouncetime=300)

    def __del__(self):
        self.__log_hw_info("deinit HardwareInterface")
        GPIO.cleanup()

    def screen_off(self):
        current_time = time.ctime()
        self.__log_hw_info("turn screen off")
        call(["/usr/bin/xset", "-display", ":0.0", "dpms", "force", "off"])

    def screen_on(self):
        current_time = time.ctime()
        self.__log_hw_info("turn screen on")
        call(["/usr/bin/xset", "-display", ":0.0", "dpms", "force", "on"])

    def __get_pin_status(self, pin_name):
        if pin_name in self.in_pins:
            pin_number = self.in_pins.get(pin_name)["id"]
            return GPIO.input(pin_number)
        else:
            raise ValueError('Requested input pin is not in the list')

    def __set_pin_status(self, pin_name, status):
        if pin_name in self.out_pins:
            if status:
                pin_number = self.out_pins.get(pin_name)["id"]
                GPIO.output(pin_number,GPIO.HIGH)
            else:
                pin_number = self.out_pins.get(pin_name)["id"]
                GPIO.output(pin_number,GPIO.LOW)
            return
        else:
            raise ValueError('Requested input pin is not in the list')

    def pir_status(self):
        return self.__get_pin_status("pir")

    def set_bell_status(self, value):
        self.__set_pin_status("bell", value)

    def ring_bell(self):
        if time.time() - self.bell_last_ring < 6:
            self.__log_hw_info("too close ring requests")
            return False
        try:
            self.__log_hw_info("ringing bell")
            for i in range(0,3):
                self.set_bell_status(0)
                time.sleep(0.5)
                self.set_bell_status(1)
                time.sleep(1)
        finally:
            self.set_bell_status(1)
            self.bell_last_ring = time.time()
        return True
