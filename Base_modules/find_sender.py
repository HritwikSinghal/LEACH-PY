from Base_modules.LEACH_configure_sensors import *


def start(Sensors: list[Sensor], Receiver):
    sender = []

    for sensor in Sensors:
        if sensor.MCH == Receiver and sensor.id != Receiver:
            sender.append(sensor.id)

    return sender
