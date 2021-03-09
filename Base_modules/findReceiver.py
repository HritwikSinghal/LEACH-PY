from math import *
from Base_modules.LEACH_set_parameters import *
from Base_modules.LEACH_configure_sensors import *


def zeros(row, column):
    re_list = []
    for x in range(row):
        # FindReceiver specific modification
        temp_list = [float(0) for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


def start(Sensors: list[Sensor], myModel: Model, sender, senderRR):
    Receiver = []

    # Calculate Distance All Sensor With Sender
    # [Note that for doing so you need to access the global fig variable]
    n = myModel.n
    distance = zeros(1, n)

    for i in range(n):
        distance[i] = sqrt(
            pow(Sensors[i].xd - Sensors[sender].xd, 2) + pow(Sensors[i].yd - Sensors[sender].yd, 2)
        )
        if distance[i] <= senderRR and sender != Sensors[i].id:
            Receiver.append(Sensors[i].id)

    return Receiver
