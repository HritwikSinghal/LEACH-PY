import random
from math import *

class Sensor:
    def __init__(self):
        self.xd = 0
        self.yd = 0
        self.G = 0
        self.df = 0
        self.type = 'N'
        self.E: float = 0
        self.id = 0
        self.dis2sink: float = 0
        self.dis2ch: float = 0
        self.MCH = 0  # Member of which CH
        self.RR = 0


def start(my_model):
    n = my_model.n

    # Configuration Sensors
    # created extra one slot for sink
    Sensors = [Sensor() for _ in range(n + 1)]

    # for sink
    """ 
    first n - 1 slots in Sensors are for normal sensors. (0 to n-1) 
    nth slot is for sink
    so for n=10, 0-9 are 10 normal sensors and 10th slot is for sink 
    """
    Sensors[n].xd = my_model.sinkx
    Sensors[n].yd = my_model.sinky
    Sensors[n].E = my_model.sinkE
    Sensors[n].id = my_model.n

    for i, sensor in enumerate(Sensors[:-1]):
        # set x location
        sensor.xd = random.randint(1, my_model.x)
        # set y location
        sensor.yd = random.randint(1, my_model.y)
        # Determinate whether in previous periods a node has been cluster-head or not? not=0 and be=n
        sensor.G = 0
        # dead flag. Whether dead or alive S[i].df=0 alive. S[i].df=1 dead.
        sensor.df = 0
        # initially there are not each cluster heads
        sensor.type = 'N'
        # initially all nodes have equal Energy
        sensor.E = my_model.Eo
        # id
        sensor.id = i
        # Radio range
        sensor.RR = my_model.RR
        # Dist to sink
        sensor.dis2sink = sqrt(pow((sensor.xd - Sensors[-1].xd), 2) + pow((sensor.yd - Sensors[-1].yd), 2))
        # print(f'Dist to sink: {Sensors[-1].id} for {sensor.id} is {sensor.dis2sink}')

    return Sensors
