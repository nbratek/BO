import random
import sys
from models import Gene
from genetic_algorithm import GeneticAlgorithm
from chromosome import seat_assignments
from utils.data_reader import input_data_reader
from chromosome import Chromosome
import time
import csv

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.json"
    input_path = 'resources/' + filename
    groups, tables = input_data_reader(input_path)
    genes = []
    # for group in groups: print(group.count, " ", group.reservation, " ", group.preferences, " \n")
    for group_id, group in enumerate(groups):
        possible_tables = [i for i, table in enumerate(tables) if group.count <= table.capacity]
        if possible_tables:
            table_id = random.choice(possible_tables)
            genes.append(Gene(group, table_id, group_id))
        else:
            print(f"No table for a group of {group_id} with a number of {group.count} people")

    # chromosome = Chromosome(genes, tables)
    # print("Fitness:", chromosome.fitness())
    run_genetic_algorithm(groups, tables)


def run_genetic_algorithm(groups, tables):
    def population_generator():
        return [Chromosome(seat_assignments(groups, tables), tables, groups) for _ in range(50)]

    d_solutions = []

    with open("results/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["Run ID", "Liczba rodziców", "Generacja", "Fitness", "Czas [s]"])

        for run_id in range(10):
            for i in range(2, 11):
                print("==========", i, " rodziców – uruchomienie", run_id, "==========")

                genetic_algorithm = GeneticAlgorithm(
                    population_generator=population_generator,
                    selection=GeneticAlgorithm.roulette_selection,
                    stop=lambda _, __, i: i > 1500,
                    mutation_probability=0.3,
                    tables=tables,
                    groups=groups,
                    num_parents=i
                )
                genetic_algorithm.first_generation = population_generator()
                start_time = time.time()
                solution, generation = genetic_algorithm.simulate(1500)
                end_time = time.time()
                total_time = end_time - start_time
                writer.writerow([run_id, i, generation, f"{solution.fitness():.4f}", f"{total_time:.4f}"])
                d_solutions.append((run_id, i, generation, solution, total_time))

    # best = max(d_solutions[-9:], key=lambda x: x[3].fitness())


if __name__ == '__main__':
    main()