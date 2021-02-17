#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import sys
# import ConstrutiveHeuristic
import Distances
# import VND
import PSO


def create_graph(ffile):
    vertices = []
    coordenates = {}
    dist_type = 'type'

    try:
        with open(ffile) as archive:
            head = [next(archive) for _ in range(6)]
            qtd_vertices, dist_type = infogetter(head)
            vertices = [x for x in range(1, qtd_vertices+1)]

            line = next(archive)

            while 'EOF' not in line:
                v, x, y = valuesgetter(line)
                coordenates[v] = (x, y)
                line = next(archive)

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
    qtd_v = 0
    dist_type = "Null"

    for inf in lhead:
        if 'DIMENSION' in inf:
            qtd_v = int(inf.split(": ")[1])
        elif 'EDGE_WEIGHT_TYPE' in inf:
            dist_type = inf.split(": ")[1]
    return qtd_v, dist_type


def write_output(file, dist, path):
    outfile = open(sys.argv[2] + file, 'w')
    outfile.write(str(dist))
    outfile.write("\n")
    outfile.write(str(path))


def create_matrix(vertices, distances):
    cities_matrix = [[-1 for _ in range(len(vertices) + 1)] for _ in range(len(vertices) + 1)]
    for k, v in distances.items():
        for pair in v:
            cities_matrix[k][pair[0]] = pair[1]
    return cities_matrix


if __name__ == "__main__":
    lvert, lcoord, d_type = create_graph(sys.argv[1])
    # lvert, lcoord, d_type = create_graph("Entradas/test.tsp")
    if "EUC_2D" in d_type:
        dists = Distances.calculate_distances(lvert, lcoord, 0)
    else:
        dists = Distances.calculate_distances(lvert, lcoord, 1)

    cities = create_matrix(lvert, dists)
    ncities = len(lvert) + 1

    if "att" in sys.argv[1]:
        ofile = "att48.tsp"
    else:
        ofile = sys.argv[1][16:]

    write_output(ofile, *PSO.inicialize(cities, ncities))

    # cost, path = ConstrutiveHeuristic.construtive_heuristic(lvert, dists)
    # s = {cost: path}
