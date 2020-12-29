from Base_modules import create_rand_sim
from Base_modules import set_param
from Base_modules import plot_ileach
from Base_modules import configure_sen


class ILEACH:

    def __init__(self, n=200, ):
        # Create sensor nodes, Set Parameters and Create Energy Model
        # ######################### Initial Parameters #######################

        self.n = n  # #Number of Nodes in the field
        self.myModel, self.myArea = set_param.setParameters(self.n)  # #Set Parameters Sensors and Network

        # ######################### configuration Sensors ####################

        # Create a random scenario & Load sensor Location
        self.X, self.Y = create_rand_sim.start(self.myModel, self.myArea)

        # configure sensors
        self.Sensors = configure_sen.start(self.myModel, self.n, self.X, self.Y)

        self.deadNum = 0  # Number of dead nodes
        myplot = plot_ileach.start(Sensors=self.Sensors, Model=self.myModel, deadnum=self.deadNum)

        # ################# Parameters initialization #############

    def start(self):
        pass
