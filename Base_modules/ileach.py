import create_rand_sim
import set_param
import plot_ileach
import configure_sen


class ILEACH:

    def __init__(self, n=200, ):
        # %% Create sensor nodes, Set Parameters and Create Energy Model
        # %%%%%%%%%%%%%%%%%%%%%%%%% Initial Parameters %%%%%%%%%%%%%%%%%%%%%%%

        self.n = n  # %Number of Nodes in the field
        self.myModel, self.myArea = set_param.setParameters(self.n)  # %Set Parameters Sensors and Network

        # %%%%%%%%%%%%%%%%%%%%%%%%% configuration Sensors %%%%%%%%%%%%%%%%%%%%

        # %Create a random scenario & Load sensor Location
        self.X, self.Y = create_rand_sim.start(self.myModel, self.myArea)

        self.Sensors = configure_sen.start(self.myModel, self.n, self.X, self.Y)

        self.deadNum = 0  # Number of dead nodes
        myplot = plot_ileach.start()

    def start(self):
        pass
