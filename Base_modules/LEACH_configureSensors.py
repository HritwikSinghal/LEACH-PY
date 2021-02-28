class Sensor:

    def __init__(self):
        # Configuration EmptySensor
        self.xd = 0
        self.yd = 0
        self.G = 0
        self.df = 0
        self.type = 'N'
        self.E = 0
        self.id = 0
        self.dis2sink = 0
        self.dis2ch = 0
        self.MCH = 0  # Member of which CH


def start(Model, n, GX, GY):
    emptySensor = Sensor()

    # Configuration Sensors
    Sensors = [
        emptySensor for _ in range(n + 1)
    ]

    for i in range(n):
        # set x location
        Sensors[i].xd = GX[i]
        # set y location
        Sensors[i].yd = GY[i]
        # Determinate whether in previous periods has been clusterhead or not? not=0 and be=n
        Sensors[i].G = 0
        # dead flag. Whether dead or alive S[i].df=0 alive. S[i].df=1 dead.
        Sensors[i].df = 0
        # initially there are not each cluster heads 
        Sensors[i].type = 'N'
        # initially all nodes have equal Energy
        Sensors[i].E = Model.Eo
        # id
        Sensors[i].id = i
        # Sensors[i].RR=Model.RR

    # for sink
    Sensors[n + 1].xd = Model.sinkx
    Sensors[n + 1].yd = Model.sinky
    Sensors[n + 1].E = 100
    Sensors[n + 1].id = Model.n + 1

    return Sensors
