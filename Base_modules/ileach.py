from Base_modules import create_rand_sim
from Base_modules import set_param
from Base_modules import plot_ileach
from Base_modules import configure_sen
from Base_modules import send_rec_pak
from Base_modules import dist_to_sink

class ILEACH:

    def __init__(self, n=200):
        # Create sensor nodes, Set Parameters and Create Energy Model
        # ######################### Initial Parameters #######################

        self.n = n  # #Number of Nodes in the field
        self.Model, self.myArea = set_param.setParameters(self.n)  # #Set Parameters Sensors and Network

        self.conf_sen()
        self.init_param()
        self.start_sim(n)
        self.start_main_loop()

    def conf_sen(self):
        # ######################### configuration Sensors ####################
        # Create a random scenario & Load sensor Location
        self.X, self.Y = create_rand_sim.start(self.Model, self.myArea)
        # configure sensors
        self.Sensors = configure_sen.start(self.Model, self.n, self.X, self.Y)
        self.deadNum = 0  # Number of dead nodes
        self.myplot = plot_ileach.start(Sensors=self.Sensors, Model=self.Model, deadnum=self.deadNum)

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

        # % All sensor send location information to Sink .
        self.Sensors = dist_to_sink.disToSink(self.Sensors, self.Model)

        # %Save metrics
        self.SRP[1] = self.srp
        self.RRP[1] = self.rrp
        self.SDP[1] = self.sdp
        self.RDP[1] = self.rdp

        self.x = 0

    def start_main_loop(self):
        pass

    def zeros(self, row, column):
        re_list = []
        for x in range(row):
            temp_list = [0 for _ in range(column)]
            re_list.append(temp_list)

        return re_list

    def start(self):
        pass
