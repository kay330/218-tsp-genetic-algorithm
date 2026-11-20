
import os
import pandas as pd
import matplotlib.pyplot as plt

# Create a folder for graphs
os.makedirs("figures", exist_ok=True)


# Print average results for each algorithm
def show_results(filename, columns):
    data = pd.read_csv(filename)

    print("\nResults from:", filename)

    results = data.groupby(columns)[["length", "time_sec"]].mean()
    print(results.round(2))

    return data


# 1. Consistency experiment
consistency = show_results(
    "results_consistency.csv",
    ["n_cities", "algorithm"]
)


# 2. Comparison with baseline algorithms
comparison = show_results(
    "results_comparison.csv",
    ["n_cities", "algorithm"]
)

# Compare GA against greedy for 20 and 30 cities
for n in [20, 30]:
    greedy = comparison[
        (comparison["n_cities"] == n) &
        (comparison["algorithm"] == "Greedy")
    ]["length"].mean()

    ga = comparison[
        (comparison["n_cities"] == n) &
        (comparison["algorithm"] == "GA")
    ]["length"].mean()

    improvement = (greedy - ga) / greedy * 100

    print(f"\n{n} cities: GA is {improvement:.2f}% shorter than greedy")


# 3. Crossover and mutation experiments
operators = show_results(
    "results_operators.csv",
    ["algorithm"]
)

operators.boxplot(column="length", by="algorithm")
plt.title("Comparison of GA Operators")
plt.suptitle("")
plt.xlabel("Operator Combination")
plt.ylabel("Route Length")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("figures/operators_boxplot.png")
plt.close()


# 4. Parameter experiments
parameters = show_results(
    "results_parameters.csv",
    ["algorithm"]
)


# 5. Scaling experiment
scaling = show_results(
    "results_scaling.csv",
    ["n_cities", "algorithm"]
)

average = scaling.groupby(
    ["n_cities", "algorithm"]
)["length"].mean().unstack()

average.plot(marker="o")
plt.title("GA Performance with Different City Counts")
plt.xlabel("Number of Cities")
plt.ylabel("Average Route Length")
plt.tight_layout()
plt.savefig("figures/scaling.png")
plt.close()


# 6. Known optimum benchmarks
benchmark = pd.read_csv("results_benchmark.csv")

benchmark["gap_pct"] = (
    (benchmark["length"] - benchmark["optimum"])
    / benchmark["optimum"]
) * 100

print("\nBenchmark Results:")
print(
    benchmark.groupby(["algorithm", "n_cities"])["gap_pct"]
    .mean()
    .round(2)
)

print("\nAnalysis complete! Graphs saved in figures folder.")
