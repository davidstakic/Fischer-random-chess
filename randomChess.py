import random
from constants import *
from print_board import print_board
from copy import deepcopy
import matplotlib.pyplot as plt

class RandomChess:
    def __init__(self, population_size, generations, mutation_rate, elitis_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.optimality_criterion = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        self.best_count = 0
        self.population = []
        self.all_evaluations = []
        self.elitis_rate = elitis_rate

    def generate_individual(self):
        individual = deepcopy(self.optimality_criterion)
        random.shuffle(individual)
        return individual
    
    def generate_population(self):
        self.population = [self.generate_individual() for _ in range(self.population_size)]
    
    def evaluate(self, individual): # OGRANICENJA
        # Provera da li neka figura fali
        piece_counts = {ROOK: 0, KNIGHT: 0, BISHOP: 0, QUEEN: 0, KING: 0}
        for piece in individual:
            piece_counts[piece] += 1

        correct_counts = {ROOK: 2, KNIGHT: 2, BISHOP: 2, QUEEN: 1, KING: 1}
        if any(piece_counts[piece] != correct_counts[piece] for piece in piece_counts):
            return float('-inf')

        # kralj ne sme biti na a i h
        if individual.index(KING) == 0 or individual.index(KING) == 7:
            return float('-inf')

        # kralj mora biti izmedju topova
        king_position = individual.index(KING)
        rook_positions = [individual.index(ROOK)]
        rook_positions.append(individual.index(ROOK, rook_positions[0] + 1))
        rook_positions.sort()
        if not rook_positions[0] < king_position < rook_positions[1]:
            return float('-inf')

        # lovci moraju biti na poljima razlicitih boja
        bishop_positions = [individual.index(BISHOP)]
        bishop_positions.append(individual.index(BISHOP, bishop_positions[0] + 1))
        if (bishop_positions[0] % 2 == bishop_positions[1] % 2):
            return float('-inf')

        correct_pieces = sum(piece == target for piece, target in zip(individual, self.optimality_criterion))

        return correct_pieces

    def select_parents(self):
        selected_parents = []

        shuffled_population = random.sample(self.population, len(self.population))

        for i in range(0, len(shuffled_population), 2):
            parent1 = shuffled_population[i]
            parent2 = shuffled_population[i + 1] if i + 1 < len(shuffled_population) else shuffled_population[i]

            winner = max([parent1, parent2], key=self.evaluate)
            selected_parents.extend([winner, winner])

        return selected_parents

    def crossover(self, parent1, parent2):
        crossover_point1 = random.randint(0, len(parent1) - 1)
        crossover_point2 = random.randint(0, len(parent1) - 1)

        while crossover_point2 == crossover_point1:
            crossover_point2 = random.randint(0, len(parent1) - 1)

        if crossover_point1 > crossover_point2:
            crossover_point1, crossover_point2 = crossover_point2, crossover_point1

        child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
        child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]

        return [child1, child2]

    def mutate(self, children):
        mutated_children = []

        for child in children:
            mutated_child = deepcopy(child)

            for i in range(len(mutated_child)):
                if random.random() < self.mutation_rate:
                    mutated_child[i] = self.generate_individual()[i]
            mutated_children.append(mutated_child)

        return mutated_children
    
    def elitis(self, parents, next_population):
        current_best = parents[0]
        old_ind_size = round(self.population_size*self.elitis_rate)
        parents_sorted = []
        for parent in parents:
            parents_sorted.append([parent, self.evaluate(parent)])
        parents_sorted = sorted(parents_sorted, key=lambda x: x[1], reverse=True)
        parents_sorted = [sublist[0] for sublist in parents_sorted]
        # provera da li se elitna jedinka ponavlja vise od 3 generacije
        if current_best == parents_sorted[0] and self.best_count >= 3:
            self.best_count = 0
            return next_population
        self.best_count += 1
        return parents_sorted[:old_ind_size] + next_population[:(self.population_size-old_ind_size)]

    def evolve(self):
        self.generate_population()

        for generation in range(self.generations):
            parents = self.select_parents()
            next_population = []

            for i in range(0, self.population_size, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1] if i + 1 < len(parents) else parents[0]
                children = self.crossover(parent1, parent2)
                children = self.mutate(children)
                next_population.extend([children[0], children[1]])

            self.population = self.elitis(parents, next_population)

            best_individual = max(self.population, key=self.evaluate)
            evaluate_value = self.evaluate(best_individual)
            self.all_evaluations.append(evaluate_value)

            if evaluate_value < 0:
                print(f"\nThere is no individual in generation {generation + 1} that satisfies constraints")
            else:
                print(f"\nGeneration {generation + 1}, Best Fitness: {self.evaluate(best_individual)}")
                print_board(best_individual)
                print()
        
        if evaluate_value < 0:
            print(f"\nThere is no individual in all generations that satisfies constraints.")
            return None
        return best_individual
    
    def plot_evaluation_through_generations(self):
        y_axis = self.all_evaluations
        plt.plot(y_axis, '-', label='Evaluation')
        plt.title('Evaluations Through Generations')
        plt.legend()
        plt.show()