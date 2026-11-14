"""
operators.py - Genetic operators for the TSP Genetic Algorithm (CSCI218, Topic 9)

Data format (agreed by the whole team)
--------------------------------------
    route  : list[int]   a permutation of city indices, e.g. [3, 0, 7, 1, ...]
                         every city appears exactly once; the tour implicitly
                         returns from the last city to the first.
    cities : list[tuple[float, float]]   (x, y) coordinates (not needed here:
                         operators only rearrange indices).

Every operator
  * takes route(s) and returns a NEW list (parents are never modified),
  * always returns a valid permutation (no duplicates, no missing cities),
  * accepts an optional `rng` (random.Random) so runs are reproducible.
    If rng is None, the global `random` module is used.

Crossover operators (2 parents -> 1 child)
    order_crossover (OX)             - preserves relative ORDER of cities
    partially_mapped_crossover (PMX) - preserves absolute POSITION of cities

Mutation operators (1 route -> 1 route)
    swap_mutation       - exchanges two cities
    inversion_mutation  - reverses a segment (a "2-opt style" move)

Registries CROSSOVERS and MUTATIONS let ga.py / run_experiments.py pick an
operator by name, e.g. CROSSOVERS["ox"](p1, p2).
"""

import random
from typing import Callable, Dict, List, Optional

Route = List[int]


def _get_rng(rng: Optional[random.Random]):
    """Return the supplied Random instance, or the global random module."""
    return rng if rng is not None else random


# ---------------------------------------------------------------------------
# Crossover
# ---------------------------------------------------------------------------
def order_crossover(parent1: Route, parent2: Route,
                    rng: Optional[random.Random] = None) -> Route:
    """
    Order Crossover (OX1, Davis 1985).

    1. Pick two cut points a <= b.
    2. Copy parent1[a:b+1] into the child at the same positions.
    3. Fill the remaining slots, starting right after the second cut point and
       wrapping around, with the cities of parent2 in the order they appear in
       parent2 (starting after the second cut point), skipping any city that
       is already in the child.

    Good for TSP because the *order* of cities (neighbour relationships) is
    what defines a tour, and OX passes on a contiguous sub-path from one
    parent and the relative order of the rest from the other.

    Example (cut a=3, b=5):
        p1 = [1 2 3 | 4 5 6 | 7 8 9]
        p2 = [9 3 7 | 8 2 6 | 5 1 4]
        child = [7 8 2 | 4 5 6 | 1 9 3]   (a valid permutation)
    (parent2 read from after the 2nd cut: 5 1 4 9 3 7 8 2 6; drop 4,5,6 ->
     1 9 3 7 8 2, written into slots 6,7,8,0,1,2)

    Complexity: O(n).
    """
    r = _get_rng(rng)
    n = len(parent1)
    if n < 2:
        return parent1[:]
    a, b = sorted(r.sample(range(n), 2))

    child: List[Optional[int]] = [None] * n
    child[a:b + 1] = parent1[a:b + 1]
    used = set(parent1[a:b + 1])

    # Cities of parent2 in order, starting just after the second cut point.
    fill = [parent2[(b + 1 + i) % n] for i in range(n)]
    fill = [c for c in fill if c not in used]

    # Write them into the empty slots, also starting after the second cut point.
    pos = (b + 1) % n
    for city in fill:
        while child[pos] is not None:
            pos = (pos + 1) % n
        child[pos] = city
    return child  # type: ignore[return-value]


def partially_mapped_crossover(parent1: Route, parent2: Route,
                               rng: Optional[random.Random] = None) -> Route:
    """
    Partially Mapped Crossover (PMX, Goldberg & Lingle 1985).

    1. Pick two cut points a <= b and copy parent1[a:b+1] into the child.
    2. For each city x of parent2[a:b+1] that is NOT in the copied segment,
       find where it should go: look at the city y that parent1 has at x's
       position in parent2; follow the mapping x -> y -> ... until reaching a
       free slot (a position outside the copied segment) and place x there.
    3. Fill all remaining slots directly from parent2.

    Preserves the absolute POSITION of cities from both parents as much as
    possible. Used as the second operator so we can compare order-preserving
    (OX) vs position-preserving (PMX) crossover in the experiments.

    Complexity: O(n).
    """
    r = _get_rng(rng)
    n = len(parent1)
    if n < 2:
        return parent1[:]
    a, b = sorted(r.sample(range(n), 2))

    child: List[Optional[int]] = [None] * n
    child[a:b + 1] = parent1[a:b + 1]
    segment = set(parent1[a:b + 1])
    pos_in_p2 = {city: i for i, city in enumerate(parent2)}

    for i in range(a, b + 1):
        x = parent2[i]
        if x in segment:
            continue
        j = i
        while a <= j <= b:               # follow the mapping chain out of the segment
            y = parent1[j]
            j = pos_in_p2[y]
        child[j] = x

    for i in range(n):                   # remaining slots come straight from parent2
        if child[i] is None:
            child[i] = parent2[i]
    return child  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Mutation
# ---------------------------------------------------------------------------
def swap_mutation(route: Route, mutation_rate: float = 0.2,
                  rng: Optional[random.Random] = None) -> Route:
    """
    Swap mutation (per-individual probability).

    With probability `mutation_rate`, pick two distinct positions and exchange
    their cities. Small, local change: keeps most of the tour intact, which
    helps fine-tuning late in the search.

    Complexity: O(1) (plus O(n) to copy the route).
    """
    r = _get_rng(rng)
    child = route[:]
    if len(child) >= 2 and r.random() < mutation_rate:
        i, j = r.sample(range(len(child)), 2)
        child[i], child[j] = child[j], child[i]
    return child


def inversion_mutation(route: Route, mutation_rate: float = 0.2,
                       rng: Optional[random.Random] = None) -> Route:
    """
    Inversion mutation (per-individual probability).

    With probability `mutation_rate`, pick two positions i < j and reverse the
    sub-tour route[i:j+1]. Reversing a segment only changes TWO edges of the
    tour (it is exactly a 2-opt move), so it disturbs the tour less than
    swapping two far-apart cities (which breaks up to four edges) and tends to
    remove edge crossings. Standard choice for TSP.

    Complexity: O(n) worst case.
    """
    r = _get_rng(rng)
    child = route[:]
    if len(child) >= 2 and r.random() < mutation_rate:
        i, j = sorted(r.sample(range(len(child)), 2))
        child[i:j + 1] = reversed(child[i:j + 1])
    return child


# ---------------------------------------------------------------------------
# Registries (so other modules can choose operators by name from a config)
# ---------------------------------------------------------------------------
CROSSOVERS: Dict[str, Callable[..., Route]] = {
    "ox": order_crossover,
    "pmx": partially_mapped_crossover,
}

MUTATIONS: Dict[str, Callable[..., Route]] = {
    "swap": swap_mutation,
    "inversion": inversion_mutation,
}


def crossover(parent1: Route, parent2: Route, method: str = "ox",
              crossover_rate: float = 0.9,
              rng: Optional[random.Random] = None) -> Route:
    """
    Convenience wrapper: apply crossover with probability `crossover_rate`,
    otherwise return a copy of parent1 (cloning).
    """
    r = _get_rng(rng)
    if r.random() < crossover_rate:
        return CROSSOVERS[method](parent1, parent2, rng)
    return parent1[:]


def mutate(route: Route, method: str = "inversion", mutation_rate: float = 0.2,
           rng: Optional[random.Random] = None) -> Route:
    """Convenience wrapper: apply the named mutation operator."""
    return MUTATIONS[method](route, mutation_rate, rng)