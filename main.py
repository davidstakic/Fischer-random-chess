from randomChess import RandomChess
from print_board import *

if __name__ == '__main__':
    genetic_algorithm = RandomChess(population_size=100, generations=50, mutation_rate=0.1)
    best_individual = genetic_algorithm.evolve()

    genetic_algorithm.plot_evaluation_through_generations()
    # print_board(best_individual)