#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import sys
import GA
from City import City


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


def match(city, coords):
    for k, coord in coords.items():
        x, y = City.get_coord(city)
        if coord[0] == x and coord[1] == y:
            return k


if __name__ == "__main__":
    lvert, lcoord, d_type = create_graph(sys.argv[1])
    cities = []

    for v in lvert:
        cities.append(City(lcoord[v][0], lcoord[v][1]))

    GA.type(d_type)

    if "att" in sys.argv[1]:
        ofile = "att48.tsp"
    else:
        ofile = sys.argv[1][16:]

    cost, bpath = GA.GA(ofile.replace("tsp", "png"), population=cities, size=25, elite=5, mutationRate=0.01,
                        generations=50)

    path = []
    for city in bpath:
        c = match(city, lcoord)
        path.append(c)

    write_output(ofile, cost, path)
