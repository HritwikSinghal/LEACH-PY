from math import *


def start(Sensors, Model):
    n = Model.n
    for i in range(n):
        distance = sqrt((Sensors[i].xd - Sensors[n + 1].xd) ^ 2
                        + (Sensors[i].yd - Sensors[n + 1].yd) ^ 2)
        Sensors[i].dis2sink = distance
