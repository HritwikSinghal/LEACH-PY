from src.LEACH_create_basics import *


def zeros(row, column):
    re_list = []
    for x in range(row):
        # JoinToNearestCH specific modification
        temp_list = [0 for _ in range(column)]
        re_list.append(temp_list)

    return re_list


def get_min_and_id_of_ch(myModel: Model, TotalCH, distance: list):
    min_dist_from_all_ch = []
    id_of_min_dist_ch = []

    total_nodes = myModel.n
    number_of_ch = len(TotalCH)

    for node in range(total_nodes):
        min_dist = inf
        ch_id = -1
        for ch in range(number_of_ch):
            if distance[ch][node] <= min_dist:
                min_dist = distance[ch][node]
                ch_id = ch

        min_dist_from_all_ch.append(min_dist)
        id_of_min_dist_ch.append(ch_id)

    return min_dist_from_all_ch, id_of_min_dist_ch


def start(Sensors: list[Sensor], myModel: Model, TotalCH):
    print('# ######################################################')
    print('# ############# Sensors join to nearest CH #############')
    print('# ######################################################')

    total_nodes = myModel.n
    number_of_ch = len(TotalCH)

    # if there are CH
    if number_of_ch > 0:
        # creating a 2x2 array with each row storing the distance of all nodes for a CH
        distance = zeros(number_of_ch, total_nodes)

        # storing the distance of all nodes with every CH
        for i in range(total_nodes):
            for j in range(number_of_ch):
                distance[j][i] = sqrt(
                    pow(Sensors[i].xd - Sensors[TotalCH[j]].xd, 2) + pow(Sensors[i].yd - Sensors[TotalCH[j]].yd, 2)
                )

        # todo: test
        print("printing Distance array:")
        for x in distance:
            print(x)
        print()

        # what below does is:
        # We have stored all CH as row and took distance between each CH and all nodes in its Columns
        # this take minimum value of each column i.e min dist for each node and that dist is dist to CH
        min_dist_from_all_ch, id_of_min_dist_ch = get_min_and_id_of_ch(myModel, TotalCH, distance)

        # todo: test
        print("min_dist_from_all_ch")
        print(min_dist_from_all_ch)
        print('id_of_min_dist_ch')
        print(id_of_min_dist_ch)

        # for every node, check from which
        for i, sensor in enumerate(Sensors[:-1]):
            if sensor.E > 0:
                # if node is in RR CH and is Nearer to CH rather than Sink
                if min_dist_from_all_ch[i] <= myModel.RR and min_dist_from_all_ch[i] < sensor.dis2sink:
                    print(f"{sensor.id} is joining {TotalCH[id_of_min_dist_ch[i]]}")
                    sensor.MCH = TotalCH[id_of_min_dist_ch[i]]
                    sensor.dis2ch = min_dist_from_all_ch[i]
                else:
                    print(f"{sensor.id} is joining sink")
                    sensor.MCH = total_nodes
                    sensor.dis2ch = sensor.dis2sink
