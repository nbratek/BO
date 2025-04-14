import random
import sys
from models import Gene
from genetic_algorithm import GeneticAlgorithm
from chromosome import seat_assignments
from utils.data_reader import input_data_reader
from chromosome import Chromosome


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
        return [Chromosome(seat_assignments(groups, tables), tables, groups) for _ in range(100)]

    genetic_algorithm = GeneticAlgorithm(population_generator=population_generator, selection=GeneticAlgorithm.roulette_selection, stop=lambda _, __, i: i > 1000, mutation_probability=0.3)
    genetic_algorithm.first_generation = population_generator
    solution = genetic_algorithm.simulate(10000)
    # solution = genetic_algorithm.simulate(0)
    print("Solution:", solution)
    # for group in solution.groups: print(group.count, " ", group.reservation, " ", group.preferences, " \n")


if __name__ == '__main__':
    main()