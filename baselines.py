import itertools
import time

from tsp import route_length, distance


def greedy(cities, start=0):
    "nearest neighbou will go to the closest unvisited city."
    unvisited = list(range(len(cities)))
    unvisited.remove(start)
    route = [start]
    while unvisited:
        current = cities[route[-1]]
        nearest = min(unvisited, key=lambda c: distance(current, cities[c]))
        route.append(nearest)
        unvisited.remove(nearest)
    return route


def brute_force(cities):
    "trying every possible route. Only practical for about 10 cities or fewer."
    best_route = None
    best_length = float("inf")
    for perm in itertools.permutations(range(1, len(cities))):
        route = [0] + list(perm)
        length = route_length(route, cities)
        if length < best_length:
            best_length = length
            best_route = route
    return best_route

#brute forces lenght must be equal to or smaller than greedys because it tries every 
# possible route and keeps the shortest one. Since it checks all of them, nothing can
# beat it. Its answer is the best route that exists."
if __name__ == "__main__":
    import random
    random.seed(42)
    test_cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    
    t = time.time()
    g = greedy(test_cities)
    print("Greedy route:", g)
    print("Greedy length:", round(route_length(g, test_cities), 2), "& time:", round(time.time() - t, 4), "s")

    t = time.time()
    b = brute_force(test_cities)
    print("Brute force route:", b)
    print("Brute force length:", round(route_length(b, test_cities), 2), "& time:", round(time.time() - t, 2), "s")