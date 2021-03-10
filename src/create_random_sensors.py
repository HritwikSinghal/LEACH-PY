import random

from src.LEACH_set_parameters import *


def generate_x_y(myModel: Model, myArea: Area):
    n = myModel.n
    x = myArea.x
    y = myArea.y

    X = [
        random.randint(1, x)
        for _ in range(n)
    ]

    Y = [
        random.randint(1, y)
        for _ in range(n)
    ]

    return X, Y


def start(myModel, myArea):
    return generate_x_y(myModel, myArea)
