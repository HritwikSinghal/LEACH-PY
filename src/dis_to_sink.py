from src.LEACH_set_parameters import *
from src.LEACH_configure_sensors import *


def start(Sensors: list[Sensor], myModel: Model):
    n = myModel.n
    for i in range(n):
        distance = sqrt(
            pow((Sensors[i].xd - Sensors[n].xd), 2) + pow((Sensors[i].yd - Sensors[n].yd), 2)
        )
        Sensors[i].dis2sink = distance
