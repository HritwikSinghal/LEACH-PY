from math import *


def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


def start(Sensors, Model, Sender, SenderRR):
    Receiver = []

    # Calculate Distance All Sensor With Sender
    # [Note that for doing so you need to access the global fig variable]
    n = Model.n
    D = zeros(1, n)

    for i in range(n):
        D[i] = sqrt((Sensors[i].xd - Sensors[Sender].xd) ^ 2 + (Sensors[i].yd - Sensors[Sender].yd) ^ 2)

    for i in range(n):
        if D[i] <= SenderRR & Sender != Sensors[i].id:
            # todo: what does below do?
            Receiver = [Receiver, Sensors[i].id]  # ok

    return Receiver
