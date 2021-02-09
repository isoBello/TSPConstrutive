#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
from numpy import random
import heapq


# Need to garantee that the neighbours will be different
def VND(vertices, distances, s):
    neighbours = get_neighbourhood(vertices, distances, s)
    r = len(neighbours)
    k = 1

    bcost = s.keys()[0]
    bpath = s.get(0)

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
        option = random.randint(1, 2)
        s = switch(option, vertices, distances, s)
    return s


def switch(n, vertices, distances, s):
    func = switcher.get(n, "nothing")
    return func(s, vertices, distances)


def change_position(s, vertices, distances):
    first = random.randint(1, len(vertices))
    second = random.randint(1, len(vertices))

    while second == first:
        second = random.randint(1, len(vertices))

    path = s.get(0)[1]
    ind_first = path.index(first)
    ind_snd = path.index(second)

    path[ind_first] = second
    path[ind_snd] = first

    return calculate_cost(s, distances, path)


def move_city(s, vertices, distances):
    u = random.randint(1, len(vertices))

    path = s.get(0)[1]
    ind_first = path.index(u)
    ind_snd = ind_first + 1

    temp = path[ind_snd]
    path[ind_snd] = u
    path[ind_first] = temp

    return calculate_cost(s, vertices, distances)


def calculate_cost(s, distances, path):
    index = 1
    cost = 0

    while index <= len(path):
        u = path[index-1]
        v = path[index]

        for w in distances.get(u):
            if w[0] == v:
                cost = cost + v[1]
                break

        index += 1

    s[cost] = path
    return s


switcher = {
    1: change_position,
    2: move_city
}
