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
    # DO not use this, it will assign same object to all in array so all will have save xd, yd etc
    # emptySensor = Sensor()

    # Configuration Sensors
    # created extra one slot for sink
    Sensors = [
        Sensor() for _ in range(n + 1)
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
    """ 
    first n - 1 slots in Sensors are for normal sensors. (0 to n-1) 
    nth slot is for sink
    so for n=10, 0-9 are 10 normal sensors and 10th slot is for sink 
    """
    Sensors[n].xd = Model.sinkx
    Sensors[n].yd = Model.sinky
    Sensors[n].E = 100
    Sensors[n].id = Model.n

    return Sensors
