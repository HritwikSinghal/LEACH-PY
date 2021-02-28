from Base_modules import LEACH_setParameters
from math import *


def start(Sensors: [], Model: LEACH_setParameters.Model, deadnum=0):
    n = Model.n
    numRx = Model.numRx
    zeroarr = [0 for x in range(numRx)]
    circlex = [
        zeroarr for x in range(numRx)
    ]
    circley = [
        zeroarr for x in range(numRx)
    ]

    for i in range(numRx):
        for j in range(numRx):
            circlex[i][j] = (Model.dr / 2) + ((j - 1) * Model.dr)
            circley[i][j] = (Model.dr / 2) + ((i - 1) * Model.dr)

    pi = 3.1415
    r = Model.dr / 2
    angle = [0]
    last = 0
    for i in range(199):
        angle.append(round(last + pi / 100, 4))
        last += 3.14 / 100

    xp = [r * cos(each_angle) for each_angle in angle]
    yp = [r * sin(each_angle) for each_angle in angle]

    # todo: next part is missing
