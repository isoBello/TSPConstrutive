# -*- coding: utf-8 -*-
# !/usr/bin/env pypy
import Ant

from copy import deepcopy
from numpy import random

# Parameters
ant_rate = 0
iterations = 0
evaporation_rate = 0
Q = 0
alpha = 0
beta = 0

# Lists and Matrix
ants = []
trails = [[]]
probs = []
cities = [[]]
choices = []
solutions = []
stats = []

# Utilities
number_cities = 0
factor = 0.01
tour = None
size = -1


# This function inicialize the lists of our algorithm, like trails and ants; in this we get the parameters values too
def inicialize(c, n_cities):
    global ant_rate, iterations, evaporation_rate, Q, alpha, beta
    ant_rate, iterations, evaporation_rate, Q, alpha, beta = parameters()

    global number_cities
    number_cities = n_cities

    global trails, ants, probs, cities
    trails = [[1.0 for _ in range(number_cities)] for _ in range(number_cities)]
    probs = [0] * number_cities

    for _ in range(ant_rate):
        ants.append(Ant.Ant(number_cities))

    cities = c   # This is our initial solution
    solve()

    return tour, size


def solve():
    global iterations

    for i in range(iterations):
        for ant in ants:
            setup(ant)
            move(ant)
        update()
        best()
        clear()


# This function prepare ants for simulation
def setup(ant):
    global number_cities
    ant.clearvisits()
    ant.visit(random.random_integers(low=1, high=number_cities-1, size=1)[0])  # Puts each ant in one node


# At each iteration, construct the path for ants
def move(ant):
    global number_cities, probs, cities, choices

    task = True
    choices = []
    while task:
        # choices = []
        try:
            # The first thing we try is move the ant for a random city connected to our last city
            # For this, we see if one rand number is < that our random factor
            source = ant.trail[-1]
            rand = random.random_sample()
            task = False  # Control if there's another city to visited.
            # If the loop and with task = False, there's no city left.

            if rand < factor:
                for j in range(number_cities):
                    if cities[source][j] != -1 and not ant.isvisited(j):
                        choices.append(j)

                # This means we gonna walk to a random city
                try:
                    ant.visit(random.choice(choices, 1)[0])
                    task = True
                except ValueError:
                    task = False

            # If we don't pick a random city, then we choose one based in the pheromone rate.
            # The ants prefer to follow stronger and shorter trails.
            # We store the probability of moving to each city in our possibilities
            calculate(ant)

            T = 0

            for j in range(number_cities):
                T += probs[j]

            rand = random.uniform(0, T)
            S = 0
            for j in range(number_cities):  # Based in roulet selection
                S += probs[j]
                if S >= rand and cities[source][j] != -1 and not ant.isvisited(j):
                    ant.visit(j)
                    task = True
                    break
        except IndexError:
            # No city was left to the ant
            break


# Calculate the next city picks probabilities
def calculate(ant):
    global number_cities, alpha, beta, probs

    i = ant.trail[-1]
    pheromone = 0.0

    for j in range(number_cities):
        if not ant.isvisited(j) and cities[i][j] != -1:
            pheromone += pow(trails[i][j], alpha) * pow((1.0/cities[i][j]), beta)

    for j in range(number_cities):
        if cities[i][j] != -1:
            if ant.isvisited(j):
                probs[j] = 0.0
            else:
                n = pow(trails[i][j], alpha) * pow(1.0/cities[i][j], beta)
                probs[j] = n/pheromone


# Update trails that ants used to find their path
def update():
    global number_cities, evaporation_rate, Q

    for L in range(number_cities):
        for C in range(number_cities):
            if cities[L][C] != -1:
                trails[L][C] *= evaporation_rate

    for ant in ants:
        i = 0

        try:
            contribution = Q / ant.mileswalked(cities)
        except ZeroDivisionError:
            contribution = 0

        while True:
            try:
                if cities[ant.trail[i]][ant.trail[i + 1]] != -1:
                    trails[ant.trail[i]][ant.trail[i + 1]] += contribution
                i += 1
            except IndexError:
                break

        trails[ant.trail[len(ant.trail) - 1]][ant.trail[0]] += contribution


# Update the best solution that ants found
def best():
    global tour, size, solutions

    for ant in ants:
        W = ant.mileswalked(cities)

        path = ant.trail
        solutions.append((path, W))

        if W > size:
            size = W
            tour = deepcopy(ant.trail)


# Clear trails after simulation
def clear():
    for i in range(number_cities):
        for j in range(number_cities):
            trails[i][j] = 1.0


def parameters():
    global ant_rate, iterations, evaporation_rate, Q, alpha, beta
    ant_rate = 25
    iterations = 40
    evaporation_rate = 0.6
    Q = 0.2
    alpha = 2
    beta = 6
    return ant_rate, iterations, evaporation_rate, Q, alpha, beta
