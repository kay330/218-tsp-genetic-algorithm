import random

from baselines import two_opt
from operators import CROSSOVERS, MUTATIONS, crossover, mutate
from tsp import route_length
from config import GA

# Random routes: shuffled permutations of the city numbers.
def create_population(cities, population_size, rng):
    
    population = []
    for _ in range(population_size):
        route = list(range(len(cities)))
        rng.shuffle(route)
        population.append(route)
    return population

# Shorter route = higher fitness (1 divided by length). -> better
def fitness(length):
    return 1.0 / (length + 1e-9)

#Pick k random routes and return  one with the highest fitness.
def tournament_selection(population, lengths, k, rng):
    picks = rng.sample(range(len(population)), min(k, len(population)))
    return population[max(picks, key=lambda i: fitness(lengths[i]))]


def run_ga(cities,
    population_size=GA["population_size"],
    generations=GA["generations"],
    crossover_method="ox",
    mutation_method="inversion",
    crossover_rate=GA["crossover_rate"],
    mutation_rate=GA["mutation_rate"],
    tournament_k=GA["tournament_k"],
    elitism=GA["elitism"],
    memetic=False,
    seed=None):
# Run the GA. Returns (best_route, best_length, history).
# history[g] = best length found up to generation g (for the convergence plot).
# memetic=True applies 2-opt to the best route of every generation ("GA with 2-opt").

    # Check the number of cities
    if len(cities) < 2:
        raise ValueError("At least 2 cities are required")

    # Check population size, generations and tournament size
    for name, value, minimum in (
        ("population_size", population_size, 2),
        ("generations", generations, 1),
        ("tournament_k", tournament_k, 1),
    ):
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < minimum
        ):
            raise ValueError(
                f"{name} must be an integer >= {minimum}"
            )
    lengths = [route_length(r, cities) for r in population]    # computed once per route
    i = min(range(len(population)), key=lengths.__getitem__)
    best_route, best_length = population[i][:], lengths[i]
    history = []

    for _ in range(generations):
        order = sorted(range(len(population)), key=lengths.__getitem__)
        new_pop = [population[j][:] for j in order[:elitism]]   # elitism
        new_len = [lengths[j] for j in order[:elitism]]

        while len(new_pop) < population_size:
            p1 = tournament_selection(population, lengths, tournament_k, rng)
            p2 = tournament_selection(population, lengths, tournament_k, rng)
            child = crossover(p1, p2, crossover_method, crossover_rate, rng)
            child = mutate(child, mutation_method, mutation_rate, rng)
            new_pop.append(child)
            new_len.append(route_length(child, cities))

        if memetic:                                             # 2-opt on the best route
            b = min(range(len(new_pop)), key=new_len.__getitem__)
            new_pop[b] = two_opt(new_pop[b], cities)
            new_len[b] = route_length(new_pop[b], cities)

        population, lengths = new_pop, new_len
        b = min(range(len(population)), key=lengths.__getitem__)
        if lengths[b] < best_length:
            best_route, best_length = population[b][:], lengths[b]
        history.append(best_length)

    k = best_route.index(0)           # start the route at city 0
    return best_route[k:] + best_route[:k], best_length, history


if __name__ == "__main__":
    from baselines import brute_force, greedy
    from tsp import random_cities
    cities = random_cities(10, random.Random(42))
    route, length, hist = run_ga(cities, seed=1)
    print("GA length     :", round(length, 2))
    print("Greedy length :", round(route_length(greedy(cities), cities), 2))
    print("Brute force   :", round(route_length(brute_force(cities), cities), 2))
    print("Generation 1 -> last:", round(hist[0], 2), "->", round(hist[-1], 2))