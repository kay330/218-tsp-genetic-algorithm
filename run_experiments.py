import csv
import random
import time
from config import BASIC_SIZES, BASIC_RUNS
from baselines import greedy
from ga import run_ga
from tsp import route_length

def generate_cities(n):
    cities=[]
    for i in range(n):
        x=random.randint(0,100)
        y=random.randint(0,100)
        city=(x,y)
        cities.append(city)
    return cities

def run_experiments():
    results=[]
    city_counts=BASIC_SIZES

    for n in city_counts:
        for seed in range(BASIC_RUNS):
            random.seed(seed)
            cities=generate_cities(n)

            start_time=time.time()
            best_route=greedy(cities)
            exec_time=time.time()-start_time
            best_length=route_length(best_route,cities)
            result_row={
                "algorithm": "Greedy",
                "n_cities": n,
                "seed": seed,
                "length":round(best_length,2),
                "time_sec":round(exec_time,4)
            }
            results.append(result_row)

            start_time=time.time()
            ga_route, ga_length, history = run_ga(cities, seed=seed)
            ga_time=time.time()-start_time
            
            ga_result_row={
                "algorithm": "GA",
                "n_cities": n,
                "seed": seed,
                "length":round(ga_length,2),
                "time_sec":round(ga_time,4)
            }
            results.append(ga_result_row)

    file_name="experiments_results.csv"
    with open(file_name,"w",newline="") as file:
        columns=["algorithm","n_cities","seed","length","time_sec"]
        writer=csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print("Done! Results saved to",file_name)

if __name__=="__main__":
    run_experiments()