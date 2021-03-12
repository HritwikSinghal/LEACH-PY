from math import *


class Model:
    def __init__(self, n):
        self.n = n

        # coordinates of field
        self.x = 1000
        self.y = 1000

        # Sink Motion pattern
        self.sinkx = self.x * 0.5
        self.sinky = self.y * 0.5
        self.sinkE = 100  # Energy of sink

        # Optimal Election Probability of a node to become cluster head
        self.p: float = 0.1

        # %%%%%%%%%%% Energy Model (all values in Joules and each value is for 1byte of data) %%%%%%%%%%%
        # Initial Energy
        self.Eo: float = 0.2

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
        self.rmax = 50

        # Data packet size
        self.DpacketLen = 4000

        # Hello packet size
        self.HpacketLen = 100

        # todo : change this to 10
        # Number of Packets sent in steady-state phase
        self.NumPacket = 1

        # Radio Range
        self.RR: float = 0.5 * self.x * sqrt(2)

        # self.numRx = int(sqrt(self.p * self.n))
        # self.dr = x / self.numRx
        # %%%%%%%%%%%%%%%%%%%%%%%%% END OF PARAMETERS %%%%%%%%%%%%%%%%%%%%%%%%


def start(n):
    myModel = Model(n)
    return myModel
