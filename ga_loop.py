"""
ga_loop.py - Connects Person 2's GA core (ga.py) with Person 3's operators
(operators.py) into a complete genetic algorithm.

Uses from ga.py : create_population, fitness (and tournament_selection if present)
Uses from operators.py : crossover, mutate

Kept in its own file so it keeps working even if ga.py is reorganised. If
Person 2 puts the main loop into ga.py, this file can be dropped or kept as the
"runner" used by run_experiments.py.

Usage:
    from ga_loop import run_ga
    route, length, history = run_ga(cities, seed=1)
"""
import random

from tsp import route_length
from ga import create_population
from operators import crossover, mutate

try:
    from ga import tournament_selection      # Person 2's version, if it exists
except ImportError:
    def tournament_selection(population, cities, k=5):
        """Fallback: pick k random tours and return the shortest one."""
        contenders = random.sample(population, k)
        return min(contenders, key=lambda r: route_length(r, cities))


def run_ga(cities, population_size=100, generations=300,
           crossover_method="ox", mutation_method="inversion",
           crossover_rate=0.9, mutation_rate=0.2,
           tournament_k=5, elitism=2, seed=None):
    """
    Run the GA. Returns (best_route, best_length, history).

    history[g] = best tour length found up to generation g (for the
    convergence plot).
    crossover_method : "ox" or "pmx"
    mutation_method  : "swap" or "inversion"
    elitism          : number of best tours copied unchanged each generation
    """
    if seed is not None:
        random.seed(seed)

    tournament_k = min(tournament_k, population_size)
    population = create_population(cities, population_size)
    best_route = min(population, key=lambda r: route_length(r, cities))
    best_length = route_length(best_route, cities)
    history = []

    for _ in range(generations):
        ranked = sorted(population, key=lambda r: route_length(r, cities))
        new_population = [r[:] for r in ranked[:elitism]]

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, cities, tournament_k)
            parent2 = tournament_selection(population, cities, tournament_k)
            child = crossover(parent1, parent2, crossover_method, crossover_rate)
            child = mutate(child, mutation_method, mutation_rate)
            new_population.append(child)

        population = new_population

        gen_best_length = route_length(ranked[0], cities)
        if gen_best_length < best_length:
            best_route, best_length = ranked[0][:], gen_best_length
        history.append(best_length)

    final_best = min(population, key=lambda r: route_length(r, cities))
    final_length = route_length(final_best, cities)
    if final_length < best_length:
        best_route, best_length = final_best[:], final_length
        if history:
            history[-1] = best_length

    return best_route, best_length, history


if __name__ == "__main__":
    from baselines import greedy, brute_force

    random.seed(42)
    cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    route, length, hist = run_ga(cities, seed=1)
    print("GA length        :", round(length, 2))
    print("Greedy length    :", round(route_length(greedy(cities), cities), 2))
    print("Brute force      :", round(route_length(brute_force(cities), cities), 2))
    print("Generation 1 -> last:", round(hist[0], 2), "->", round(hist[-1], 2))