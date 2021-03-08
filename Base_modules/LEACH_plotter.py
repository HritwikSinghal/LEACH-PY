from Base_modules import LEACH_setParameters
from math import *
from Base_modules.LEACH_setParameters import *
from Base_modules.LEACH_configureSensors import *


def start(Sensors: [Sensor], myModel: Model, deadnum=0):
    n = myModel.n
    deadNum = 0

    # numRx = myModel.numRx
    # zeroarr = [0 for x in range(numRx)]
    # circlex = [
    #     zeroarr for x in range(numRx)
    # ]
    # circley = [
    #     zeroarr for x in range(numRx)
    # ]

    # for i in range(numRx):
    #     for j in range(numRx):
    #         circlex[i][j] = (myModel.dr / 2) + ((j - 1) * myModel.dr)
    #         circley[i][j] = (myModel.dr / 2) + ((i - 1) * myModel.dr)

    # pi = 3.1415
    # r = myModel.dr / 2
    # angle = [0]
    # last = 0
    # for i in range(199):
    #     angle.append(round(last + pi / 100, 4))
    #     last += 3.14 / 100
    #
    # xp = [r * cos(each_angle) for each_angle in angle]
    # yp = [r * sin(each_angle) for each_angle in angle]

    for sensor in Sensors:
        if sensor.E > 0:
            if sensor.type == 'N':
                # plot(Sensors(i).xd, Sensors(i).yd, 'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'k');
                pass  # todo: Plot here
            else:  # Sensors.type == 'C'
                # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'r');
                pass  # todo: Plot here
        else:
            deadNum += 1
            # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize',5, 'MarkerFaceColor', 'w');
            pass  # todo: plot here

        # hold on

    '''
    plot(Sensors(n+1).xd,Sensors(n+1).yd,'bo', 'MarkerSize', 8, 'MarkerFaceColor', 'b');
    text(Sensors(n+1).xd+1,Sensors(n+1).yd-1,'Sink');
    axis square
    '''

    # todo: fix this in in Ileach
    return deadNum, [], []
