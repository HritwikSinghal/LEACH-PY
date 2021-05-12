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


def start(sensors: list[Sensor], my_model: Model, sender, sender_rr):
    receiver = []

    # Calculate Distance All Sensor With Sender
    n = my_model.n
    distance = zeros(1, n)

    for i, sensor in enumerate(sensors[:-1]):
        distance[i] = sqrt(
            pow(sensor.xd - sensors[sender].xd, 2) + pow(sensor.yd - sensors[sender].yd, 2)
        )
        
        # node should be in RR
        if distance[i] <= sender_rr and sender != sensor.id:
            receiver.append(sensor.id)
            # Todo: UNCOMMENT
            # print(f"{sender} has reciever: {sensor.id}")

    return receiver
