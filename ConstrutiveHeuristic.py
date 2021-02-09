#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-
from numpy import random
import heapq


def construtive_heuristic(vertices, distances):
    visited = [False] * (len(vertices)+1)
    u = random.randint(1, 52)
    visited[u] = True

    stack = [(0, u)]
    total_distance = 0
    path = []

    while len(path) <= len(vertices) and stack:
        distance, u = heapq.heappop(stack)

        while visited[u] and stack:
            distance, u = heapq.heappop(stack)

        visited[u] = True
        stack.clear()  # Cleaning the distances 'cause we already have our u

        if u not in path:
            path.append(u)
            total_distance += distance

        for v in distances.get(u):   # Getting the distance between u and every vertex
            if not visited[v[0]]:
                heapq.heappush(stack, (v[1], v[0]))

    for v in distances.get(u):  # Putting the connection between origin > last vertex in path
        if v[0] == path[-1]:
            total_distance = total_distance + v[1]
            break

    return total_distance, path

