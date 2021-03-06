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


def start(Sensors, Model, TotalCH):
    n = Model.n
    m = len(TotalCH)
    if m > 1:
        D = zeros(m, n)
        for i in range(n):
            for j in range(m):
                D[j][i] = sqrt((Sensors[i].xd - Sensors[TotalCH[j].id].xd) ^ 2 +
                               (Sensors[i].yd - Sensors[TotalCH(j).id].yd) ^ 2
                               )

        # todo: WT?
        [Dmin, idx] = min(D)

        for i in range(n):
            if Sensors[i].E > 0:
                # if node is in RR CH and is Nearer to CH rather than Sink
                if Dmin[i] <= Model.RR and Dmin[i] < Sensors[i].dis2sink:
                    Sensors[i].MCH = TotalCH[idx[i]].id
                    Sensors[i].dis2ch = Dmin[i]
                else:
                    Sensors[i].MCH = n + 1
                    Sensors[i].dis2ch = Sensors[i].dis2sink
