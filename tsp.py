import random
import math

random.seed(42)  # to make sure same random cities run evertime

#Make 10 random cities, each one is (x, y)
cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]

#Distance between 2 cities
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

#Total length of route (a list of city numbers), coming back to the start
def route_length(route):
    total = 0
    for i in range(len(route)):
        city_a = cities[route[i]]
        city_b = cities[route[(i + 1) % len(route)]]
        total += distance(city_a, city_b)
    return total

# 4. Trying it on the simple route 0, 1, 2, ... 9
route = list(range(10))
print("Cities:", cities)
print("Route length:", round(route_length(route), 2))