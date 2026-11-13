# ga.py - Person 2: GA Core
# Functions: population, fitness, selection, main generation loop
import random
from tsp import route_length, distance

def create_population(cities, population_size=100):
    population = []
    num_cities = len(cities)
    for i in range(population_size):
        route = list(range(num_cities))  # [0, 1, 2, 3, ...]
        random.shuffle(route)            # shuffle into random order
        population.append(route)
    return population

def fitness(route, cities):
    return 1 / route_length(route, cities)  # shorter route = higher fitness