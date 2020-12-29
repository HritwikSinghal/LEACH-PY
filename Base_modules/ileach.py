import set_param


class ILEACH:

    def __init__(self, n=200, ):
        """
        %% Create sensor nodes, Set Parameters and Create Energy Model
        %%%%%%%%%%%%%%%%%%%%%%%%% Initial Parameters %%%%%%%%%%%%%%%%%%%%%%%

        :param n: Number of nodes in simulation

        """
        self.n = n
        self.myMedel, self.myArea = set_param.setParameters(self.n)

    def start(self):
        pass
