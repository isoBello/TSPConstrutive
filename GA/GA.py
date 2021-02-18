#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-

# Genetic Algorithmfor TSP problem
import random
from Fitness import Fitness
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

dtype = None


def create_route(cities):
    route = random.sample(cities, len(cities))
    route.append(route[0])
    return route


def create_population(size, cities):
    population = []
    for i in range(0, size):
        population.append(create_route(cities))
    return population


def get_fitness(population):
    global dtype
    fit = {}
    for i in range(0, len(population)):
        fit[i] = Fitness(population[i]).get_fitness(dtype)
    return sorted(fit.items(), key=itemgetter(1), reverse=True)


def selection(population, elite):
    results = []
    df = pd.DataFrame(np.array(population), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite):
        results.append(population[i][0])
    for i in range(0, len(population) - elite):
        pick = 100 * random.random()
        for i in range(0, len(population)):
            if pick <= df.iat[i, 3]:
                results.append(population[i][0])
                break
    return results


def matingPool(population, results):
    matingpool = []
    for i in range(0, len(results)):
        index = results[i]
        matingpool.append(population[index])
    return matingpool


def breed(A, B):
    childP1 = []

    geneA = int(random.random() * len(A))
    geneB = int(random.random() * len(A))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(A[i])

    childP2 = [item for item in B if item not in childP1]

    child = childP1 + childP2
    return child


def breedPopulation(matingpool, elite):
    children = []
    length = len(matingpool) - elite
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, elite):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if random.random() < mutationRate:
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


def mutatePopulation(population, mutationRate):
    mutated = []

    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutated.append(mutatedInd)
    return mutated


def nextGeneration(currentGen, elite, mutationRate):
    global dtype
    popRanked = get_fitness(currentGen)
    selectionResults = selection(popRanked, elite)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, elite)
    next = mutatePopulation(children, mutationRate)
    return next


def GA(file, population, size, elite, mutationRate, generations):
    pop = create_population(size, population)
    progress = [1 / get_fitness(pop)[0][1]]

    for i in range(0, generations):
        pop = nextGeneration(pop, elite, mutationRate)
        progress.append(1 / get_fitness(pop)[0][1])

    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.savefig(file)

    bcost = 1 / get_fitness(pop)[0][1]
    bpath = pop[get_fitness(pop)[0][0]]

    return bcost, bpath


def type(dt):
    global dtype
    dtype = dt
