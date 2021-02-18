#!/TSPConstrutive/venv/bin python3.6
# -*- coding: utf-8 -*-

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fit = 0.0

    def get_distance(self, type):
        if self.distance == 0:
            dist = 0
            for i in range(0, len(self.route)):
                source = self.route[i]
                dest = None

                if i + 1 < len(self.route):
                    dest = self.route[i + 1]
                else:
                    dest = self.route[0]
                dist += dest.distance(source, type)
            self.distance = dist
        return self.distance

    def get_fitness(self, type):
        if self.fit == 0:
            self.fit = 1 / float(self.get_distance(type))
        return self.fit
