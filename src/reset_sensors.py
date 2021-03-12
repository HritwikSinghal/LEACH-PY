from math import inf
from src.LEACH_set_parameters import *
from src.LEACH_configure_sensors import *


def start(Sensors: list[Sensor], myModel: Model):
    n = myModel.n
    for sensor in Sensors:
        # todo: update deadnum var also
        # if sensor is dead
        if sensor.E <= 0:
            sensor.df = 1

        # MCH = member of CH, initially all will have sink as their CH
        sensor.MCH = n
        sensor.type = 'N'
        sensor.dis2ch = inf
