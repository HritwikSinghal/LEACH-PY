from src.LEACH_create_basics import *


def zeros(row, column):
    re_list = []
    for x in range(row):
        # Todo: UNCOMMENT
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
        # node should be in RR and it should be not DEAD
        if distance[i] <= senderRR and sender != Sensors[i].id and Sensors[i].E > 0:
            Receiver.append(Sensors[i].id)
            # Todo: UNCOMMENT
            # print(f"{sender} has reciever: {Sensors[i].id}")

    return Receiver
