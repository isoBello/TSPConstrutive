#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import math
from collections import defaultdict


def calculate_distances(lvs, lcoords, type):
    count = 1
    distances = defaultdict(list)

    while count <= len(lvs):
        coords = lcoords.get(count)
        xi = coords[0]
        yi = coords[1]
        for k, v in lcoords.items():
            if k != count:
                xj = v[0]
                yj = v[1]
                if type == 0:
                    distances[count].append((k, calculate_euclidian_dist(xi, yi, xj, yj)))
                else:
                    distances[count].append((k, calculate_pseudo_euclidian_dist(xi, yi, xj, yj)))
        count += 1
    return distances


def calculate_euclidian_dist(x_i, y_i, x_j, y_j):
    xd = x_i - x_j
    yd = y_i - y_j
    return int(math.sqrt(pow(xd, 2) + pow(yd, 2)))


def calculate_pseudo_euclidian_dist(x_i, y_i, x_j, y_j):
    xd = x_i - x_j
    yd = y_i - y_j

    rij = math.sqrt((pow(xd, 2) + pow(yd, 2))/10.0)
    tij = int(rij)

    if tij < rij:
        return tij + 1
    else:
        return tij
