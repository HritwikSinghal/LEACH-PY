from math import inf


def start(Sensors, Model):
    n = Model.n
    for i in range(n):
        Sensors[i].MCH = n + 1
        Sensors[i].type = 'N'
        Sensors[i].dis2ch = inf
