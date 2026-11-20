# 218-tsp-genetic-algorithm

CSCI218 group project: solving the Travelling Salesman Problem with a Genetic Algorithm
Group members: Khizra, Sherwin, Krrish , Dalila, Palak

# TSP with a Genetic Algorithm (CSCI218, Topic 9)

This project solves the Travelling Salesman Problem (TSP): given a set of cities,
find the shortest route that visits each city once and returns to the start.
We solve it with a Genetic Algorithm (GA) and compare it with two simple
methods: brute force (tries every route) and greedy nearest neighbour.

## What you need

- Python 3.8 or newer
- The packages in `requirements.txt`

## Install

```
git clone https://github.com/kay330/218-tsp-genetic-algorithm.git
cd REPO
pip install -r requirements.txt
```

## How to run

Run these from the repo folder.

| What you want | Command |
|---|---|
| Live demo (compares greedy, brute force and the GA, draws plots) | `python demo.py` |
| Demo with 30 cities (brute force is skipped, it is too slow) | `python demo.py --cities 30` |
| Demo that also compares crossover and mutation choices | `python demo.py --compare` |
| Demo that saves the plots as PNG files instead of opening windows | `python demo.py --save` |
| Run the experiments (20 seeds each at 10, 20 and 30 cities) | `python run_experiments.py` |
| Run the tests | `python test_operators.py` |

The experiments take a few minutes and write their results to
`experiments_results.csv`. Every run uses fixed random seeds, so results can be
repeated.

## Data format

All files use the same format:

- `cities`: a list of `(x, y)` pairs, for example `[(10, 20), (55, 3), ...]`
- `route`: a list of city numbers that visits each city once, for example `[3, 0, 7, 1, ...]`
- The route returns from the last city to the first, so the length includes that return trip.

## Files

| File | What it does |
|---|---|
| `tsp.py` | Distance between two cities and the total length of a route |
| `baselines.py` | Brute force, greedy nearest neighbour, greedy from the best start city, and 2-opt improvement |
| `ga.py` |GA: population, fitness, tournament selection, the main loop (run_ga), optional 2-opt (memetic=True) |
| `operators.py` | Crossover (Order Crossover, Partially Mapped Crossover) and mutation (swap, inversion) |
| `run_experiments.py` | Runs the algorithms many times and saves results to a CSV file |
| `experiments_results.csv` | Results from the experiments |
| `demo.py` | Live demo: comparison table, route plots at different generations, convergence graph |
| `test_operators.py` | Tests for the crossover and mutation operators |
| `requirements.txt` | Python packages needed |
| `test_core.py` |  |

## How the GA works (short version)

1. Start with a population of random routes.
2. Pick good routes as parents (tournament selection: pick a few at random, keep the shortest).
3. Combine two parents into a child with crossover.
4. Randomly change the child a little with mutation.
5. Keep the best routes unchanged (elitism) and repeat for many generations.

## Notes

- Brute force tries every order of the cities, so it is only practical for about 10 cities or fewer.
- The GA and greedy can be run on any number of cities.
