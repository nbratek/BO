import pandas as pd
from scipy.stats import f_oneway

roulette_df = pd.read_csv("results/results_roulette_big_example_3.csv", sep=";")
selection_df = pd.read_csv("results/results_selection_big_example_3.csv", sep=";")

roulette_groups = [group["Fitness"].values for _, group in roulette_df.groupby("Liczba rodziców")]
selection_groups = [group["Fitness"].values for _, group in selection_df.groupby("Liczba rodziców")]
anova_roulette = f_oneway(*roulette_groups)
anova_selection = f_oneway(*selection_groups)

print("anova_roulette: ", anova_roulette)
print("anova_selection:", anova_selection)