from abc import ABC, abstractmethod

class Interface2World(ABC):

    @abstractmethod
    def door_open(self):
        pass

    @abstractmethod
    def flash_error_led(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
