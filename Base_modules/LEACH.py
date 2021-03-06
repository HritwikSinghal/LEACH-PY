from Base_modules import LEACH_configureSensors
from Base_modules import LEACH_selectCH
from Base_modules import LEACH_setParameters
from Base_modules import createRandomSen
from Base_modules import disToSink
from Base_modules import findReceiver
from Base_modules import findSender
from Base_modules import joinToNearestCH
from Base_modules import resetSensors
from Base_modules import sendReceivePackets

################################################################
# todo :test
import pprint


def var_pp(stuff):
    pp = pprint.PrettyPrinter(indent=1)
    for x in stuff:
        pp.pprint(vars(x))


def pp(stuff):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(stuff)


################################################################
class ILEACH:

    def __init__(self, n=200):
        # Create sensor nodes, Set Parameters and Create Energy self.Model
        # ######################### Initial Parameters #######################
        self.n = n  # #Number of Nodes in the field
        self.myArea, self.Model = LEACH_setParameters.setParameters(self.n)  # Set Parameters self.Sensors and Network

        # todo: test
        print(vars(self.myArea))
        print(vars(self.Model))
        print('----------------------------------------------')

        # ######################### configuration Sensors ####################
        self.conf_sen()

        # todo: test
        pp(self.X)
        pp(self.Y)
        var_pp(self.Sensors)
        print('----------------------------------------------')

        # todo: Plot sensors Here
        # self.myplot = LEACH_plotter.start(self.Sensors, self.Model, self.deadNum)

        # ################# Parameters initialization #############
        self.init_param()

        # todo: test
        print("self.initEnergy: ", self.initEnergy)
        print("self.SRP", self.SRP)
        print("len(self.SRP)", len(self.SRP))
        print(self.RRP)
        print(self.SDP)
        print(self.RDP)
        print('----------------------------------------------')
        exit()

        # ############# Start Simulation ##############
        self.start_sim(n)

        # Main loop program
        self.main_loop()

    def conf_sen(self):
        # ######################### configuration Sensors ####################
        # Create a random scenario & Load sensor Location
        self.X, self.Y = createRandomSen.start(self.Model, self.myArea)

        # configure sensors
        self.Sensors = LEACH_configureSensors.start(self.Model, self.n, self.X, self.Y)
        # self.deadNum = 0  # Number of dead nodes

    def init_param(self):
        # ################# Parameters initialization #############
        self.countCHs = 0  # counter for CHs
        self.flag_first_dead = 0  # flag_first_dead
        self.deadNum = 0  # Number of dead nodes

        self.initEnergy = 0  # Initial Energy
        for sensor in self.Sensors:
            self.initEnergy += sensor.E

        self.SRP = self.zeros(1, self.Model.rmax)  # number of sent routing packets
        self.RRP = self.zeros(1, self.Model.rmax)  # number of receive routing packets
        self.SDP = self.zeros(1, self.Model.rmax)  # number of sent data packets
        self.RDP = self.zeros(1, self.Model.rmax)  # number of receive data packets

        # total_energy_dissipated = zeros(1,Model.rmax)
        self.Sum_DEAD = self.zeros(1, self.Model.rmax)
        self.CLUSTERHS = self.zeros(1, self.Model.rmax)
        self.AllSensorEnergy = self.zeros(1, self.Model.rmax)

    def zeros(self, row, column):
        re_list = []
        for x in range(row):
            temp_list = [0 for _ in range(column)]
            if row == 1:
                re_list.extend(temp_list)
            else:
                re_list.append(temp_list)

        return re_list

    def start_sim(self, n):
        # ############# Start Simulation ##############
        self.srp = 0  # #counter number of sent routing packets
        self.rrp = 0  # #counter number of receive routing packets
        self.sdp = 0  # #counter number of sent data packets
        self.rdp = 0  # #counter number of receive data packets

        # Sink broadcast start message to all nodes
        self.Sender = self.n + 1  # Sink
        self.Receiver = [x for x in range(n)]  # All nodes
        self.Sensors = sendReceivePackets.start(self.Sensors, self.Model, self.Sender, 'Hello', self.Receiver)

        # All sensors location information to Sink .
        disToSink.start(self.Sensors, self.Model)

        # #Save metrics
        self.SRP[1] = self.srp
        self.RRP[1] = self.rrp
        self.SDP[1] = self.sdp
        self.RDP[1] = self.rdp

        self.x = 0

    def main_loop(self):
        for r in range(self.Model.rmax):

            # ####### Initialization #######

            # This section Operate for each epoch
            self.member = []  # Member of each cluster in per period
            self.countCHs = 0  # Number of CH in per period

            # #counter for bit transmitted to Bases Station and Cluster Heads
            self.srp = 0  # counter number of sent routing packets
            self.rrp = 0  # counter number of receive routing packets
            self.sdp = 0  # counter number of sent data packets to sink
            self.rdp = 0  # counter number of receive data packets by sink

            # #initialization per round
            self.SRP[r + 1] = self.srp
            self.RRP[r + 1] = self.rrp
            self.SDP[r + 1] = self.sdp
            self.RDP[r + 1] = self.rdp

            # pause(0.001)  # pause simulation
            # hold off      # clear figure

            # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # self.packets_TO_BS = 0

            resetSensors.start(self.Sensors, self.Model)
            # #allow to sensor to become cluster-head. LEACH Algorithm
            self.AroundClear = 10
            if r % self.AroundClear == 0:
                for i in range(self.n):
                    self.Sensors[i].G = 0

            # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% plot Sensors %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # todo: plot here
            # self.deadNum, self.circlex, self.circley = LEACH_plotter.start(self.Sensors, self.Model)

            # #Save r'th period When the first node dies
            if (self.deadNum >= 1) and (self.flag_first_dead == 0):
                self.first_dead = r
                self.flag_first_dead = 1

            # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% cluster head election %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            # Selection Candidate Cluster Head Based on LEACH Set-up Phase
            # todo: fix this
            self.TotalCH = LEACH_selectCH.start(self.Sensors, self.Model, r, self.circlex, self.circley)

            # #Broadcasting CHs to All Sensor that are in Radio Rage CH.
            for i in range(len(self.TotalCH)):
                self.Sender = self.TotalCH[i].id
                SenderRR = self.Model.RR
                self.Receiver = findReceiver.start(self.Sensors, self.Model, self.Sender, SenderRR)
                sendReceivePackets.start(self.Sensors, self.Model, self.Sender, 'Hello', self.Receiver,
                                         self.srp, self.rrp, self.sdp, self.rdp)

            # #Sensors join to nearest CH
            joinToNearestCH.start(self.Sensors, self.Model, self.TotalCH)

            # %%%%%%%%%%%%%%%%%%%%%%% end of cluster head election phase %%%%%%

            # %%%%%%%%%%%%%%%%%%%%%%% plot network status in end of set-up phase
            # %%%%%%%%%%%%%%%%%%%%%%% this will draw lines from every node to its CH

            # %     for i=1:n
            # %
            # %         if (Sensors(i).type=='N' && Sensors(i).dis2ch<Sensors(i).dis2sink && ...
            # %                 Sensors(i).E>0)
            # %
            # %             XL=[Sensors(i).xd ,Sensors(Sensors(i).MCH).xd];
            # %             YL=[Sensors(i).yd ,Sensors(Sensors(i).MCH).yd];
            # %             hold on
            # %             line(XL,YL)

            # ######## steady-state phase ######
            self.NumPacket = self.Model.NumPacket
            for i in range(1):  # NumPacket
                # todo: Plotter
                # [deadNumo, circlex, circley] = LEACH_plotter.start(self.Sensors, self.Model)

                # ######## All sensor s data packet to  CH
                for j in range(len(self.TotalCH)):
                    self.Receiver = self.TotalCH(j).id
                    findSender.start(self.Sensors, self.Model, self.Receiver)
                    self.Sensors = sendReceivePackets.start(self.Sensors, self.Model, self.Sender, 'Data',
                                                            self.Receiver)

            # ### send Data packet from CH to Sink after Data aggregation
            for i in range(len(self.TotalCH)):
                self.Receiver = self.n + 1  # #Sink
                Ser = self.TotalCH[i].id  # #CH
                self.Sensors = sendReceivePackets.start(self.Sensors, self.Model, self.Sender, 'Data', self.Receiver)

            # send Data packet directly from other nodes(that aren't in each cluster) to Sink
            for i in range(self.n):
                if self.Sensors[i].MCH == self.Sensors[n + 1].id:
                    self.Receiver = self.n + 1  # #Sink
                    Ser = self.Sensors(i).id  # #Other Nodes
                    self.Sensors = sendReceivePackets.start(self.Sensors, self.Model, self.Sender, 'Data',
                                                            self.Receiver)

            ## Todo: STATISTICS

            # Sum_DEAD(r + 1) = deadNum
            #
            # SRP(r + 1) = srp
            # RRP(r + 1) = rrp
            # SDP(r + 1) = sdp
            # RDP(r + 1) = rdp
            #
            # CLUSTERHS(r + 1) = countCHs
            #
            # alive = 0
            # SensorEnergy = 0
            # for i=1:n
            # if self.Sensors(i).E > 0
            #     alive = alive + 1
            #     SensorEnergy = SensorEnergy + self.Sensors(i).E
            #
            # AliveSensors(r) = alive  # #ok
            #
            # SumEnergyAllSensor(r + 1) = SensorEnergy  # #ok
            #
            # AvgEnergyAllSensor(r + 1) = SensorEnergy / alive  # #ok
            #
            # ConsumEnergy(r + 1) = (initEnergy - SumEnergyAllSensor(r + 1)) / n  # #ok
            #
            # En = 0
            # for i=1:n
            # if self.Sensors(i).E > 0
            #     En = En + (Sensors(i).E - AvgEnergyAllSensor(r + 1)) ^ 2
            #
            # Enheraf(r + 1) = En / alive  # #ok
            #
            # title(sprintf('Round=##d,Dead nodes=##d', r + 1, deadNum))
            #
            # # #dead
            # if (n == deadNum)
            #
            #     lastPeriod = r
            #     break


if __name__ == '__main__':
    myleach = ILEACH(n=5)
