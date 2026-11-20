import random

from tsp import route_length
from baselines import greedy, brute_force, two_opt
from ga import run_ga


def make_cities(n, seed):
    rng = random.Random(seed)
    return [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(n)]


def visits_every_city_once(route, n):
    return sorted(route) == list(range(n))


def test_route_length_known_triangle():
    # 3-4-5 triangle: 3 + 4 + 5 = 12 (includes the trip back to the start)
    cities = [(0, 0), (3, 0), (3, 4)]
    assert abs(route_length([0, 1, 2], cities) - 12) < 1e-9


def test_greedy_visits_every_city_once():
    for seed in range(5):
        cities = make_cities(15, seed)
        assert visits_every_city_once(greedy(cities), 15)


def test_ga_visits_every_city_once():
    for seed in range(3):
        cities = make_cities(15, seed)
        route, length, history = run_ga(cities, population_size=30,
                                        generations=30, seed=seed)
        assert visits_every_city_once(route, 15)
        assert abs(length - route_length(route, cities)) < 1e-9


def test_brute_force_not_longer_than_greedy():
    for seed in range(3):
        cities = make_cities(8, seed)
        best = route_length(brute_force(cities), cities)
        assert best <= route_length(greedy(cities), cities) + 1e-9


def test_ga_same_seed_gives_same_answer():
    cities = make_cities(12, 0)
    first = run_ga(cities, population_size=30, generations=30, seed=7)
    second = run_ga(cities, population_size=30, generations=30, seed=7)
    assert first[0] == second[0]
    assert first[1] == second[1]


def test_ga_history_never_gets_worse():
    cities = make_cities(15, 1)
    _, _, history = run_ga(cities, population_size=30, generations=40, seed=3)
    assert all(history[i + 1] <= history[i] + 1e-9 for i in range(len(history) - 1))


def test_two_opt_never_makes_route_longer():
    rng = random.Random(0)
    for seed in range(10):
        cities = make_cities(15, seed)
        route = list(range(15))
        rng.shuffle(route)
        improved = two_opt(route, cities)
        assert visits_every_city_once(improved, 15)
        assert route_length(improved, cities) <= route_length(route, cities) + 1e-9


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)