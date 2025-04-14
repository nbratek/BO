import random
import copy
from chromosome import Chromosome


class GeneticAlgorithm:


    def __init__(self, population_generator, selection, stop, tables, mutation_probability=0.3, num_parents=3):
        self.selection = selection
        self.stop = stop
        self.mutation_probability = mutation_probability
        self.population_generator = population_generator
        self.num_parents = num_parents
        self.tables = tables

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

    def copy(self):
        new_genes = [copy.deepcopy(gene) for gene in self.genes]
        return Chromosome(new_genes, self.tables, self.groups)

    def evolve(self, old_population):
        selected = self.selection(old_population, self.num_parents)
        new_population = selected.copy()
        while len(new_population) < len(old_population):
            new_population.extend(self.reproduce(selected))
        return new_population[:100]

    def clip(self, parents, gene):
        for parent in parents:
            for g in parent:
                if g.table_id == gene.table_id or g.group_id == gene.group_id:
                    parent.remove(g)
        return parents

    def reproduce(self, selected):
        #parent1, parent2 = random.choice(selected), random.choice(selected)
        parents = [random.choice(selected).genes for _ in range(self.num_parents)]
 #       child1, child2 = parent1.cross(parent2)
        children = []
        for i in range(self.num_parents):
            child = []
            current = copy.deepcopy(parents)
            j = 0
            while not all(not parent for parent in current):
                if current[j % self.num_parents]:
                    child.append(random.choice(current[j % self.num_parents]))
                current = self.clip(current, child[-1])
                j += 1
            children.append(Chromosome(child, self.tables))

        # if random.random() <= self.mutation_probability:
        #     child1.mutate()
        # if random.random() <= self.mutation_probability:
        #     child2.mutate()
        # return [child1, child2]

        return children


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

        return best_found, generation_idx
