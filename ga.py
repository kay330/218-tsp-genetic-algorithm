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

def selection(population, cities, tournament_size=5):
    # Pick random routes and return the best one
    tournament = random.sample(population, tournament_size)
    best = max(tournament, key=lambda route: fitness(route, cities))
    return best

def run_ga(cities, population_size=100, generations=500):
    # Import Person 3's functions - agree names with them first!
    from operators import crossover, mutate
    
    # Step 1: create starting population
    population = create_population(cities, population_size)
    
    best_route = None
    best_fitness = 0
    
    # Step 2: run for many generations
    for gen in range(generations):
        new_population = []
        
        for i in range(population_size):
            # Step 3: select two parents
            parent1 = selection(population, cities)
            parent2 = selection(population, cities)
            
            # Step 4: create child using Person 3's crossover
            child = crossover(parent1, parent2)
            
            # Step 5: mutate the child using Person 3's mutation
            child = mutate(child)
            
            new_population.append(child)
        
        # Step 6: replace old population
        population = new_population
        
        # Step 7: track the best route found
        current_best = max(population, key=lambda route: fitness(route, cities))
        current_fitness = fitness(current_best, cities)
        
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_route = current_best
        
        # Print progress every 100 generations
        if gen % 100 == 0:
            print(f"Generation {gen}: best length = {route_length(best_route, cities):.2f}")
    
    return best_route