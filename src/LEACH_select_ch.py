import random
from src.LEACH_set_parameters import *
from src.LEACH_configure_sensors import *


def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


def start(Sensors: list[Sensor], myModel: Model, round_number: int, circlex, circley):
    CH = []
    # countCHs = 0 # no use
    n = myModel.n

    # numRx = myModel.numRx
    # dr = myModel.dr
    # CH_selected_arr = zeros(numRx, numRx)

    # sink can't be a CH
    for senser in Sensors[:-1]:

        # # % these are the circle (x,y) for this node
        # row_circle_of_node = -1
        # col_circle_of_node = -1
        # br = 0
        #
        # # % checking in which circle this node lies
        # for row in range(numRx):
        #     for column in range(numRx):
        #         if (sqrt((Sensors[i].xd - circlex[row][column]) ^ 2 +
        #                  (Sensors[i].yd - circley[row][column]) ^ 2) <= dr / 2):
        #             row_circle_of_node = row
        #             col_circle_of_node = column
        #
        #             br = 1
        #             break
        #
        #     if br == 1:
        #         break
        #
        # # % if this node is not in any circle then also skip
        # if br == 0:
        #     continue
        #
        # # % if CH of this circle has already been chosen, then skip
        # if CH_selected_arr[row_circle_of_node][col_circle_of_node] == 1:
        #     continue

        # If current sensor has energy left and has not been CH before
        if senser.E > 0 and senser.G <= 0:
            # Election of Cluster Heads
            temp_rand = random.uniform(0, 1)
            value = myModel.p / (1 - myModel.p * (round_number % round(1 / myModel.p)))
            print(f'for {senser.id}, temprand = {temp_rand}, value = {value}')
            if temp_rand <= value:
                # countCHs += 1
                print(f"Adding {senser.id} to CH")
                CH.append(senser.id)
                # CH[countCHs].id = i  # ok
                senser.type = 'C'
                senser.G = round(1 / myModel.p) - 1

                # # mark this cirle now that it has a CH
                # CH_selected_arr(row_circle_of_node, col_circle_of_node) = 1

    return CH
