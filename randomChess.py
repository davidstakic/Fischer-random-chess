import random
from constants import *

class RandomChess:
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.optimality_criterion = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        self.colors = [WHITE, BLACK]

    def generate_individual(self):
        """
        Generiše jednog pojedinca, tj. nasumičnu šahovsku tablu.
        """
        chess_board = ['' for _ in range(8)]

        for i, piece in enumerate(self.optimality_criterion):
            chess_board[i] = piece

        king_col = random.choice(range(1, 7))
        chess_board[king_col] = KING

        bishop_col = random.choice(range(0, 8, 2))
        chess_board[bishop_col] = BISHOP

        king_col = random.choice([col for col in range(8) if col not in [0, 7]])
        chess_board[king_col] = KING

        return chess_board

    def evaluate_fitness(self, chess_board):
        """
        Evaluirajte prilagođenost pojedinca na osnovu različitih kriterijuma.
        """
        # Primer: Hamming distance između trenutne postavke i standardne šahovske postavke
        standard_board = [['' for _ in range(8)] for _ in range(8)]
        for i, piece in enumerate(self.optimality_criterion):
            standard_board[0][i] = 'W' + piece
            standard_board[7][i] = 'B' + piece

        return sum(1 for i in range(8) for j in range(8) if chess_board[i][j] != standard_board[i][j])

    def crossover(self, parent1, parent2):
        """
        Križanje dva roditelja kako bi se stvorilo dete.
        """
        crossover_point = random.randint(0, 7)
        child = [parent1[i][:crossover_point] + parent2[i][crossover_point:] for i in range(8)]
        return child

    def mutate(self, individual):
        """
        Mutacija jedinke kako bi se uvodila raznovrsnost.
        """
        for i in range(8):
            for j in range(8):
                if random.random() < self.mutation_rate:
                    # Mutacija: promena vrednosti na slučajnu figuru
                    individual[i][j] = random.choice(self.colors) + random.choice(self.optimality_criterion)
        return individual

    def genetic_algorithm(self):
        """
        Genetski algoritam za rešavanje problema Fischerovog nasumičnog šaha.
        """
        population = [self.generate_individual() for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Evaluacija prilagođenosti svake jedinke
            fitness_scores = [self.evaluate_fitness(individual) for individual in population]

            # Izbor roditelja
            parents = random.choices(population, weights=[1/score for score in fitness_scores], k=self.population_size)

            # Križanje roditelja
            offspring = []
            for i in range(0, self.population_size, 2):
                child = self.crossover(parents[i], parents[i + 1])
                offspring.append(self.mutate(child))

            # Zamena starih jedinki sa decom
            population = offspring

            # Prikaz najbolje jedinke u svakoj generaciji
            best_individual = population[fitness_scores.index(min(fitness_scores))]
            print(f"Generacija {generation + 1}, Najbolja prilagođenost: {self.evaluate_fitness(best_individual)}")
            self.print_board(best_individual)

    def print_board(self, chess_board):
        """
        Prikazuje šahovsku tablu.
        """
        for row in chess_board:
            print(' '.join(piece if piece else '.' for piece in row))
        print()

# Primer korišćenja genetskog algoritma
genetic_algorithm = RandomChess(population_size=50, generations=100, mutation_rate=0.1)
genetic_algorithm.genetic_algorithm()
