import matplotlib

from src.LEACH_create_basics import *

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# todo: add condition to show sink only as red dot and not both red and blue
def start(Sensors: [Sensor], myModel: Model):
    print('########################################')
    print('############# plot Sensors #############')
    print('########################################')
    print()

    n = myModel.n
    plt.plot([Sensors[n].xd], [Sensors[n].yd], 'r^', label="Sink")

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
    n_flag = True
    for sensor in Sensors:

        if n_flag:
            plt.plot([sensor.xd], [sensor.yd], 'b+', label='Nodes')
            n_flag = False
        else:
            plt.plot([sensor.xd], [sensor.yd], 'b+')
    #     if sensor.E > 0:
    #         if sensor.type == 'N':
    #             # plot(Sensors(i).xd, Sensors(i).yd, 'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'k');
    #             pass  # todo: Plot here
    #         else:  # Sensors.type == 'C'
    #             # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'r');
    #             pass  # todo: Plot here
    #     else:
    #         deadNum += 1
    #         # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize',5, 'MarkerFaceColor', 'w');
    #         pass  # todo: plot here
    plt.title('Network Plot for Leach')
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.legend(loc='upper right')
    plt.show()

    '''
    plot(Sensors(n+1).xd,Sensors(n+1).yd,'bo', 'MarkerSize', 8, 'MarkerFaceColor', 'b');
    text(Sensors(n+1).xd+1,Sensors(n+1).yd-1,'Sink');
    axis square
    '''
