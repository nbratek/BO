import random
import sys
from models import Gene
from genetic_algorithm import GeneticAlgorithm
from chromosome import seat_assignments
from utils.data_reader import input_data_reader
from chromosome import Chromosome

def get_user_input(prompt, default, cast_func=str, choices=None):
    try:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        if not user_input:
            return default
        value = cast_func(user_input)
        if choices and value not in choices:
            print(f"Invalid choice. Using default: {default}")
            return default
        return value
    except Exception:
        print(f"Invalid input. Using default: {default}")
        return default

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.json"
    input_path = 'resources/' + filename
    groups, tables = input_data_reader(input_path)
    genes = []

    selection_type = None
    nr_of_generations = None
    mutation_probability = None

    selection_input = get_user_input(
        "Select selection method: 'ranking' or 'roulette'",
        "ranking",
        str,
        choices=["ranking", "roulette"]
    )
    selection_type = (
        GeneticAlgorithm.ranking_selection if selection_input == "ranking"
        else GeneticAlgorithm.roulette_selection
    )

    nr_of_generations = get_user_input("Enter number of generations", 1500, int)
    mutation_probability = get_user_input("Enter mutation probability (e.g. 0.3)", 0.3, float)



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
    run_genetic_algorithm(groups, tables, selection_type, nr_of_generations, mutation_probability)


def run_genetic_algorithm(groups, tables, selection_type, nr_of_generations, mutation_probability):
    def population_generator():
        return [Chromosome(seat_assignments(groups, tables), tables, groups) for _ in range(50)]

    # solution = genetic_algorithm.simulate(0)
    d_solutions = []
    for i in range(10):
        solutions = []
        for i in range(2, 11):
            genetic_algorithm = GeneticAlgorithm(population_generator=population_generator,
                                                 selection=selection_type,
                                                 stop=lambda _, __, i: i > 1500, mutation_probability=mutation_probability,
                                                 tables=tables,groups=groups, num_parents=i)
            genetic_algorithm.first_generation = population_generator()
            solution, generation = genetic_algorithm.simulate(nr_of_generations)
            solutions.append((i, generation, solution))
            d_solutions.append(solutions)
            with open(f"results{i}.txt", "w") as f:
                for s in solutions:
                    f.write(f"{s[0]}\t{s[1]}\t{s[2].fitness()}\n")

    # last_solutions = d_solutions[-1]
    # last_solutions.sort(key=lambda x: x[2].fitness(), reverse=True)
    best = max(d_solutions[-1], key=lambda x: x[2].fitness())

    print("Best nr of parents : ", best[0])
    print(best[2])


if __name__ == '__main__':
    main()