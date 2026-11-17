import random
from tsp import route_length
from baselines import greedy

def make_cities(n, seed):
    rng = random.Random(seed)
    return [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(n)]

def main():
    cities = make_cities(10, 42)
    route = greedy(cities)
    print("Greedy route:", route)
    print("Greedy length:", round(route_length(route, cities), 2))

if __name__ == "__main__":
    main()
