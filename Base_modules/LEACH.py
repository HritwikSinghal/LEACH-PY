import pprint

from Base_modules import LEACH_configure_sensors
from Base_modules import LEACH_plotter
from Base_modules import LEACH_select_ch
from Base_modules import LEACH_set_parameters
from Base_modules import create_random_sensors
from Base_modules import dis_to_sink
from Base_modules import findReceiver
from Base_modules import find_sender
from Base_modules import join_to_nearest_ch
from Base_modules import reset_sensors
from Base_modules import send_receive_packets


# #################################################
# todo :test, for debugging


def var_pp(stuff):
    pp = pprint.PrettyPrinter(indent=1)
    for x in stuff:
        pp.pprint(vars(x))


def pp(stuff):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(stuff)


# #################################################

def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


class LEACH:

    def __init__(self, n=200):
        self.AroundClear = 1 / self.myModel.p  # After every "AroundClear" rounds, let every sensor be CH again
        self.n = n  # Number of Nodes in the field

        self.deadNum = 0  # Number of dead nodes

        # counter for bit transmitted to Bases Station and Cluster Heads
        self.srp = 0  # counter number of sent routing packets
        self.rrp = 0  # counter number of receive routing packets
        self.sdp = 0  # counter number of sent data packets to sink
        self.rdp = 0  # counter number of receive data packets by sink

        # This section Operate for each epoch
        self.member = []  # Member of each cluster in per period      # Not used
        self.countCHs = 0  # Number of CH in per period               # Not Used

        self.NumPacket = self.myModel.NumPacket  # Number of Packets sent in steady-state phase

    def start(self):

        # ##################################################
        # ############# Set Initial Parameters #############
        # ##################################################
        self.__set_init_param()

        # todo: test
        print("self.myArea")
        print(vars(self.myArea))
        print("self.myModel")
        print(vars(self.myModel))
        print('----------------------------------------------')

        # #############################################
        # ############# configure Sensors #############
        # #############################################
        self.__conf_sen()

        # todo: test
        print("Sensors X co-ordinates:")
        pp(self.X)
        print("Sensors Y co-ordinates:")
        pp(self.Y)
        print()
        var_pp(self.Sensors)
        print('----------------------------------------------')

        # ########################################
        # ############# plot Sensors #############
        # ########################################
        # todo: Plot sensors Here
        # self.myplot = LEACH_plotter.start(self.Sensors, self.Model, self.deadNum)

        # #####################################################
        # ############# Parameters initialization #############
        # #####################################################
        self.__init_param()

        # todo: test
        print("self.initEnergy", self.initEnergy)
        print("self.SRP", self.SRP)
        print("len(self.SRP)", len(self.SRP))
        print("self.RRP", self.RRP)
        print("self.SDP", self.SDP)
        print("self.RDP", self.RDP)
        print("self.Sum_DEAD", self.Sum_DEAD)
        print("self.CLUSTERHS", self.CLUSTERHS)
        print("self.AllSensorEnergy", self.AllSensorEnergy)
        print('----------------------------------------------')

        # ############################################
        # ############# Start Simulation #############
        # ############################################
        self.__start_sim(self.n)

        # todo: test
        print("self.Sender", self.sender)
        print("self.receivers ", end='')
        pp(self.receivers)
        var_pp(self.Sensors)
        print('self.srp', self.srp)
        print('self.rrp', self.rrp)
        print('self.sdp', self.sdp)
        print('self.rdp', self.rdp)
        print('----------------------------------------------')

        # #############################################
        # ############# Main loop program #############
        # #############################################
        self.__main_loop()

        # ##############################################
        # ############# END of simulation ##############
        # ##############################################
        print('-------------------- XXX --------------------')
        print('############# END of simulation #############')
        print('-------------------- XXX --------------------')

    def __set_init_param(self):
        print("##################################################")
        print("############# Set Initial Parameters #############")
        print("##################################################")
        print()

        # Create sensor nodes, Set Parameters and Create Energy Model
        self.myArea, self.myModel = LEACH_set_parameters.start(self.n)  # Set Parameters self.Sensors and Network

    def __conf_sen(self):
        print("#############################################")
        print("############# configure Sensors #############")
        print("#############################################")
        print()

        '''
        This will set random X and Y coord for each sensor and store it in X, Y
        And then it will initialize other parameters also.
        '''

        # Create a random scenario & Load sensor Location
        self.X, self.Y = create_random_sensors.start(self.myModel, self.myArea)

        # configure sensors
        self.Sensors = LEACH_configure_sensors.start(self.myModel, self.n, self.X, self.Y)

    def __init_param(self):
        print('#####################################################')
        print('############# Parameters initialization #############')
        print('#####################################################')
        print()

        # self.countCHs = 0  # counter for CHs      # Declared in __init__
        self.flag_first_dead = 0  # flag_first_dead
        self.deadNum = 0  # Number of dead nodes

        self.initEnergy = 0  # Initial Energy
        for sensor in self.Sensors:
            self.initEnergy += sensor.E

        # Below will be of length(Max_rounds) so each element will store the total packets in each round
        # the length is rmax + 1 since we take one initialization round also.
        self.SRP = zeros(1, self.myModel.rmax + 1)  # number of sent routing packets
        self.RRP = zeros(1, self.myModel.rmax + 1)  # number of receive routing packets
        self.SDP = zeros(1, self.myModel.rmax + 1)  # number of sent data packets
        self.RDP = zeros(1, self.myModel.rmax + 1)  # number of receive data packets

        # total_energy_dissipated = zeros(1,Model.rmax)
        self.Sum_DEAD = zeros(1, self.myModel.rmax)
        self.CLUSTERHS = zeros(1, self.myModel.rmax)
        self.AllSensorEnergy = zeros(1, self.myModel.rmax)

    def __start_sim(self, n):
        print("############################################")
        print("############# Start Simulation #############")
        print("############################################")
        print()

        self.srp = 0  # counter of number of sent routing packets
        self.rrp = 0  # counter of number of receive routing packets
        self.sdp = 0  # counter of number of sent data packets
        self.rdp = 0  # counter of number of receive data packets

        # Sink broadcast 'Hello' message to all nodes
        self.sender = [self.n]  # List of senders, for start_sim, sink will send hello packet to all
        self.receivers = [x for x in range(n)]  # List of senders, for start_sim, All nodes will receive from sink

        self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
            self.Sensors, self.myModel, self.sender, 'Hello', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
        )

        # All sensors location information to Sink .
        dis_to_sink.start(self.Sensors, self.myModel)

        # Save metrics
        self.SRP[0] = self.srp
        self.RRP[0] = self.rrp
        self.SDP[0] = self.sdp
        self.RDP[0] = self.rdp

        self.x = 0

    def __main_loop(self):
        print("#############################################")
        print("############# Main loop program #############")
        print("#############################################")
        print()

        for round_number in range(1, self.myModel.rmax + 1):
            # ##########################################
            # ############# Initialization #############
            # ##########################################
            self.__initialization_main_loop(round_number)

            # ########################################
            # ############# plot Sensors #############
            # ########################################
            self.deadNum, self.circlex, self.circley = LEACH_plotter.start(self.Sensors, self.myModel)

            # Save the period in which the first node died
            if self.deadNum > 0 and self.flag_first_dead == 0:
                self.first_dead = round_number
                self.flag_first_dead = 1

            # #################################################
            # ############# cluster head election #############
            # #################################################
            self.__cluster_head_selection_phase(round_number)

            # ######################################################################
            # ############# plot network status in end of set-up phase #############
            # ######################################################################
            # this will draw lines from every node to its CH

            #      for i=1:n
            #
            #          if (Sensors(i).type=='N' && Sensors(i).dis2ch<Sensors(i).dis2sink && ...
            #                  Sensors(i).E>0)
            #
            #              XL=[Sensors(i).xd ,Sensors(Sensors(i).MCH).xd];
            #              YL=[Sensors(i).yd ,Sensors(Sensors(i).MCH).yd];
            #              hold on
            #              line(XL,YL)

            '''
            What has been done till now:
            All Ch are elected 
            All nodes know which CH they should send to
            
            Whats Todo:
            Start steady state phase
            '''

            # ##############################################
            # ############# steady-state phase #############
            # ##############################################
            self.__steady_state_phase()

            # todo: test
            print()

            # Todo: done till here
            exit()

            # ######################################
            # ############# STATISTICS #############
            # ######################################

            # Todo: STATISTICS

            # Sum_DEAD(round_number) = deadNum
            #
            # SRP(round_number) = srp
            # RRP(round_number) = rrp
            # SDP(round_number) = sdp
            # RDP(round_number) = rdp
            #
            # CLUSTERHS(round_number) = countCHs
            #
            # alive = 0
            # SensorEnergy = 0
            # for i=1:n
            # if self.Sensors(i).E > 0
            #     alive = alive + 1
            #     SensorEnergy = SensorEnergy + self.Sensors(i).E
            #
            # AliveSensors(round_number) = alive  # #ok
            #
            # SumEnergyAllSensor(round_number) = SensorEnergy  # #ok
            #
            # AvgEnergyAllSensor(round_number) = SensorEnergy / alive  # #ok
            #
            # ConsumEnergy(round_number) = (initEnergy - SumEnergyAllSensor(round_number)) / n  # #ok
            #
            # En = 0
            # for i=1:n
            # if self.Sensors(i).E > 0
            #     En = En + (Sensors(i).E - AvgEnergyAllSensor(round_number)) ^ 2
            #
            # Enheraf(round_number) = En / alive  # #ok
            #
            # title(sprintf('Round=##d,Dead nodes=##d', round_number, deadNum))
            #
            # # #dead
            # if (n == deadNum)
            #
            #     lastPeriod = round_number
            #     break

    def __initialization_main_loop(self, r):
        print('####################################################')
        print('############# Main loop Initialization #############')
        print('####################################################')
        print()

        # counter for bit transmitted to Bases Station and Cluster Heads
        self.srp = 0  # counter number of sent routing packets
        self.rrp = 0  # counter number of receive routing packets
        self.sdp = 0  # counter number of sent data packets to sink
        self.rdp = 0  # counter number of receive data packets by sink

        # initialization per round
        self.SRP[r] = self.srp
        self.RRP[r] = self.rrp
        self.SDP[r] = self.sdp
        self.RDP[r] = self.rdp

        # ##################################################
        # self.packets_to_base_station = 0
        # ##################################################

        reset_sensors.start(self.Sensors, self.myModel)

        # allow to sensor to become cluster-head. LEACH Algorithm
        if r % self.AroundClear == 0:
            for sensor in self.Sensors:
                sensor.G = 0

    def __cluster_head_selection_phase(self, r):
        print('#################################################')
        print('############# cluster head election #############')
        print('#################################################')
        print()

        # Selection Candidate Cluster Head Based on LEACH Set-up Phase
        # self.list_CH stores the id of all CH in current round
        self.list_CH = LEACH_select_ch.start(self.Sensors, self.myModel, r, self.circlex, self.circley)

        # todo: test
        print('self.list_CH: ', end='')
        pp(self.list_CH)
        print()

        # #####################################################################################
        # ############# Broadcasting CHs to All Sensors that are in Radio Rage CH #############
        # #####################################################################################
        self.__broadcast_cluster_head()

        # ######################################################
        # ############# Sensors join to nearest CH #############
        # ######################################################
        join_to_nearest_ch.start(self.Sensors, self.myModel, self.list_CH)

        # todo: test
        print("\nSensors:")
        var_pp(self.Sensors)
        print()
        print("\nModel:")
        print(vars(self.myModel))
        print()

        # ########################################
        # ############# plot Sensors #############
        # ########################################
        # Todo: plot here

        # ##############################################################
        # ############# end of cluster head election phase #############
        # ##############################################################

        print('##############################################################')
        print('############# end of cluster head election phase #############')
        print('##############################################################')

    def __broadcast_cluster_head(self):
        print('#####################################################################################')
        print('############# Broadcasting CHs to All Sensors that are in Radio Rage CH #############')
        print('#####################################################################################')
        print()

        # Broadcasting CH x to All Sensors that are in Radio Rage of x.
        # Doing this for all CH
        for ch_id in self.list_CH:
            senderRR = self.myModel.RR  # Radio range of sender
            self.receivers: list = findReceiver.start(self.Sensors, self.myModel, ch_id, senderRR)

            # todo: test
            print("sender: ", ch_id)
            print('self.Receivers: ', end='')
            print(self.receivers)

            # we require the sender parameter of sendReceivePackets.start to be a list.
            send_receive_packets.start(
                self.Sensors, self.myModel, [ch_id], 'Hello', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
            )

    def __steady_state_phase(self):
        print('##############################################')
        print('############# steady state phase #############')
        print('##############################################')
        print()

        # changed from 1 to self.myModel.NumPacket
        for i in range(self.NumPacket):  # Number of Packets sent in steady-state phase

            # ########################################
            # ############# plot Sensors #############
            # ########################################
            # todo: Plot here
            # [deadNumo, circlex, circley] = LEACH_plotter.start(self.Sensors, self.Model)

            # #############################################################
            # ############# All sensor send data packet to CH #############
            # #############################################################
            print('#############################################################')
            print('############# All sensor send data packet to CH #############')
            print('#############################################################')
            print()

            for receiver in self.list_CH:
                sender = find_sender.start(self.Sensors, receiver)
                send_receive_packets.start(
                    self.Sensors, self.myModel, sender, 'Data', [receiver], self.srp, self.rrp, self.sdp, self.rdp
                )

        # ###################################################################################
        # ############# Send Data packet from CH to Sink after Data aggregation #############
        # ###################################################################################
        print('###################################################################################')
        print('############# Send Data packet from CH to Sink after Data aggregation #############')
        print('###################################################################################')
        print()

        for sender in self.list_CH:
            self.receivers = [self.n]  # Sink
            send_receive_packets.start(
                self.Sensors, self.myModel, [sender], 'Data', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
            )

        # ###########################################################################################################
        # ############# send Data packet directly from other nodes(that aren't in each cluster) to Sink #############
        # ###########################################################################################################
        for sensor in self.Sensors:
            if sensor.MCH == self.Sensors[self.n].id:  # if it is sink
                self.receivers = [self.n]  # #Sink
                sender = [sensor.id]  # Other Nodes
                send_receive_packets.start(
                    self.Sensors, self.myModel, sender, 'Data', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
                )
