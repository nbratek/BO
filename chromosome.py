from models import Gene
import random


class Chromosome:
    def __init__(self, genes, tables):
        self.genes = genes
        self.tables = tables

    def __repr__(self):
        return f"<Chromosome with {len(self.genes)} genes at {id(self)}>"

    def __str__(self):
        gene_details = ', '.join(str(gene) for gene in self.genes)
        return f"Chromosome with {len(self.genes)} genes: [{gene_details}]"

    def __len__(self):
        return len(self.genes)

    def fitness(self):
        window_tables = [0, 2, 4]
        score = 0
        table_usage = {table_id: 0 for table_id in range(len(self.tables))}
        for gene in self.genes:
            table_usage[gene.table_id] += gene.group.count
            if gene.group.preferences.get("window") and gene.table_id in window_tables:
                score += 10
        for table_id, used_capacity in table_usage.items():
            if used_capacity > self.tables[table_id].capacity:
                score -= (used_capacity - self.tables[table_id].capacity) * 5
        return score

    def cross(self, other):
        common_genes = set()
        for gene in self.genes:
            if gene in other.genes:
                common_genes.add(gene)
        new_genes1 = list(common_genes)
        new_genes2 = list(common_genes)
        new_genes1 += self.unique_genes(other, new_genes1)
        new_genes2 += other.unique_genes(self, new_genes2)
        return Chromosome(new_genes1, self.tables), Chromosome(new_genes2, other.tables)

    def unique_genes(self, other, current_genes):
        used_tables = set()
        used_groups = set()
        unique_genes = set()
        for gene in current_genes:
            used_tables.add(gene.table_id)
        for gene in current_genes:
            used_groups.add(gene.group_id)
        for gene in self.genes:
            if gene.table_id not in used_tables and gene.group_id not in used_groups and gene not in other.genes:
                unique_genes.add(gene)
        return unique_genes

    def mutate(self):
        if len(self.genes) < 2:
            return
        mutated_gene_idx = random.randint(0, len(self.genes) - 1)
        mutated_gene = self.genes[mutated_gene_idx]
        used_tables = set()
        possible_tables = []
        for gene in self.genes:
            if gene != mutated_gene:
                used_tables.add(gene.table_id)
        for i, table in enumerate(self.tables):
            if table.capacity >= mutated_gene.group.count and i not in used_tables:
                possible_tables.append(i)
        if not possible_tables:
            return
        new_table_id = random.choice(possible_tables)
        new_gene = Gene(mutated_gene.group, new_table_id, mutated_gene.group_id)
        self.genes[mutated_gene_idx] = new_gene


def seat_assignments(groups, tables):
    genes = []
    table_assigned = [False] * len(tables)
    group_assigned = [False] * len(groups)
    # if len(groups) > len(tables):
    #     groups = groups[:len(tables)]

    for group_id, group in enumerate(groups):
        if not group_assigned[group_id]:
            possible_tables = []
            for i, table in enumerate(tables):
                if group.count <= table.capacity and not table_assigned[i]:
                    possible_tables.append(i)
            if possible_tables:
                chosen_table = random.choice(possible_tables)
                genes.append(Gene(group, chosen_table, group_id))
                table_assigned[chosen_table] = True
                group_assigned[group_id] = True
    return genes