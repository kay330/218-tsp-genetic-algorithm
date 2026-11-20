#all experiment settings in one place for reproducibility

GA = dict(population_size=100, generations=300, crossover_rate=0.9,
          mutation_rate=0.2, tournament_k=5, elitism=2)

RUNS = 30                  # GA runs (seeds 0..29) per instance and setting

BASELINE_N = 10            # cities for the brute-force comparison
BASELINE_INSTANCES = 5     # different random city sets

OPERATOR_N = 30            # cities for the operator comparison
OPERATOR_INSTANCES = 3

SCALING_SIZES = [10, 20, 30, 50, 100]
SCALING_INSTANCES = 3
SCALING_RUNS = 5           # fewer runs: n=100 is slower in pure Python

KNOWN_RUNS = 10
KNOWN_GENERATIONS = 600