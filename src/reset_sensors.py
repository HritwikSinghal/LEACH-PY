from math import inf

from src.LEACH_create_basics import *


def start(Sensors: list[Sensor], my_model: Model, dead_num: list[Sensor], round_number):
    for sensor in Sensors:
        print(f"\nresetting {sensor.id}")

        # if sensor is dead
        if sensor.E <= 0 and sensor not in dead_num:
            sensor.df = 1
            dead_num.append(sensor)
            print(f'{sensor.id} is dead, \ndeadnum=')
            for _ in dead_num:
                print(_.id, end=' ')
            print()

        # allow to sensor to become cluster-head. LEACH Algorithm
        AroundClear = 1 / my_model.p  # After every "AroundClear" rounds, let every sensor be CH again
        if round_number % AroundClear == 0:
            sensor.G = 0

        sensor.MCH = my_model.n  # MCH = member of CH, initially all will have sink as their CH
        if sensor.type != 'S':
            sensor.type = 'N'
        sensor.dis2ch = inf

    srp = 0  # counter number of sent routing packets
    rrp = 0  # counter number of receive routing packets
    sdp = 0  # counter number of sent data packets to sink
    rdp = 0  # counter number of receive data packets by sink

    return dead_num, srp, rrp, sdp, rdp
