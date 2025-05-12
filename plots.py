import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results/results_roulette_big_example_3.csv", sep=";")
subset = df[df["Liczba rodziców"] == 2]

plt.hist(subset["Fitness"], bins=10)
plt.title("Histogram fitness - ruletka, 2 rodziców")
plt.xlabel("Wartość fitness")
plt.ylabel("Liczba wystąpień")
plt.show()
