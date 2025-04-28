import random
import copy
from chromosome import Chromosome
from models import Gene


class GeneticAlgorithm:


    def __init__(self, population_generator, selection, stop, tables, groups, mutation_probability=0.3, num_parents=3):
        self.selection = selection
        self.stop = stop
        self.mutation_probability = mutation_probability
        self.population_generator = population_generator
        self.num_parents = num_parents
        self.tables = tables
        self.groups = groups

    @staticmethod
    def roulette_selection(population, selected_no=2):
        total_fitness = 0
        for chromosome in population:
            total_fitness += chromosome.fitness()
        if total_fitness == 0:
            return [random.choice(population) for _ in range(selected_no)]
        selected_pop = []
        for i in range(selected_no):
            pick = random.uniform(0, total_fitness)
            current = 0
            for chromosome in population:
                current += chromosome.fitness()
                if current > pick:
                    selected_pop.append(chromosome)
                    break
        return selected_pop

    @staticmethod
    def ranking_selection(population, selected_no=2):
        sorted_population = sorted(population, key=lambda x: x.fitness())

        ranks = list(range(1, len(sorted_population) + 1))

        total_rank = sum(ranks)

        selected_pop = []
        for _ in range(selected_no):
            pick = random.uniform(0, total_rank)
            current = 0
            for chromosome, rank in zip(sorted_population, ranks):
                current += rank
                if current >= pick:
                    selected_pop.append(chromosome)
                    break
        return selected_pop

    def copy(self):
        new_genes = [copy.deepcopy(gene) for gene in self.genes]
        return Chromosome(new_genes, self.tables, self.groups)

    def evolve(self, old_population):
        selected = self.selection(old_population, self.num_parents)
        new_population = selected.copy()
        while len(new_population) < len(old_population):
            new_population.extend(self.reproduce(selected))
        return new_population[:len(old_population)]

    def reproduce(self, selected):
        parents = [random.choice(selected) for _ in range(self.num_parents)]
        children = []

        for _ in range(self.num_parents):
            child_genes = []
            for i in range(len(parents[0].genes)):
                chosen_parent = random.choice(parents)
                chosen_gene = chosen_parent.genes[i]
                new_gene = Gene(chosen_gene.group, chosen_gene.table_id, i)
                child_genes.append(new_gene)

            child = Chromosome(child_genes, self.tables, self.groups)

            if random.random() < self.mutation_probability:
                child.mutate()

            children.append(child)

        return children



    def simulate(self, total_generations):
        best_generation = 0

        population = self.population_generator()
        if not population:
            raise ValueError("Initial population is empty and cannot be evolved.")
        population.sort(key=lambda chromosome: chromosome.fitness(), reverse=True)
        best_found, counter, generation_idx = population[0], 0, 0
        while generation_idx < total_generations and not self.stop(best_found, best_found.fitness(), counter):
            population = self.evolve(population)
            # if generation_idx % 100 == 0:
            #     print("nr of pop" , len(population))
            #     print([mem.fitness() for mem in population])
            leading_member = max(population, key=lambda member: member.fitness())
            if leading_member.fitness() <= best_found.fitness():
                counter += 1
            else:
                best_found = leading_member
                best_generation = generation_idx
                # print("Znaleziono nowe rozwiązanie w generacji : ",generation_idx)
                counter = 0
            generation_idx += 1

        return best_found, best_generation
