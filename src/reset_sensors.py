from math import inf

from src.LEACH_create_sensors import *


def start(Sensors: list[Sensor], myModel: Model, dead_num):
    for sensor in Sensors:
        print(f"resetting {sensor.id}")
        # todo: update deadnum var also
        # if sensor is dead
        if sensor.E <= 0 and sensor.df == 0:
            sensor.df = 1
            sensor.E = 0
            print(f'{sensor.id} is dead. so incrementing dead_num by 1 to {dead_num + 1}')
            dead_num += 1

        sensor.MCH = myModel.n  # MCH = member of CH, initially all will have sink as their CH
        sensor.type = 'N'
        sensor.dis2ch = inf

    return dead_num
