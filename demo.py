import argparse
import random
import statistics
import time

import matplotlib

from tsp import route_length
from baselines import greedy, brute_force
from ga import run_ga

BRUTE_FORCE_LIMIT = 10  # more cities than this and brute force takes far too long


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------
def make_cities(n, seed):
    """Random cities on a 100 x 100 map. Same seed = same cities every time."""
    rng = random.Random(seed)
    return [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(n)]


def timed(function, *args, **kwargs):
    """Run a function and also return how many seconds it took."""
    start = time.time()
    result = function(*args, **kwargs)
    return result, time.time() - start


def draw_route(ax, cities, route, title):
    """Draw one route: dots for cities, a line that loops back to the start."""
    xs = [cities[c][0] for c in route] + [cities[route[0]][0]]
    ys = [cities[c][1] for c in route] + [cities[route[0]][1]]
    ax.plot(xs, ys, "-o", markersize=5, linewidth=1.3)
    ax.plot(cities[route[0]][0], cities[route[0]][1], "s", color="red",
            markersize=9, label="start")
    ax.set_title(title, fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal", adjustable="datalim")


# ----------------------------------------------------------------------------
# Parts of the demo
# ----------------------------------------------------------------------------
def run_all_methods(cities, generations, seed):
    """Run greedy, brute force (if small) and the GA. Returns a dict of results."""
    results = {}

    route, secs = timed(greedy, cities)
    results["Greedy"] = (route, route_length(route, cities), secs)

    if len(cities) <= BRUTE_FORCE_LIMIT:
        route, secs = timed(brute_force, cities)
        results["Brute force"] = (route, route_length(route, cities), secs)

    (route, length, history), secs = timed(
        run_ga, cities, generations=generations, seed=seed)
    results["Genetic Algorithm"] = (route, length, secs)
    return results, history


def print_table(results):
    """Print the comparison. 'Gap' = how much longer than the best route we know."""
    best = min(length for _, length, _ in results.values())
    print("\n{:<20}{:>12}{:>12}{:>16}".format(
        "Method", "Length", "Time (s)", "Gap to best"))
    print("-" * 60)
    for name, (_, length, secs) in results.items():
        gap = (length - best) / best * 100
        print("{:<20}{:>12.2f}{:>12.4f}{:>15.1f}%".format(name, length, secs, gap))
    note = "Brute force = true best route (it tries every route)." \
        if "Brute force" in results else \
        "Brute force skipped: too many cities. 'Best' = best of the methods shown."
    print(note)


def show_progress_pictures(cities, results, history, generations, seed, save):
    """
    Figure 1: the GA's best route at 4 stages, same seed each time, so the
    pictures are reproducible. Figure 2: route length vs generation.
    """
    import matplotlib.pyplot as plt

    stages = sorted({1, max(2, generations // 10), max(3, generations // 3), generations})
    fig, axes = plt.subplots(1, len(stages), figsize=(4 * len(stages), 4))
    for ax, g in zip(axes, stages):
        # Re-running with the same seed and fewer generations gives the GA's
        # state at that earlier stage (the GA is deterministic for a given seed).
        route, length, _ = run_ga(cities, generations=g, seed=seed)
        draw_route(ax, cities, route, "Generation {}\nlength {:.1f}".format(g, length))
    fig.suptitle("Genetic Algorithm: best route found so far", fontsize=12)
    fig.tight_layout()
    if save:
        fig.savefig("demo_route_stages.png", dpi=150)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(range(1, len(history) + 1), history, label="GA best so far")
    ax2.axhline(results["Greedy"][1], color="orange", linestyle="--", label="Greedy")
    if "Brute force" in results:
        ax2.axhline(results["Brute force"][1], color="green", linestyle="--",
                    label="Brute force (best possible)")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Route length (shorter is better)")
    ax2.set_title("Convergence: GA vs baselines")
    ax2.legend()
    ax2.grid(alpha=0.3)
    fig2.tight_layout()
    if save:
        fig2.savefig("demo_convergence.png", dpi=150)
        print("\nSaved: demo_route_stages.png, demo_convergence.png")


def compare_operators(cities, generations, runs=5):
    """Try every crossover x mutation pair a few times; show the average length."""
    print("\nOperator comparison (average of {} runs, {} generations)".format(
        runs, generations))
    print("{:<8}{:<12}{:>12}{:>12}".format("Cross", "Mutation", "Mean", "Std dev"))
    print("-" * 44)
    for cx in ("ox", "pmx"):
        for mu in ("swap", "inversion"):
            lengths = [run_ga(cities, generations=generations, crossover_method=cx,
                              mutation_method=mu, seed=s)[1] for s in range(runs)]
            print("{:<8}{:<12}{:>12.2f}{:>12.2f}".format(
                cx.upper(), mu, statistics.mean(lengths), statistics.stdev(lengths)))


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="TSP Genetic Algorithm demo")
    parser.add_argument("--cities", type=int, default=10, help="number of cities")
    parser.add_argument("--generations", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42, help="makes the demo repeatable")
    parser.add_argument("--compare", action="store_true",
                        help="also compare crossover/mutation choices")
    parser.add_argument("--save", action="store_true",
                        help="save pictures as PNG instead of opening windows")
    args = parser.parse_args()

    if args.save:
        matplotlib.use("Agg")  # no window needed

    print("TSP demo: {} cities, {} generations, seed {}".format(
        args.cities, args.generations, args.seed))
    cities = make_cities(args.cities, args.seed)

    results, history = run_all_methods(cities, args.generations, args.seed)
    print_table(results)

    if args.compare:
        compare_operators(cities, args.generations)

    show_progress_pictures(cities, results, history, args.generations, args.seed, args.save)
    if not args.save:
        import matplotlib.pyplot as plt
        plt.show()


if __name__ == "__main__":
    main()
