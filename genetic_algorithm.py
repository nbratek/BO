import random
import copy
from chromosome import Chromosome


class GeneticAlgorithm:
    def __init__(self, population_generator, selection, stop, mutation_probability=0.3):
        self.selection = selection
        self.stop = stop
        self.mutation_probability = mutation_probability
        self.population_generator = population_generator

    @staticmethod
    def roulette_selection(population):
        total_fitness = 0
        for chromosome in population:
            total_fitness += chromosome.fitness()
        if total_fitness == 0:
            return [random.choice(population)]
        pick = random.uniform(0, total_fitness)
        current = 0
        for chromosome in population:
            current += chromosome.fitness()
            if current > pick:
                return [chromosome]
        return [population[-1]]

    def copy(self):
        new_genes = [copy.deepcopy(gene) for gene in self.genes]
        return Chromosome(new_genes, self.tables, self.groups)

    def evolve(self, old_population):
        selected = self.selection(old_population)
        new_population = selected.copy()
        while len(new_population) < len(old_population):
            new_population.extend(self.reproduce(selected))
        return new_population

    def reproduce(self, selected):
        parent1, parent2 = random.choice(selected), random.choice(selected)
        child1, child2 = parent1.cross(parent2)
        if random.random() <= self.mutation_probability:
            child1.mutate()
        if random.random() <= self.mutation_probability:
            child2.mutate()
        return [child1, child2]

    def simulate(self, total_generations):
        population = self.population_generator()
        if not population:
            raise ValueError("Initial population is empty and cannot be evolved.")
        population.sort(key=lambda chromosome: chromosome.fitness(), reverse=True)
        best_found, counter, generation_idx = population[0], 0, 0
        while generation_idx < total_generations and not self.stop(best_found, best_found.fitness(), counter):
            population = self.evolve(population)
            leading_member = max(population, key=lambda member: member.fitness())
            if leading_member.fitness() <= best_found.fitness():
                counter += 1
            else:
                best_found = leading_member
                print("Znaleziono nowe rozwiązanie w generacji : ",generation_idx)
                counter = 0
            generation_idx += 1
        #print(generation_idx)
        return best_found