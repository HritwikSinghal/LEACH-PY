import random


class Simulation:

    def __init__(self, Model, Area):
        self.n = Model.n
        self.x = Area.x
        self.y = Area.y

        self.X = [
            random.randint(1, self.x)
            for _ in range(self.n)
        ]

        self.Y = [
            random.randint(1, self.y)
            for _ in range(self.n)
        ]


def start(myModel, myArea):
    mySim = Simulation(Model=myModel, Area=myArea)
    return mySim.X, mySim.Y
