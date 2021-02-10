#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import sys
import ConstrutiveHeuristic
import Distances
import VND


def create_graph(ffile):
    vertices = []
    coordenates = {}
    dist_type = 'type'

    try:
        with open(ffile) as archive:
            head = [next(archive) for x in range(6)]
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


if __name__ == "__main__":
    lvert, lcoord, d_type = create_graph(sys.argv[1])

    if "EUC_2D" in d_type:
        dists = Distances.calculate_distances(lvert, lcoord, 0)
    else:
        dists = Distances.calculate_distances(lvert, lcoord, 1)

    cost, path = ConstrutiveHeuristic.construtive_heuristic(lvert, dists)
    s = {cost: path}

    if "att" in sys.argv[1]:
        ofile = "att48.tsp"
    else:
        ofile = sys.argv[1][16:]

    write_output(ofile, *VND.VND(lvert, dists, s))
