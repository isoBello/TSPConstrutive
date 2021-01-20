#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import math
import sys
from collections import defaultdict


def create_graph():
    vertices = []
    coordenates = {}

    try:
        with open(sys.argv[1]) as file:
            head = [next(file) for x in range(5)]
            qtd_vertices, distance_type = infogetter(head)
            vertices = [x for x in range(1, qtd_vertices+1)]

            lines = file.readlines()
            for line in lines[1:]:
                try:
                    v, x, y = valuesgetter(line)
                    coordenates[v] = (x, y)
                except TypeError:
                    continue

    except FileNotFoundError:
        print("File not found, please try another filename.")

    if "EUC_2D" in distance_type:
        calculate_distances(vertices, coordenates, 0)
    else:
        calculate_distances(vertices, coordenates, 1)


def valuesgetter(line):
    values = line.split(" ")
    try:
        v = int(values[0])
        x = float(values[1])
        y = float(values[2])
        return v, x, y
    except ValueError:
        pass


def infogetter(lhead):
    for inf in lhead:
        if 'DIMENSION' in inf:
            qtd_v = int(inf.split(" ")[1])
        elif 'EDGE_WEIGHT_TYPE' in inf:
            dist_type = inf.split(" ")[1]
    return qtd_v, dist_type


def calculate_distances(lvs, lcoords, type):
    count = 1
    distances = defaultdict(list)

    while count <= len(lvs):
        coords = lcoords.get(count)
        xi = coords[0]
        yi = coords[1]
        for k, v in lcoords.items():
            xj = v[0]
            yj = v[1]
            if type == 0:
                distances[count].append(calculate_euclidian_dist(xi, yi, xj, yj))
            else:
                distances[count].append(calculate_pseudo_euclidian_dist(xi, yi, xj, yj))
        count += 1


def calculate_euclidian_dist(x_i, y_i, x_j, y_j):
    xd = x_i - x_j
    yd = y_i - y_j
    return int(math.sqrt(pow(xd, 2) + pow(yd, 2)))


def calculate_pseudo_euclidian_dist(x_i, y_i, x_j, y_j):
    xd = x_i - x_j
    yd = y_i - y_j

    rij = math.sqrt(pow(xd, 2) + pow(yd, 2)/10.0)
    tij = int(rij)

    if tij < rij:
        return tij + 1
    else:
        return tij


if __name__ == "__main__":
    create_graph()
