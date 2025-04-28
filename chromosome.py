from models import Gene
import random
from itertools import combinations, zip_longest as zip_l
import copy

class Chromosome:
    def __init__(self, genes, tables, groups):
        self.genes = genes  # Każdy gen odpowiada jednej grupie!
        self.tables = tables
        self.groups = groups
        self.all_tables_capacity = sum(table.capacity for table in tables)

    def __repr__(self):
        return f"<Chromosome with {len(self.genes)} genes at {id(self)}>"

    def __str__(self):
        gene_details = '\n '.join(str(gene) for gene in self.genes)
        return f"Assignment:\n {gene_details}\nfitness: {self.fitness()})"

    def __len__(self):
        return len(self.genes)

    def fitness(self):
        score = 0
        table_usage = {table_id: 0 for table_id in range(len(self.tables))}

        w1 = -1 / self.all_tables_capacity  # waga za wolne miejsca
        w2 = 10                              # waga za spełnianie preferencji
        w3 = -15                             # waga za odległość zajętych stolików
        w4 = -50                             # waga za brak przypisania grupy

        assigned_groups = set()

        for gene in self.genes:
            if gene.table_id is not None:
                assigned_groups.add(gene.group)
                table_usage[gene.table_id] += gene.group.count
                for preference in gene.group.preferences.keys():
                    if preference in self.tables[gene.table_id].features:
                        score += w2
                score += (self.tables[gene.table_id].capacity - gene.group.count) * w1

        # Odległości między zajętymi stolikami
        for t1, t2 in combinations(range(len(self.tables)), 2):
            if table_usage[t1] and table_usage[t2]:
                score += w3 / self.tables[t1].distance(self.tables[t2])

        # Kary za brak przypisania grup
        for group in self.groups:
            if group not in assigned_groups:
                score += w4

        # Uwzględnienie rezerwacji
        for group in self.groups:
            if group.reservation and group not in assigned_groups:
                for gene in self.genes:
                    if gene.table_id is not None and not gene.group.reservation:
                        score -= 200
                        break

        # Pojemność stolików
        for table_id, used_capacity in table_usage.items():
            if used_capacity > self.tables[table_id].capacity:
                return float('-inf')

        return score

    def cross(self, other):
        new_genes1 = []
        new_genes2 = []

        for g1, g2 in zip(self.genes, other.genes):
            if random.random() > 0.5:
                new_genes1.append(copy.deepcopy(g1))
                new_genes2.append(copy.deepcopy(g2))
            else:
                new_genes1.append(copy.deepcopy(g2))
                new_genes2.append(copy.deepcopy(g1))

        # Aby zapobiec klonom
        if new_genes1 == self.genes or new_genes2 == self.genes:
            i = random.randint(0, len(new_genes1) - 1)
            new_genes1[i], new_genes2[i] = new_genes2[i], new_genes1[i]

        return Chromosome(new_genes1, self.tables, self.groups), Chromosome(new_genes2, self.tables, self.groups)

    def mutate(self):
        if len(self.genes) == 0:
            return

        idx = random.randint(0, len(self.genes) - 1)
        gene = self.genes[idx]

        possible_tables = [
            i for i, table in enumerate(self.tables)
            if table.capacity >= gene.group.count
        ]
        possible_tables.append(None)

        if possible_tables:
            new_table_id = random.choice(possible_tables)
            self.genes[idx] = Gene(gene.group, new_table_id, idx)

def seat_assignments(groups, tables):
    genes = []
    available_tables = set(range(len(tables)))

    for idx, group in enumerate(groups):
        possible_tables = [
            i for i in available_tables
            if tables[i].capacity >= group.count
        ]

        if possible_tables:
            chosen_table = random.choice(possible_tables)
            genes.append(Gene(group, chosen_table, idx))
            available_tables.remove(chosen_table)
        else:
            genes.append(Gene(group, None, idx))  # brak przypisania

    return genes