import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("results_scaling.csv")
m = df.groupby(["n_cities", "algorithm"])[["length", "time_sec"]].mean().unstack()
m["length"].plot(marker="o", title="Mean route length vs number of cities")
plt.ylabel("Route length")
plt.savefig("scaling_length.png", dpi=200, bbox_inches="tight")
plt.figure()
m["time_sec"].plot(marker="o", title="Mean runtime vs number of cities")
plt.ylabel("Seconds")
plt.savefig("scaling_time.png", dpi=200, bbox_inches="tight")