#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import heapq
from numpy import random
from copy import deepcopy


def VND(vertices, distances, s):
    neighbours = get_neighbourhood(vertices, distances, s)
    r = len(vertices)
    k = 1

    bcost = list(s.keys())[0]
    bpath = s.get(bcost)

    solutions = list(neighbours.items())

    while k <= r:
        neighbours = solutions[k][1]
        heapq.heapify(neighbours)

        try:
            cost, path = heapq.heappop(neighbours)
        except IndexError:
            pass

        if cost < bcost:
            bcost = cost
            bpath = path
            k = 1
        else:
            k += 1

    return bcost, bpath


def get_neighbourhood(vertices, distances, s):
    bpath = list(list(s.values())[0])

    k = 0
    i = len(vertices)

    neighbourhood = create_dict(i)

    for v in bpath:
        npath = bpath[:]
        option = random.randint(1, 3)
        while k < i:
            if option == 1:  # Change the city with another one
                path = change_cities(v, i, bpath)
                cost = calculate_cost(distances, path)
                neighbourhood[v].append((cost, path))
            else:  # Move city to another place
                path = move_city(v, npath)
                cost = calculate_cost(distances, path)
                npath = path[:]
                neighbourhood[v].append((cost, path))
            k += 1
        k = 0

    neighbourhood = check_equals(neighbourhood)
    return neighbourhood


def change_cities(v, i, bpath):
    second = random.randint(1, i)
    path = deepcopy(bpath)

    ind_first = path.index(v)
    ind_snd = path.index(second)

    path[ind_first] = second
    path[ind_snd] = v

    path = check_integrity(path)
    return path


def move_city(v, npath):
    path = deepcopy(npath)
    ind_first = path.index(v)

    try:
        ind_snd = ind_first + 1
        temp = path[ind_snd]

    except IndexError:
        ind_snd = ind_first - 1
        temp = path[ind_snd]

    path[ind_snd] = v
    path[ind_first] = temp

    path = check_integrity(path)
    return path


def calculate_cost(distances, path):
    index = 1
    cost = 0

    while index < len(path):
        u = path[index - 1]
        v = path[index]

        for w in distances.get(u):
            if w[0] == v:
                cost = cost + w[1]
                break

        index += 1

    return cost


def create_dict(i):
    dicionary = {}
    for j in range(0, i + 1):
        dicionary[j] = []
    return dicionary


def check_equals(neighbourhood):
    temp = []
    ans = {}

    for k, val in neighbourhood.items():
        for v in val:
            if (v[0], v[1]) not in temp:
                temp.append((v[0], v[1]))
        ans[k] = temp
        temp = []
    return ans


def check_integrity(path):
    auxpath = path[:]
    auxpath = list(dict.fromkeys(auxpath))
    if auxpath[:-1] == auxpath[0]:
        return auxpath
    else:
        auxpath.append(auxpath[0])
    return auxpath