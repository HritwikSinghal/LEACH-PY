from Base_modules import create_rand_sim
from Base_modules import set_param
from Base_modules import plot_ileach
from Base_modules import configure_sen
from Base_modules import send_rec_pak
from Base_modules import dist_to_sink
from Base_modules import reset_sen
from Base_modules import select_CH
from math import *


class ILEACH:

    def __init__(self, n=200):
        # Create sensor nodes, Set Parameters and Create Energy self.Model
        # ######################### Initial Parameters #######################

        self.n = n  # #Number of Nodes in the field
        self.Model, self.myArea = set_param.setParameters(self.n)  # #Set Parameters self.Sensors and Network

        self.conf_sen()
        self.init_param()
        self.start_sim(n)
        self.start()

    def zeros(self, row, column):
        re_list = []
        for x in range(row):
            temp_list = [0 for _ in range(column)]
            re_list.app(temp_list)

        return re_list

    def conf_sen(self):
        # ######################### configuration Sensors ####################
        # Create a random scenario & Load sensor Location
        self.X, self.Y = create_rand_sim.start(self.Model, self.myArea)
        # configure sensors
        self.Sensors = configure_sen.start(self.Model, self.n, self.X, self.Y)
        self.deadNum = 0  # Number of dead nodes
        self.myplot = plot_ileach.start(self.Sensors, self.Model, self.deadNum)

    def init_param(self):
        # ################# Parameters initialization #############
        self.countCHs = 0  # counter for CHs
        self.flag_first_dead = 0  # flag_first_dead
        self.initEnergy = 0  # #Initial Energy
        for i in range(self.n):
            self.initEnergy = self.Sensors[i] + self.initEnergy
        self.SRP = self.zeros(1, self.Model.rmax)  # #number of sent routing packets
        self.RRP = self.zeros(1, self.Model.rmax)  # #number of receive routing packets
        self.SDP = self.zeros(1, self.Model.rmax)  # #number of sent data packets
        self.RDP = self.zeros(1, self.Model.rmax)  # #number of receive data packets
        # total_energy_disipated=zeros(1,Model.rmax)
        self.Sum_DEAD = self.zeros(1, self.Model.rmax)
        self.CLUSTERHS = self.zeros(1, self.Model.rmax)
        self.AllSensorEnergy = self.zeros(1, self.Model.rmax)

    def start_sim(self, n):
        # ############# Start Simulation ##############
        self.srp = 0  # #counter number of sent routing packets
        self.rrp = 0  # #counter number of receive routing packets
        self.sdp = 0  # #counter number of sent data packets
        self.rdp = 0  # #counter number of receive data packets
        # Sink broadcast start message to all nodes
        self.Sender = self.n + 1  # Sink
        self.Receiver = [x for x in range(n)]  # All nodes

        self.Sensors = send_rec_pak.SendReceivePackets(
            self.Sensors, self.Model, self.Sender, 'Hello', self.Receiver
        )

        # # All sensor s location information to Sink .
        self.Sensors = dist_to_sink.disToSink(self.Sensors, self.Model)

        # #Save metrics
        self.SRP[1] = self.srp
        self.RRP[1] = self.rrp
        self.SDP[1] = self.sdp
        self.RDP[1] = self.rdp

        self.x = 0

    def start(self):
        for r in range(self.Model.rmax):

            # ####### Initialization #######

            # This section Operate for each epoch
            self.member = []  # #Member of each cluster in per period
            self.countCHs = 0  # #Number of CH in per period

            # #counter for bit transmitted to Bases Station and Cluster Heads
            self.srp = 0  # #counter number of sent routing packets
            self.rrp = 0  # #counter number of receive routing packets
            self.sdp = 0  # #counter number of sent data packets to sink
            self.rdp = 0  # #counter number of receive data packets by sink

            # #initialization per round
            self.SRP[r + 1] = self.srp
            self.RRP[r + 1] = self.rrp
            self.SDP[r + 1] = self.sdp
            self.RDP[r + 1] = self.rdp

            # pause(0.001)  # #pause simulation
            # hold
            # off  # #clear figure

            self.packets_TO_BS = 0
            self.Sensors = reset_sen.resetSensors(self.Sensors, self.Model)

            # #allow to sensor to become cluster-head. LEACH Algorithm
            self.AroundClear = 10

            if r % self.AroundClear == 0:
                for i in range(self.n):
                    self.Sensors[i].G = 0

            # ####### plot self.Sensors #######
            self.deadNum, self.circlex, self.circley = plot_ileach.start(self.Sensors, self.Model)

            # #Save r'th period When the first node dies
            if (self.deadNum >= 1) and (self.flag_first_dead == 0):
                self.first_dead = r
                self.flag_first_dead = 1

            # ###### cluster head election ######
            # #Selection Candidate Cluster Head Based on LEACH Set-up Phase
            self.TotalCH, self.Sensors = select_CH.SelectCH(self.Sensors, self.Model, r, self.circlex, self.circley)

            # #Broadcasting CHs to All Sensor that are in Radio Rage CH.
            for i=1:length(TotalCH)

            Ser = TotalCH(i).id
            SerRR = self.Model.RR
            Receiver = findReceiver(Sensors, self.Model, Ser, SerRR)
            self.Sensors = SReceivePackets(Sensors, self.Model, Ser, 'Hello', Receiver)

            # #Sensors join to nearest CH
            self.Sensors = JoinToNearestCH(Sensors, self.Model, TotalCH)

            # ######  of cluster head election phase ###

            # ######## steady-state phase ######
            NumPacket = self.Model.NumPacket
            for i=1:1: 1  # #NumPacket 

            # #Plotter     
            [deadNumo, circlex, circley] = plot_ileach(Sensors, self.Model)

            # ######## All sensor s data packet to  CH 
            for j=1:length(TotalCH)

            Receiver = TotalCH(j).id
            Ser = findSer(Sensors, self.Model, Receiver)
            self.Sensors = SReceivePackets(Sensors, self.Model, Ser, 'Data', Receiver)

            # ### s Data packet from CH to Sink after Data aggregation
            for i=1:length(TotalCH)

            Receiver = n + 1  # #Sink
            Ser = TotalCH(i).id  # #CH 
            self.Sensors = SReceivePackets(Sensors, self.Model, Ser, 'Data', Receiver)

            # # s data packet directly from other nodes(that aren't in each cluster) to Sink
            for i=1:n
            if (Sensors(i).MCH == self.Sensors(n + 1).id)
                Receiver = n + 1  # #Sink
                Ser = self.Sensors(i).id  # #Other Nodes 
                self.Sensors = SReceivePackets(Sensors, self.Model, Ser, 'Data', Receiver)

            # # STATISTICS

            Sum_DEAD(r + 1) = deadNum

            SRP(r + 1) = srp
            RRP(r + 1) = rrp
            SDP(r + 1) = sdp
            RDP(r + 1) = rdp

            CLUSTERHS(r + 1) = countCHs

            alive = 0
            SensorEnergy = 0
            for i=1:n
            if self.Sensors(i).E > 0
                alive = alive + 1
                SensorEnergy = SensorEnergy + self.Sensors(i).E

            AliveSensors(r) = alive  # #ok

            SumEnergyAllSensor(r + 1) = SensorEnergy  # #ok

            AvgEnergyAllSensor(r + 1) = SensorEnergy / alive  # #ok

            ConsumEnergy(r + 1) = (initEnergy - SumEnergyAllSensor(r + 1)) / n  # #ok

            En = 0
            for i=1:n
            if self.Sensors(i).E > 0
                En = En + (Sensors(i).E - AvgEnergyAllSensor(r + 1)) ^ 2

            Enheraf(r + 1) = En / alive  # #ok

            title(sprintf('Round=##d,Dead nodes=##d', r + 1, deadNum))

            # #dead
            if (n == deadNum)

                lastPeriod = r
                break
