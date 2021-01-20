#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import math
import sys
import ConstrutiveHeuristic
from collections import defaultdict
from os import listdir
from os.path import isfile, join


def create_graph():
    vertices = []
    coordenates = {}
    dist_type = 'type'

    onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]

    try:
        for file in onlyfiles:
            with open(file) as archive:
                head = [next(archive) for x in range(5)]
                qtd_vertices, dist_type = infogetter(head)
                vertices = [x for x in range(1, qtd_vertices+1)]

                lines = archive.readlines()
                for line in lines[1:]:
                    try:
                        v, x, y = valuesgetter(line)
                        coordenates[v] = (x, y)
                    except TypeError:
                        continue

    except FileNotFoundError:
        print("File not found, please try another filename.")

    return vertices, coordenates, dist_type


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

    rij = math.sqrt(pow(xd, 2) + pow(yd, 2)/10.0)
    tij = int(rij)

    if tij < rij:
        return tij + 1
    else:
        return tij


if __name__ == "__main__":
    lvert, lcoord, d_type = create_graph()

    if "EUC_2D" in d_type:
        dists = calculate_distances(lvert, lcoord, 0)
    else:
        dists = calculate_distances(lvert, lcoord, 1)

    ConstrutiveHeuristic.construtive_heuristic(lvert, dists)
