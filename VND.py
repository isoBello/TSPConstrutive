#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
from numpy import random
import heapq
from copy import deepcopy


# Need to garantee that the neighbours will be different
def VND(vertices, distances, s):
    neighbours = get_neighbourhood(vertices, distances, s)
    r = len(neighbours)
    k = 1

    bcost = list(s.keys())[0]
    bpath = s.get(bcost)

    solutions = list(neighbours.items())
    heapq.heapify(solutions)

    while k <= r:
        cost, path = heapq.heappop(solutions)
        if cost < bcost:
            bcost = cost
            bpath = path

            solutions.clear()
            solutions = sk_neighbourhood(vertices, distances, {bcost: bpath})
            k = 1
        else:
            k += 1

    return bcost, bpath


def sk_neighbourhood(vertices, distances, s):
    neighbours = get_neighbourhood(vertices, distances, s)
    solutions = list(neighbours.items())
    heapq.heapify(solutions)

    return solutions


def get_neighbourhood(vertices, distances, s):
    while len(s) < len(vertices):
        option = random.randint(1, 3)
        if option == 1:
            s = change_position(s, vertices, distances)
        else:
            s = move_city(s, vertices, distances)
    return s


def change_position(s, vertices, distances):
    orgpath = list(s.values())[0]
    path = change(vertices, orgpath)

    while True:
        if path in s.values():
            path = change(vertices, orgpath)
        else:
            break

    return calculate_cost(s, distances, path)


def move_city(s, vertices, distances):
    orgpath = list(s.values())[0]
    path = move(vertices, orgpath)

    while True:
        if path in s.values():
            path = move(vertices, orgpath)
        else:
            break

    return calculate_cost(s, distances, path)


def calculate_cost(s, distances, path):
    index = 1
    cost = 0

    while index < len(path):
        u = path[index-1]
        v = path[index]

        for w in distances.get(u):
            if w[0] == v:
                cost = cost + w[1]
                break

        index += 1

    s[cost] = path
    return s


def change(vertices, opath):
    first = random.randint(1, len(vertices))
    second = random.randint(1, len(vertices))

    while second == first:
        second = random.randint(1, len(vertices))

    path = deepcopy(opath)
    ind_first = path.index(first)
    ind_snd = path.index(second)

    path[ind_first] = second
    path[ind_snd] = first

    return path


def move(vertices, orpath):
    u = random.randint(1, len(vertices))

    path = deepcopy(orpath)
    ind_first = path.index(u)

    try:
        ind_snd = ind_first + 1
        temp = path[ind_snd]

    except IndexError:
        ind_snd = ind_first - 1
        temp = path[ind_snd]

    path[ind_snd] = u
    path[ind_first] = temp

    return path
