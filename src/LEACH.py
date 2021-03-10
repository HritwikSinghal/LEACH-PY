import pprint

from src import LEACH_configure_sensors
from src import LEACH_plotter
from src import LEACH_select_ch
from src import LEACH_set_parameters
from src import create_random_sensors
from src import dis_to_sink
from src import findReceiver
from src import find_sender
from src import join_to_nearest_ch
from src import reset_sensors
from src import send_receive_packets


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


class LEACHSimulation:

    def __init__(self, n=200):
        self.n = n  # Number of Nodes in the field

        # ########################################################
        # ############# For set_init_param_for_nodes #############
        # ########################################################
        self.deadNum = 0  # Number of dead nodes
        self.countCHs = 0  # counter for CHs

        # #########################################
        # ############# For start_sim #############
        # #########################################
        # counter for bit transmitted to Bases Station and Cluster Heads
        self.srp = 0  # counter number of sent routing packets
        self.rrp = 0  # counter number of receive routing packets
        self.sdp = 0  # counter number of sent data packets to sink
        self.rdp = 0  # counter number of receive data packets by sink
        self.x = 0

        # ########################################################
        # ############# For initialization_main_loop #############
        # ########################################################
        self.packets_to_base_station = 0

        # ##################################################
        # ############# For steady_state_phase #############
        # ##################################################
        # This section Operate for each epoch
        self.member = []  # Member of each cluster in per period      # Not used
        self.countCHs = 0  # Number of CH in per period               # Not Used

    def start(self):
        print("#################################")
        print("############# Start #############")
        print("#################################")
        print()

        # #################################################################
        # ############# Set Initial Parameters for Simulation #############
        # #################################################################
        self.__set_init_param_for_simulation()

        # #############################################
        # ############# configure Sensors #############
        # #############################################
        self.__conf_sen()

        # ########################################
        # ############# plot Sensors #############
        # ########################################
        # todo: Plot sensors Here
        # self.myplot = LEACH_plotter.start(self.Sensors, self.Model, self.deadNum)

        # ############################################################
        # ############# Set Initial Parameters for Nodes #############
        # ############################################################
        self.__set_init_param_for_nodes()

        # ############################################
        # ############# Start Simulation #############
        # ############################################
        self.__start_simulation()

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

    def __set_init_param_for_simulation(self):
        print("#################################################################")
        print("############# Set Initial Parameters for Simulation #############")
        print("#################################################################")
        print()

        # Create sensor nodes, Set Parameters and Create Energy Model
        self.myArea, self.myModel = LEACH_set_parameters.start(self.n)  # Set Parameters self.Sensors and Network

        # todo: test
        print("self.myArea")
        print(vars(self.myArea))
        print("self.myModel")
        print(vars(self.myModel))
        print("self.total_energy_dissipated", self.total_energy_dissipated)
        print("self.Sum_DEAD", self.Sum_DEAD)
        print("self.CLUSTERHS", self.CLUSTERHS)
        print("self.AllSensorEnergy", self.AllSensorEnergy)
        print('----------------------------------------------')

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

        # todo: test
        print("Sensors X co-ordinates:")
        pp(self.X)
        print("Sensors Y co-ordinates:")
        pp(self.Y)
        print()
        var_pp(self.Sensors)
        print('----------------------------------------------')

    def __set_init_param_for_nodes(self):
        print('############################################################')
        print('############# Set Initial Parameters for Nodes #############')
        print('############################################################')
        print()

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

        # todo: test
        print("self.initEnergy", self.initEnergy)
        print("self.SRP", self.SRP)
        print("len(self.SRP)", len(self.SRP))
        print("self.RRP", self.RRP)
        print("self.SDP", self.SDP)
        print("self.RDP", self.RDP)
        print('----------------------------------------------')

    def __start_simulation(self):
        print("############################################")
        print("############# Start Simulation #############")
        print("############################################")
        print()

        self.srp = 0  # counter of number of sent routing packets
        self.rrp = 0  # counter of number of receive routing packets
        self.sdp = 0  # counter of number of sent data packets
        self.rdp = 0  # counter of number of receive data packets

        # #######################################################################
        # ############# Sink broadcast 'Hello' message to all nodes #############
        # #######################################################################
        print("#######################################################################")
        print("############# Sink broadcast 'Hello' message to all nodes #############")
        print("#######################################################################")
        print()

        self.sender = [self.n]  # List of senders, for start_sim, sink will send hello packet to all
        self.receivers = [x for x in range(self.n)]  # List of senders, for start_sim, All nodes will receive from sink

        # todo: test
        print("Senders: ", end='')
        pp(self.sender)
        print("Receivers: ", end='')
        pp(self.receivers)
        print()

        self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
            self.Sensors, self.myModel, self.sender, 'Hello', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
        )

        # todo: test
        print("self.srp", self.srp)
        print("self.rrp", self.rrp)
        print("self.sdp", self.sdp)
        print("self.rdp", self.rdp)
        print("Sensors: ", )
        var_pp(self.Sensors)

        # Save metrics, Round 0 is initialization phase where all nodes send routing packets (hello) to Sink as above
        self.SRP[0] = self.srp
        self.RRP[0] = self.rrp
        self.SDP[0] = self.sdp
        self.RDP[0] = self.rdp

        # todo: test
        print('self.SRP', self.SRP)
        print('self.RRP', self.RRP)
        print('self.SDP', self.SDP)
        print('self.RDP', self.RDP)

        # #########################################################################
        # ############# Find All sensors distance from Sink #############
        # #########################################################################
        print("###############################################################")
        print("############# Find All sensors distance from Sink #############")
        print("###############################################################")
        print()

        dis_to_sink.start(self.Sensors, self.myModel)

        # todo: test
        print("Sensors: ", )
        var_pp(self.Sensors)
        print('----------------------------------------------')

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
            # ############# Plot network status in end of set-up phase #############
            # ######################################################################
            print("######################################################################")
            print("############# Plot network status in end of set-up phase #############")
            print("######################################################################")
            print()

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

            # # Todo: done till here
            # exit()

            # ######################################
            # ############# STATISTICS #############
            # ######################################

            # Used in Statistics
            self.total_energy_dissipated = zeros(1, self.myModel.rmax)
            self.Sum_DEAD = zeros(1, self.myModel.rmax)
            self.CLUSTERHS = zeros(1, self.myModel.rmax)
            self.AllSensorEnergy = zeros(1, self.myModel.rmax)
            self.AliveSensors = zeros(1, self.myModel.rmax)
            self.SumEnergyAllSensor = zeros(1, self.myModel.rmax)
            self.AvgEnergyAllSensor = zeros(1, self.myModel.rmax)
            self.ConsumEnergy = zeros(1, self.myModel.rmax)
            self.Enheraf = zeros(1, self.myModel.rmax)

            self.Sum_DEAD[round_number] = self.deadNum

            self.SRP[round_number] = self.srp
            self.RRP[round_number] = self.rrp
            self.SDP[round_number] = self.sdp
            self.RDP[round_number] = self.rdp

            self.CLUSTERHS[round_number] = self.countCHs

            alive = 0
            SensorEnergy = 0
            for i in range(self.n):
                if self.Sensors[i].E > 0:
                    alive += 1
                    SensorEnergy += self.Sensors[i].E

            self.AliveSensors[round_number] = alive  # ok
            self.SumEnergyAllSensor[round_number] = SensorEnergy  # #ok

            self.AvgEnergyAllSensor[round_number] = SensorEnergy / alive  # #ok
            self.ConsumEnergy[round_number] = (self.initEnergy - self.SumEnergyAllSensor[round_number]) / self.n  # #ok

            En = 0
            for i in range(self.n):
                if self.Sensors[i].E > 0:
                    En += pow((self.Sensors[i].E - self.AvgEnergyAllSensor[round_number]), 2)

            self.Enheraf[round_number] = En / alive  # #ok

            # todo: maybe this is related to graph
            # title(sprintf('Round=##d,Dead nodes=##d', round_number, deadNum))

            # dead
            if self.n == self.deadNum:
                self.lastPeriod = round_number
                break

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

        reset_sensors.start(self.Sensors, self.myModel)

        # todo: test
        print("\n\nAfter Reset")
        print('self.SRP', self.SRP)
        print('self.RRP', self.RRP)
        print('self.SDP', self.SDP)
        print('self.RDP', self.RDP)
        print("Sensors: ", )
        var_pp(self.Sensors)

        # allow to sensor to become cluster-head. LEACH Algorithm
        self.AroundClear = 1 / self.myModel.p  # After every "AroundClear" rounds, let every sensor be CH again
        if r % self.AroundClear == 0:
            for sensor in self.Sensors:
                sensor.G = 0

        # todo: test
        print("\n\nAfter: allow sensor to become CH")
        print("Sensors: ", )
        var_pp(self.Sensors)

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
        # updates dist2ch & MCH in node
        join_to_nearest_ch.start(self.Sensors, self.myModel, self.list_CH)

        # todo: test
        print("\nSensors:")
        var_pp(self.Sensors)
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
            self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                self.Sensors, self.myModel, [ch_id], 'Hello', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
            )

            # todo: test
            print("self.srp", self.srp)
            print("self.rrp", self.rrp)
            print("self.sdp", self.sdp)
            print("self.rdp", self.rdp)
            print("Sensors: ", )
            var_pp(self.Sensors)
            print()

    def __steady_state_phase(self):
        print('##############################################')
        print('############# steady state phase #############')
        print('##############################################')
        print()

        self.NumPacket = self.myModel.NumPacket  # Number of Packets sent in steady-state phase
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

                # todo: test
                print("sender: ", sender)
                print("receiver: ", receiver)

                self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                    self.Sensors, self.myModel, sender, 'Data', [receiver], self.srp, self.rrp, self.sdp, self.rdp
                )

                # todo: test
                print("self.srp", self.srp)
                print("self.rrp", self.rrp)
                print("self.sdp", self.sdp)
                print("self.rdp", self.rdp)
                print("Sensors: ", )
                var_pp(self.Sensors)
                print()

        # ###################################################################################
        # ############# Send Data packet from CH to Sink after Data aggregation #############
        # ###################################################################################
        print('###################################################################################')
        print('############# Send Data packet from CH to Sink after Data aggregation #############')
        print('###################################################################################')
        print()

        for sender in self.list_CH:
            self.receivers = [self.n]  # Sink

            # todo: test
            print("sender: ", sender)
            print("receiver: ", self.receivers)

            self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                self.Sensors, self.myModel, [sender], 'Data', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
            )

            # todo: test
            print("self.srp", self.srp)
            print("self.rrp", self.rrp)
            print("self.sdp", self.sdp)
            print("self.rdp", self.rdp)
            print("Sensors: ", )
            var_pp(self.Sensors)
            print()

        # ###########################################################################################################
        # ############# send Data packet directly from other nodes(that aren't in each cluster) to Sink #############
        # ###########################################################################################################
        for sensor in self.Sensors:
            if sensor.MCH == self.n:  # if it is sink
                self.receivers = [self.n]  # Sink
                sender = [sensor.id]  # Other Nodes
                self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                    self.Sensors, self.myModel, sender, 'Data', self.receivers, self.srp, self.rrp, self.sdp, self.rdp
                )
