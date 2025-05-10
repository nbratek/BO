import pandas as pd

df = pd.read_csv("results/results_roulette_input.csv", sep=';')
grouped = df.groupby("Liczba rodziców")

stats = grouped["Fitness"].agg(["mean", "median", "std", "max", "min"])
print(stats)
