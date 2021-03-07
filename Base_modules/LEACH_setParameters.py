from math import *


class Area:
    def __init__(self):
        # Field Dimensions - x and y maximum (in meters)
        self.x = 1000
        self.y = 1000


class Model:
    def __init__(self, n, x, y):
        self.n = n

        # Sink Motion pattern
        self.sinkx = x * 0.5
        self.sinky = y * 0.5

        # Optimal Election Probability of a node to become cluster head
        self.p = 0.1

        # %%%%%%%%%%% Energy Model (all values in Joules and each value is for 1byte of data) %%%%%%%%%%%
        # Initial Energy
        self.Eo = 2

        # ETX = Energy dissipated in Transmission, ERX = in Receive
        # Eelec=Etx=Erx
        self.ETX = 50 * 0.000000001
        self.ERX = 50 * 0.000000001

        # Transmit Amplifier types
        self.Efs = 10e-12
        self.Emp = 0.0013 * 0.000000000001

        # Data Aggregation Energy
        self.EDA = 5 * 0.000000001

        # Computation of do
        self.do = sqrt(self.Efs / self.Emp)

        # %%%%%%%%%%%%%%%%%%%%%%%%% Run Time Parameters %%%%%%%%%%%%%%%%%%%%%%%%%
        # maximum number of rounds
        self.rmax = 200

        # Data packet size
        self.DpacketLen = 4000

        # Hello packet size
        self.HpacketLen = 100

        # Number of Packets sent in steady-state phase
        self.NumPacket = 10

        # Radio Range
        self.RR = 0.5 * x * sqrt(2)

        # self.numRx = int(sqrt(self.p * self.n))
        # self.dr = x / self.numRx
        # %%%%%%%%%%%%%%%%%%%%%%%%% END OF PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%


def setParameters(n):
    myArea = Area()
    myModel = Model(n, myArea.x, myArea.y)

    return myArea, myModel
