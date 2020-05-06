import RPi.GPIO as GPIO
import time
from services.GPIO_interface import Interface2World
import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.OPEN_DOOR_PIN, GPIO.OUT)
GPIO.setup(config.ERROR_PIN, GPIO.OUT)

class Class2World(Interface2World):
    """Class used for the physical interaction with the GPIO of the Raspberry Pi"""

    def door_open(self):
            GPIO.output(config.OPEN_DOOR_PIN, GPIO.HIGH)
            time.sleep(4)
            GPIO.output(config.OPEN_DOOR_PIN, GPIO.LOW)

    def flash_error_led(self):
        for i in range(5):
            GPIO.output(config.ERROR_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(config.ERROR_PIN, GPIO.LOW)
            time.sleep(0.2)

    def cleanup(self):
        GPIO.cleanup()


