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

#Trying it on the simple route 0, 1, 2, ... 9
if __name__ == "__main__":
    random.seed(42) 
    test_cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
    route = list(range(10))
    print("Cities:", test_cities)
    print("Route length:", round(route_length(route, test_cities), 2))