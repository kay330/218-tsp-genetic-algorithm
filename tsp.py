import random
import math
#Distance between 2 cities
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

#Total length of route (a list of city numbers), coming back to the start
def route_length(route, cities):
    total = 0
    for i in range(len(route)):
        city_a = cities[route[i]]
        city_b = cities[route[(i + 1) % len(route)]]
        total += distance(city_a, city_b)
    return total

def random_cities(n, rng, size=100):
    # generates random test cities with a fixed seed for reproducibility
    return [(rng.randint(0, size), rng.randint(0, size)) for _ in range(n)]


# on a 30-50 stop problem brute force doesnt work, so to find out if GA is close to the optimal
# we are using benchmarks of idealised shapes like a circle or regular polygon because the optimal 
# route is mathematicallyknown for these shapes. The following functions generate cities in a circle 
# or grid and return the known optimal route length.
def circle_cities(n, radius=50):
    return [(50 + radius * math.cos(2 * math.pi * k / n),
             50 + radius * math.sin(2 * math.pi * k / n)) for k in range(n)]
def circle_optimum(n, radius=50):
    return n * 2 * radius * math.sin(math.pi / n)
def grid_cities(rows, cols, spacing=10):
    return [(c * spacing, r * spacing) for r in range(rows) for c in range(cols)]
def grid_optimum(rows, cols, spacing=10):
   
    assert (rows * cols) % 2 == 0
    return rows * cols * spacing

#Testing
if __name__ == "__main__":
    random.seed(42) 
    test_cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    route = list(range(10))
    print("Cities:", test_cities)
    print("Route length:", round(route_length(route, test_cities), 2))