import bluetooth
import signal
import sys

from config import BT_TIME_DELTA


def __dictify_device(device):
    keys = ('address', 'name')

    # decode the address (convert from bytes to str)
    address = device[0].decode('utf-8')
    name = device[1]
    values = [address, name]
    return dict(zip(keys, values))


def discover_devices():
    print("Performing inquiry...")

    nearbly_devices = bluetooth.discover_devices(duration=BT_TIME_DELTA, lookup_names=True, flush_cache=True)

    print("I've found {} devices".format(len(nearbly_devices)))

    formatted_devices = [__dictify_device(d) for d in nearbly_devices]
    return formatted_devices


def get_local_device_address():
    return bluetooth.read_local_bdaddr()[0].decode(encoding='utf-8', errors='strict')


if __name__ == '__main__':
    print("LOCAL ADDRESS:", get_local_device_address())
    print(discover_devices())
