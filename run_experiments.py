import argparse
import csv
import os
import random
import statistics as st
import time
import config
from baselines import brute_force, greedy, two_opt
from ga import run_ga
from tsp import (circle_cities, circle_optimum, grid_cities, grid_optimum,
                 random_cities, route_length)

OUT = "results"


def save(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("saved", path, f"({len(rows)} rows)")


def timed(fn, *args, **kwargs):
    t = time.perf_counter()
    result = fn(*args, **kwargs)
    return result, time.perf_counter() - t


def ga_length(cities, **kwargs):
    (route, length, hist), sec = timed(run_ga, cities, **{**config.GA, **kwargs})
    return length, sec


def baselines(quick):
    runs = 3 if quick else config.RUNS
    rows = []
    for inst in range(2 if quick else config.BASELINE_INSTANCES):
        cities = random_cities(config.BASELINE_N, random.Random(100 + inst))
        r, sec = timed(brute_force, cities)
        rows.append(["Brute force", inst, 0, round(route_length(r, cities), 4), round(sec, 4)])
        r, sec = timed(greedy, cities)
        rows.append(["Greedy", inst, 0, round(route_length(r, cities), 4), round(sec, 6)])
        for seed in range(runs):
            L, sec = ga_length(cities, seed=seed)
            rows.append(["GA", inst, seed, round(L, 4), round(sec, 4)])
            L, sec = ga_length(cities, seed=seed, memetic=True)
            rows.append(["GA with 2-opt", inst, seed, round(L, 4), round(sec, 4)])
        print("  instance", inst, "done")
    save("baselines.csv", ["method", "instance", "run", "length", "time_sec"], rows)


def operators(quick):
    runs = 3 if quick else config.RUNS
    combos = [("ox", "inversion"), ("ox", "swap"), ("pmx", "inversion"), ("pmx", "swap")]
    n = 15 if quick else config.OPERATOR_N
    rows = []
    for inst in range(1 if quick else config.OPERATOR_INSTANCES):
        cities = random_cities(n, random.Random(200 + inst))
        for cx, mu in combos:
            for seed in range(runs):
                L, sec = ga_length(cities, seed=seed, crossover_method=cx, mutation_method=mu)
                rows.append([f"{cx}+{mu}", inst, seed, round(L, 4), round(sec, 4)])
        print("  instance", inst, "done")
    save("operators.csv", ["combination", "instance", "run", "length", "time_sec"], rows)


def scaling(quick):
    sizes = [10, 20] if quick else config.SCALING_SIZES
    runs = 2 if quick else config.SCALING_RUNS
    rows = []
    for n in sizes:
        for inst in range(1 if quick else config.SCALING_INSTANCES):
            cities = random_cities(n, random.Random(1000 * n + inst))
            g, sec = timed(greedy, cities)
            rows.append(["Greedy", n, inst, 0, round(route_length(g, cities), 4), round(sec, 5)])
            t, sec2 = timed(two_opt, g, cities)
            rows.append(["Greedy + 2-opt", n, inst, 0, round(route_length(t, cities), 4), round(sec + sec2, 5)])
            for seed in range(runs):
                L, s = ga_length(cities, seed=seed)
                rows.append(["GA", n, inst, seed, round(L, 4), round(s, 4)])
                L, s = ga_length(cities, seed=seed, memetic=True)
                rows.append(["GA with 2-opt", n, inst, seed, round(L, 4), round(s, 4)])
        print("  n =", n, "done")
    save("scaling.csv", ["method", "n", "instance", "run", "length", "time_sec"], rows)


def convergence(quick):
    runs = 3 if quick else config.RUNS
    cities = random_cities(30, random.Random(200))
    rows = []
    for name, memetic in (("GA", False), ("GA with 2-opt", True)):
        hists = [run_ga(cities, **config.GA, memetic=memetic, seed=s)[2] for s in range(runs)]
        for gen in range(len(hists[0])):
            rows.append([name, gen + 1, round(st.mean(h[gen] for h in hists), 4)])
    save("convergence.csv", ["method", "generation", "mean_best_length"], rows)


def known(quick):
    runs = 3 if quick else config.KNOWN_RUNS
    gens = 100 if quick else config.KNOWN_GENERATIONS
    cases = [("circle 40", circle_cities(40), circle_optimum(40)),
             ("grid 6x6", grid_cities(6, 6), grid_optimum(6, 6)),
             ("grid 8x8", grid_cities(8, 8), grid_optimum(8, 8))]
    if quick:
        cases = cases[:2]
    rows = []
    for name, cities, opt in cases:
        g = greedy(cities)
        rows.append([name, round(opt, 4), "Greedy", 0, round(route_length(g, cities), 4)])
        t = two_opt(g, cities)
        rows.append([name, round(opt, 4), "Greedy + 2-opt", 0, round(route_length(t, cities), 4)])
        for seed in range(runs):
            for label, memetic in (("GA", False), ("GA with 2-opt", True)):
                L, _ = ga_length(cities, seed=seed, memetic=memetic, generations=gens)
                rows.append([name, round(opt, 4), label, seed, round(L, 4)])
        print(" ", name, "done")
    save("known.csv", ["instance", "optimum", "method", "run", "length"], rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["baselines", "operators", "scaling", "convergence", "known", "all"])
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    for name, fn in [("baselines", baselines), ("operators", operators), ("scaling", scaling),
                     ("convergence", convergence), ("known", known)]:
        if a.what in (name, "all"):
            print("==", name)
            fn(a.quick)