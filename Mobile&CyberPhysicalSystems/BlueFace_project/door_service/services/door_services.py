import json
import config

if not config.TEST_MACHINE:
    import services.GPIO_service as GPIO_service
else:
    import tests.GPIO_mock as GPIO_service

gpio = GPIO_service.Class2World()


def open_door_message_handler(payload):
    '''
    This method expect a json payload with the following format:
        {
            "door_id": string,
            "user": string,
            "open": Bool
        }
    if "open" == true and "to"== current device id (the id inside the configuration file) open the door,
    otherwise if "open"==false and "to"==id flash the error light (this means we received a bad response from server

    this method returns a boolean representing the success of the operation
    '''
    message = json.loads(payload)
    if message["door_id"] == config.DEVICE_ID:
        if message["open"]:
            gpio.door_open()
        else:
            gpio.flash_error_led()
            return False

        return True

    return False


def cleanup_handler():
    gpio.cleanup()
