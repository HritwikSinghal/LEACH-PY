from math import inf

from src.LEACH_create_basics import *


def start(Sensors: list[Sensor], my_model: Model, round_number):
    for sensor in Sensors[:-1]:
        sensor.MCH = my_model.n  # MCH = member of CH, initially all will have sink as their CH
        sensor.type = 'N'
        sensor.dis2ch = inf
        # print(f"\nresetting {sensor.id}")
        #
        # # allow to sensor to become cluster-head. LEACH Algorithm
    AroundClear = 1 / my_model.p  # After every "AroundClear" rounds, let every sensor be CH again
    if round_number % AroundClear == 0:
        for sensor in Sensors:
            sensor.G = 0
    return 0, 0, 0, 0
