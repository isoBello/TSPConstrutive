#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
import numpy as np


def graph():
    coordenates = {}
    head = {}

    try:
        with open(sys.argv[1]) as file:
            for inf in range(0, int(file.readline())[5]):
                infos = inf.split(" ")
                head[infos[0]] = infos[:0]
            vertices = [x for x in range(0, head.get("DIMENSION:"))]

            for line in file.readline()[5:]:
                try:
                    values = line.split(" ")
                    v = values[0]
                    x = values[1]
                    y = values[2]

                    coordenates[v] = (x, y)
                except ValueError:
                    continue
    except FileNotFoundError:
        print("File not found, please try another filename.")

    if head.get("EDGE_WEIGHT_TYPE") == "EUC_2D":
        calculate_distances(vertices, coordenates, 0)
    else:
        calculate_distances(vertices, coordenates, 1)


def calculate_distances(lvs, lcoords, type):
    count = 1
    distances = defaultdict(list)

    while count < len(lvs):
        coords = lcoords.get(count)
        xi = coords[0]
        yi = coords[1]
        for k, v in lcoords.items():
            if k != count:
                xj = v[0]
                yj = v[1]
                if type == 0:
                    distances[count].append(calculate_euclidian_dist(xi, yi, xj, yj))
                else:
                    distances[count].append(calculate_pseudo_euclidian_dist(xi, yi, xj, yj))
        count += 1
    print(distances)


def calculate_euclidian_dist(x_i, y_i, x_j, y_j):
    xd = x_i - x_j
    yd = y_i - y_j
    return int(np.sqrt(pow(xd, 2) + pow(yd, 2)))


def calculate_pseudo_euclidian_dist(x_i, y_i, x_j, y_j):
    xd = x_i - x_j
    yd = y_i - y_j

    rij = np.sqrt(pow(xd, 2) + pow(yd, 2)/10.0)
    tij = int(rij)

    if tij < rij:
        return tij + 1
    else:
        return tij
