import itertools
import time
from tsp import cities, route_length, distance


def greedy(start=0):
    "nearest neighbour: always go to the closest unvisited city."
    unvisited = list(range(len(cities)))
    unvisited.remove(start)
    route = [start]
    while unvisited:
        current = cities[route[-1]]
        nearest = min(unvisited, key=lambda c: distance(current, cities[c]))
        route.append(nearest)
        unvisited.remove(nearest)
    return route


def brute_force():
    "trying every possible route. Only practical for about 10 cities or fewer."
    best_route = None
    best_length = float("inf")
    for perm in itertools.permutations(range(1, len(cities))):
        route = [0] + list(perm)
        length = route_length(route)
        if length < best_length:
            best_length = length
            best_route = route
    return best_route

"brute forces lenght must be equal to or smaller than greedys"
if __name__ == "__main__":
    t = time.time()
    g = greedy()
    print("Greedy route:", g)
    print("Greedy length:", round(route_length(g), 2), "| time:", round(time.time() - t, 4), "s")

    t = time.time()
    b = brute_force()
    print("Brute force route:", b)
    print("Brute force length:", round(route_length(b), 2), "| time:", round(time.time() - t, 2), "s")