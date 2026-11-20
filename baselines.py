import itertools
import time

from tsp import route_length, distance


def greedy(cities, start=0):
# start at 0, visit the nearest unvisited city until all cities are visited. Returns a route.
    unvisited = list(range(len(cities)))
    unvisited.remove(start)
    route = [start]
    while unvisited:
        current = cities[route[-1]]
        nearest = min(unvisited, key=lambda c: distance(current, cities[c]))
        route.append(nearest)
        unvisited.remove(nearest)
    return route

#this code will run greedy once from EVERY node as the start, and then keep the route with shortest total
#lenght, unlike normal greedy that depends on which city you start from.
def greedy_best_start(cities):
    routes = [greedy(cities, s) for s in range(len(cities))]
    return min(routes, key=lambda r: route_length(r, cities))

# Try every possible route. A route and its reverse have the same length, so one of each pair is skipped.
# brute forces lenght must be equal to or smaller than greedys because it tries every 
# possible route and keeps the shortest one. Since it checks all of them, nothing can
# beat it. Its answer is the best route that exists."
def brute_force(cities):
    best_route = None
    best_length = float("inf")

    for perm in itertools.permutations(range(1, len(cities))): #tries every order of other cities after city 0, covering every possible loop.
        if perm[0] > perm[-1]:      # reverse of a route already tried
            continue
        route = [0] + list(perm)
        length = route_length(route, cities)
        if length < best_length:
            best_length = length
            best_route = route
    return best_route


# 2-opt local search: reverse a section of the route whenever that makes it shorter.
def two_opt(route, cities, max_passes=100):
    
    r = route[:]
    n = len(r)
    if n < 4:
        return r

    def d(a, b):
        return distance(cities[a], cities[b])

    improved, passes = True, 0
    while improved and passes < max_passes:
        improved = False
        passes += 1
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = r[i], r[i + 1]
                c, e = r[j], r[(j + 1) % n]
                if d(a, c) + d(b, e) - d(a, b) - d(c, e) < -1e-12:
                    r[i + 1:j + 1] = reversed(r[i + 1:j + 1])
                    improved = True
    return r


if __name__ == "__main__":
    import random
    random.seed(42)
    test_cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]


# Quick test: run both baselines on the same 10 cities and print each route's
# length and time. The loop avoids repeating the same timing/printing code for
# each method, and perf_counter() is used because time.time() is too coarse
# for greedy (it showed 0.0). 
    for name, fn in [("Greedy", greedy), ("Brute force", brute_force)]:
        t = time.perf_counter()
        r = fn(test_cities)
        print(name, "length:", round(route_length(r, test_cities), 2),
              "& time:", round(time.perf_counter() - t, 3), "s")