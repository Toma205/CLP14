import random

class Individual:
    def __init__(self, gene_length, target):
        self.gene_length = gene_length
        self.target = target
        self.genes = [random.randint(0, 9) for _ in range(gene_length)]
        self.fitness = 0
        self.calc_fitness()

    def calc_fitness(self):
        # Ideal: genes[0] + genes[1] == target
        s = self.genes[0] + self.genes[1]
        self.fitness = max(0, 100 - abs(self.target - s))  # Higher is better


class Population:
    def __init__(self, size, gene_length, target):
        self.pop_size = size
        self.individuals = [Individual(gene_length, target) for _ in range(size)]
        self.fittest = 0
        self.gene_length = gene_length
        self.target = target
        self.calculate_fitness()

    def get_fittest(self):
        max_fit_individual = max(self.individuals, key=lambda ind: ind.fitness)
        self.fittest = max_fit_individual.fitness
        return max_fit_individual

    def get_second_fittest(self):
        sorted_individuals = sorted(self.individuals, key=lambda ind: ind.fitness, reverse=True)
        return sorted_individuals[1]

    def get_least_fittest_index(self):
        return min(range(self.pop_size), key=lambda i: self.individuals[i].fitness)

    def calculate_fitness(self):
        for ind in self.individuals:
            ind.calc_fitness()
        self.get_fittest()


class SimpleDemoGA:
    def __init__(self, target, k):
        self.population = Population(size=10, gene_length=k, target=target)
        self.fittest = None
        self.second_fittest = None
        self.generation_count = 0
        self.target = target

    def selection(self):
        self.fittest = self.population.get_fittest()
        self.second_fittest = self.population.get_second_fittest()

    def crossover(self):
        point = random.randint(1, self.population.gene_length - 1)
        for i in range(point):
            self.fittest.genes[i], self.second_fittest.genes[i] = self.second_fittest.genes[i], self.fittest.genes[i]

    def mutation(self):
        for ind in [self.fittest, self.second_fittest]:
            mutation_point = random.randint(0, self.population.gene_length - 1)
            ind.genes[mutation_point] = random.randint(0, 9)

    def get_fittest_offspring(self):
        return self.fittest if self.fittest.fitness > self.second_fittest.fitness else self.second_fittest

    def add_fittest_offspring(self):
        self.fittest.calc_fitness()
        self.second_fittest.calc_fitness()
        least_fit_index = self.population.get_least_fittest_index()
        self.population.individuals[least_fit_index] = self.get_fittest_offspring()

    def run(self):
        print(f"Generation {self.generation_count}: Best fitness = {self.population.fittest}")

        while self.fittest_sum() != self.target:
            self.generation_count += 1
            self.selection()
            self.crossover()
            if random.random() < 0.7:
                self.mutation()
            self.add_fittest_offspring()
            self.population.calculate_fitness()

            print(f"Generation {self.generation_count}: Best fitness = {self.population.fittest}, Best genes = {self.population.get_fittest().genes}")

        solution = self.population.get_fittest()
        print(f"\n Solution found in generation {self.generation_count}")
        print(f"Genes: {' '.join(map(str, solution.genes))} → Sum of first two = {solution.genes[0] + solution.genes[1]}")

    def fittest_sum(self):
        best = self.population.get_fittest()
        return best.genes[0] + best.genes[1]


# === Run Case 1 ===
if __name__ == "__main__":
    T = 7
    k = 3
    ga = SimpleDemoGA(target=T, k=k)
    ga.run()