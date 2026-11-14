"""Tests for operators.py. Run with:  python -m pytest test_operators.py  (or  python test_operators.py)"""
import random

from operators import (order_crossover, partially_mapped_crossover,
                       swap_mutation, inversion_mutation, crossover, mutate,
                       CROSSOVERS, MUTATIONS)


def is_valid(route, n):
    return sorted(route) == list(range(n))


def test_crossovers_return_valid_permutations():
    rng = random.Random(42)
    for n in (2, 3, 5, 10, 50, 200):
        for _ in range(300):
            p1 = list(range(n)); rng.shuffle(p1)
            p2 = list(range(n)); rng.shuffle(p2)
            for name, op in CROSSOVERS.items():
                child = op(p1, p2, rng)
                assert is_valid(child, n), f"{name} produced invalid child for n={n}"


def test_crossover_does_not_modify_parents():
    rng = random.Random(1)
    p1, p2 = list(range(10)), list(reversed(range(10)))
    c1, c2 = p1[:], p2[:]
    for op in CROSSOVERS.values():
        op(p1, p2, rng)
    assert p1 == c1 and p2 == c2


def test_identical_parents_give_same_child():
    rng = random.Random(3)
    p = list(range(12)); rng.shuffle(p)
    for op in CROSSOVERS.values():
        assert op(p, p[:], rng) == p


def test_mutations_return_valid_permutations():
    rng = random.Random(7)
    for n in (2, 5, 30):
        for _ in range(300):
            r = list(range(n)); rng.shuffle(r)
            for name, op in MUTATIONS.items():
                assert is_valid(op(r, 1.0, rng), n), name


def test_mutation_rate_zero_changes_nothing():
    rng = random.Random(5)
    r = list(range(20)); rng.shuffle(r)
    for op in MUTATIONS.values():
        assert op(r, 0.0, rng) == r


def test_mutation_rate_one_changes_route():
    rng = random.Random(5)
    r = list(range(20))
    assert swap_mutation(r, 1.0, rng) != r          # swaps two distinct positions
    # inversion of a segment of length >= 2 always changes the route
    assert inversion_mutation(r, 1.0, rng) != r


def test_mutation_does_not_modify_input():
    rng = random.Random(9)
    r = list(range(10)); copy = r[:]
    swap_mutation(r, 1.0, rng); inversion_mutation(r, 1.0, rng)
    assert r == copy


def test_reproducible_with_seed():
    p1 = list(range(15)); p2 = list(reversed(range(15)))
    a = order_crossover(p1, p2, random.Random(123))
    b = order_crossover(p1, p2, random.Random(123))
    assert a == b


def test_wrappers():
    rng = random.Random(0)
    p1, p2 = list(range(10)), list(reversed(range(10)))
    assert crossover(p1, p2, "ox", crossover_rate=0.0, rng=rng) == p1   # cloning
    assert is_valid(crossover(p1, p2, "pmx", crossover_rate=1.0, rng=rng), 10)
    assert is_valid(mutate(p1, "swap", 1.0, rng), 10)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)