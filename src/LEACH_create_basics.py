import random
from math import *


class Model:
    def __init__(self, n):
        self.n = n

        # coordinates of field
        self.x = 1000
        self.y = 1000

        # Sink Motion pattern
        self.sink_x = self.x * 0.5
        self.sink_y = self.y * 0.5
        self.sinkE = 100  # Energy of sink

        # Optimal Election Probability of a node to become cluster head
        self.p: float = 0.1

        # %%%%%%%%%%% Energy Model (all values in Joules and each value is for 1byte of data) %%%%%%%%%%%
        # Initial Energy
        self.Eo: float = 2

        # ETX = Energy dissipated in Transmission, ERX = in Receive
        self.Eelec: float = 50 * 0.000000001
        self.ETX: float = 50 * 0.000000001
        self.ERX: float = 50 * 0.000000001

        # Transmit Amplifier types
        self.Efs: float = 10e-12
        self.Emp: float = 0.0013 * 0.000000000001

        # Data Aggregation Energy
        self.EDA: float = 5 * 0.000000001

        # Computation of do
        self.do: float = sqrt(self.Efs / self.Emp)

        # %%%%%%%%%%%%%%%%%%%%%%%%% Run Time Parameters %%%%%%%%%%%%%%%%%%%%%%%%%
        # maximum number of rounds
        self.rmax = 200

        # Data packet size
        self.data_packet_len = 4000

        # Hello packet size
        self.hello_packet_len = 100

        # todo : change this to 10
        # Number of Packets sent in steady-state phase
        self.NumPacket = 10

        # Radio Range
        self.RR: float = 0.5 * self.x * sqrt(2)

        # self.numRx = int(sqrt(self.p * self.n))
        # self.dr = x / self.numRx
        # %%%%%%%%%%%%%%%%%%%%%%%%% END OF PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%


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


def create_sensors(my_model: Model):
    n = my_model.n

    # Configuration sensors
    # created extra one slot for sink
    sensors = [Sensor() for _ in range(n + 1)]

    # for sink
    """ 
    first n - 1 slots in sensors are for normal sensors. (0 to n-1) 
    nth slot is for sink
    so for n=10, 0-9 are 10 normal sensors and 10th slot is for sink 
    so Sensor[10] = 11th node = sink
    """
    sensors[n].xd = my_model.sink_x
    sensors[n].yd = my_model.sink_y
    sensors[n].E = my_model.sinkE
    sensors[n].id = my_model.n
    sensors[n].type = 'S'

    for i, sensor in enumerate(sensors[:-1]):
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
        sensor.MCH = n
        # Dist to sink
        sensor.dis2sink = sqrt(pow((sensor.xd - sensors[-1].xd), 2) + pow((sensor.yd - sensors[-1].yd), 2))
        # print(f'Dist to sink: {sensors[-1].id} for {sensor.id} is {sensor.dis2sink}')

    return sensors
