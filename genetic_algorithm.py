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
            chromosome = Chromosome(child, self.tables, self.groups)
            chromosome = self.fix_chromosome(chromosome)
            children.append(chromosome)



        # if random.random() <= self.mutation_probability:
        #     child1.mutate()
        # if random.random() <= self.mutation_probability:
        #     child2.mutate()
        # return [child1, child2]

        return children

    def fix_chromosome(self, chromosome):
        assigned_groups = {gene.group_id for gene in chromosome.genes}
        all_groups = {i for i in range(len(self.groups))}
        missing_groups = all_groups - assigned_groups

        for missing_group_id in missing_groups:
            if len(chromosome.genes) >= len(self.tables): break
            table = random.choice([i for i in range(len(self.tables))])
            new_gene = Gene(self.groups[missing_group_id],table, missing_group_id)
            chromosome.genes.append(new_gene)

        seen_groups = set()
        unique_genes = []
        for gene in chromosome.genes:
            if gene.group_id not in seen_groups:
                unique_genes.append(gene)
                seen_groups.add(gene.group_id)
        chromosome.genes = unique_genes

        return chromosome


    def simulate(self, total_generations):
        best_generation = 0

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
                best_generation = generation_idx
                # print("Znaleziono nowe rozwiązanie w generacji : ",generation_idx)
                counter = 0
            generation_idx += 1

        return best_found, best_generation
