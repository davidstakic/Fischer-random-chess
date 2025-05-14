# Fischer Random Chess Optimization – University Project (Python)

This repository contains a Python implementation of a **genetic algorithm** developed to find valid and optimized starting positions for **Fischer Random Chess (Chess960)**. The project was created as part of a university course focusing on heuristic search and optimization techniques.

## ♟️ Project Overview

**Fischer Random Chess** is a variant of classical chess where the initial position of the pieces on the back rank is randomized, while still following specific constraints (e.g., bishops must be on opposite-color squares, the king must be placed between the rooks, etc.).

The objective of this project was to use a **genetic algorithm** to evolve a population of board configurations toward a solution that:
- Satisfies all **Fischer Random rules**
- Optimizes a defined **fitness/optimality criterion**

## 🧠 Algorithm Highlights

The genetic algorithm used in this project includes the following components:

- **Chromosome Representation:** Each individual represents a possible piece layout on the first rank.
- **Fitness Function:** Measures how well a board satisfies Fischer's constraints and how “optimal” it is based on custom criteria.
- **Selection:** Chooses parent solutions based on fitness (e.g., tournament selection, roulette wheel, etc.).
- **Crossover:** Combines parents to produce offspring.
- **Mutation:** Randomly alters individuals to maintain diversity in the population.
- **Termination:** Stops when a valid (or optimal) configuration is found or after a fixed number of generations.

## 🛠️ Technologies Used

- Python 3

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/davidstakic/Fischer-random-chess.git
