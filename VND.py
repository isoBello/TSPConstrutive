#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
import heapq
import itertools
from numpy import random
from copy import deepcopy
from collections import defaultdict


def VND(vertices, distances, s):
    neighbours = get_neighbourhood(vertices, distances, s)
    r = len(vertices)
    k = 1

    bcost = list(s.keys())[0]
    bpath = s.get(bcost)

    solutions = list(neighbours.items())
    heapq.heapify(solutions)

    # r = len(neighbours)
    # k = 1
    #
    # bcost = list(s.keys())[0]
    # bpath = s.get(bcost)
    #
    # solutions = list(neighbours.items())
    # heapq.heapify(solutions)
    #
    # while k <= r:
    #     cost, path = heapq.heappop(solutions)
    #     if cost < bcost:
    #         bcost = cost
    #         bpath = path
    #
    #         # solutions.clear()
    #         # solutions = sk_neighbourhood(vertices, distances, {bcost: bpath})
    #         k = 1
    #     else:
    #         k += 1
    #
    # return bcost, bpath


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
                cost, path = move_city(v, npath, distances)
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

    return path


def move_city(v, bpath, distances):
    path = deepcopy(bpath)
    ind_first = path.index(v)

    try:
        ind_snd = ind_first + 1
        temp = path[ind_snd]

    except IndexError:
        ind_snd = ind_first - 1
        temp = path[ind_snd]

    path[ind_snd] = v
    path[ind_first] = temp

    cost = calculate_cost(distances, path)
    return cost, path


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


# def sk_neighbourhood(vertices, distances, s):
#     neighbours = get_neighbourhood(vertices, distances, s)
#     solutions = list(neighbours.items())
#     heapq.heapify(solutions)
#
#     return solutions
#
#
# def get_neighbourhood(vertices, distances, s, neighbours):
#     r = 0
#     i = 0
#     neighbours[0] = deepcopy(s)
#
#     city = list(neighbours[0].get(list(neighbours[0].keys())[r]))
#
#     while len(neighbours) < len(vertices):
#         while i < len(vertices):
#             option = random.randint(1, 3)
#             if option == 1:
#                 neighbours[r] = change_position(city, neighbours[0], vertices, distances)
#             else:
#                 neighbours[r] = move_city(city, neighbours[0], vertices, distances)
#             i += 1
#
#         i = 0
#         r += 1
#
#     return neighbours
#
#
# def change_position(city, s, vertices, distances):
#     path = change(vertices, city)
#
#     while True:
#         if path in s.values():
#             path = change(vertices, city)
#         else:
#             break
#
#     return calculate_cost(s, distances, path)
#
#
# def move_city(city, s, vertices, distances):
#     path = move(vertices, city)
#
#     while True:
#         if path in s.values():
#             path = move(vertices, city)
#         else:
#             break
#
#     return calculate_cost(s, distances, path)
#
#
# def calculate_cost(s, distances, path):
#     index = 1
#     cost = 0
#
#     while index < len(path):
#         u = path[index-1]
#         v = path[index]
#
#         for w in distances.get(u):
#             if w[0] == v:
#                 cost = cost + w[1]
#                 break
#
#         index += 1
#
#     s[cost] = path
#     return s
#
#
# def change(vertices, opath):
#     first = random.randint(1, len(vertices))
#     second = random.randint(1, len(vertices))
#
#     while second == first:
#         second = random.randint(1, len(vertices))
#
#     path = deepcopy(opath)
#     ind_first = path.index(first)
#     ind_snd = path.index(second)
#
#     path[ind_first] = second
#     path[ind_snd] = first
#
#     return path
#
#
# def move(vertices, orpath):
#     u = random.randint(1, len(vertices))
#
#     path = deepcopy(orpath)
#     ind_first = path.index(u)
#
#     try:
#         ind_snd = ind_first + 1
#         temp = path[ind_snd]
#
#     except IndexError:
#         ind_snd = ind_first - 1
#         temp = path[ind_snd]
#
#     path[ind_snd] = u
#     path[ind_first] = temp
#
#     return path
