from services.GPIO_interface import Interface2World


class Class2World(Interface2World):
    def door_open(self):
        print("Door Opened")

    def flash_error_led(self):
        print("Error Led Flashing")

    def cleanup(self):
        print("Cleaning up gpio ports")


