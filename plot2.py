import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("results/results_roulette_big_example_3.csv", sep=';')


plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Liczba rodziców", y="Czas [s]")
plt.title("Czas wykonania od liczby rodziców (selekcja ruletkowa)")
plt.xlabel("Liczba rodziców")
plt.ylabel("Czas [s]")
plt.tight_layout()
plt.show()
