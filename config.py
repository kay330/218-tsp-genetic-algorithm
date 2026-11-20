#all experiment settings in one place for reproducibility

GA = dict(population_size=100, generations=300, crossover_rate=0.9,
          mutation_rate=0.2, tournament_k=5, elitism=2)

# Basic experiments
BASIC_SIZES = (10, 20, 30)
BASIC_RUNS = 20

# Extended experiments
RUNS = 30
RUNS_PARAM = 15
RUNS_BIG = 10

# Experiment city sizes
COMPARISON_SIZES = (10, 20, 30)
CONSISTENCY_SIZES = (10, 30)
OPERATOR_N = 30
PARAMETER_N = 30
SCALING_SIZES = (10, 20, 30, 50, 100)

# Demo
DEMO_CITIES = 10
DEMO_SEED = 42
BRUTE_FORCE_LIMIT = 10

# Existing benchmark settings
BASELINE_N = 10
BASELINE_INSTANCES = 5
OPERATOR_INSTANCES = 3
SCALING_INSTANCES = 3
SCALING_RUNS = 5
KNOWN_RUNS = 10
KNOWN_GENERATIONS = 600