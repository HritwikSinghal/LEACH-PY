from src.LEACH_set_parameters import *
from src.LEACH_configure_sensors import *


def start(Sensors: list[Sensor], myModel: Model):
    n = myModel.n

    for sensor in Sensors[:-1]:
        distance = sqrt(pow((sensor.xd - Sensors[-1].xd), 2) + pow((sensor.yd - Sensors[-1].yd), 2))
        sensor.dis2sink = distance
        print(f'Dist to sink: {Sensors[-1].id} for {sensor.id} is {distance}')
