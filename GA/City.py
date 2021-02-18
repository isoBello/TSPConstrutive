#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import math


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city, type):
        if "EUC_2D" in type:
            distance = use_euclidian(self, city)
        else:
            distance = use_att(self, city)
        return distance

    def get_coord(self):
        return self.x, self.y


def use_euclidian(i, j):
    xd = i.x - j.x
    yd = i.y - j.y
    return int(math.sqrt(pow(xd, 2) + pow(yd, 2)))


def use_att(i, j):
    xd = i.x - j.x
    yd = i.y - j.y

    rij = math.sqrt((pow(xd, 2) + pow(yd, 2)) / 10.0)
    tij = int(rij)

    if tij < rij:
        return tij + 1
    else:
        return tij
