import random
from constants import *
from print_board import print_board
from copy import deepcopy
import matplotlib.pyplot as plt

class RandomChess:
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.optimality_criterion = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        self.best_count = 0
        self.population = []
        self.all_evaluations = []

    def generate_individual(self):
        individual = deepcopy(self.optimality_criterion)
        random.shuffle(individual)
        return individual
    
    # generate_inital_chromosomes
    def generate_population(self):
        self.population = [self.generate_individual() for _ in range(self.population_size)]
    
    def evaluate(self, individual): # OGRANICENJA
        # Check if any piece is missing
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
        # Tournament selection: Randomly select individuals and choose the one with the highest fitness.
        selected_parents = []

        for _ in range(self.population_size):
            tournament = random.sample(self.population, 2)
            winner = max(tournament, key=self.evaluate)
            selected_parents.append(winner)

        return selected_parents

    def crossover(self, parent1, parent2):
        # Single-point crossover: Choose a random index and swap the portions of the parents.
        crossover_point = random.randint(0, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(self, individual):
        # Randomly mutate positions with a probability defined by mutation_rate.
        mutated_individual = deepcopy(individual)

        for i in range(len(mutated_individual)):
            if random.random() < self.mutation_rate:
                mutated_individual[i] = self.generate_individual()[i]

        return mutated_individual
    
    def elitis(self, parents, next_population, elitis_rate = 0.1):
        # current_best = parents[0]
        old_ind_size = round(self.population_size*elitis_rate)
        parents_sorted = []
        for parent in parents:
            parents_sorted.append([parent, self.evaluate(parent)])
        parents_sorted = sorted(parents_sorted, key=lambda x: x[1], reverse=True)
        parents_sorted = [sublist[0] for sublist in parents_sorted]
        # if current_best == parents_sorted[0] and self.best_count >= 3:
        #     self.best_count = 0
        #     return next_population
        # self.best_count += 1
        return parents_sorted[:old_ind_size] + next_population[:(self.population_size-old_ind_size)]

    def evolve(self):
        for generation in range(self.generations):
            parents = self.select_parents()
            next_population = []

            # Create offspring through crossover and mutation
            for i in range(0, self.population_size, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1] if i + 1 < len(parents) else parents[0]  # Wrap around for odd population size
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                next_population.extend([parent1, parent2, child])

            # Replace the old population with the new one using elitis
            self.population = self.elitis(parents, next_population)

            # Optionally, you can keep track of the best individual in each generation
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