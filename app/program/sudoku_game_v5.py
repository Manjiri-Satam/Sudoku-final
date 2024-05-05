import random
from sudoku_full_board import SudokuGenerator
from Solver_experiment_unified import UnifiedSolver


class SudokuGame:
    def __init__(self, board_size=9, difficulty='easy'):
        self.board_size = board_size
        self.generator = SudokuGenerator(board_size)
        self.difficulty_levels = {
            'easy': random.randint(36, 40),
            'medium': random.randint(32, 35),
            'hard': random.randint(28, 31)
        }
        self.difficulty = difficulty
        self.full_board = None
        self.num_clues = None  # To store the number of clues provided in the puzzle
        self.num_empty = None  # To store the number of empty cells in the puzzle

    def generate_game(self):
        valid_puzzle = False
        while not valid_puzzle:
            # Generate full Sudoku board
            self.generator.generate_full_board()
            self.full_board = [row[:] for row in self.generator.board]

            # Get the number of initial clues based on difficulty level
            self.num_clues = self.difficulty_levels[self.difficulty]
            self._remove_numbers_to_puzzle(self.num_clues)

            # Calculate the number of clues correctly
            self.num_clues = sum(1 for row in self.generator.board for cell in row if cell != 0)
            self.num_empty = self.board_size ** 2 - self.num_clues

            # Check if the puzzle has at least 8 different numbers from 1 to 9
            valid_puzzle = self._check_puzzle_validity()

        return self.generator.board

    def _remove_numbers_to_puzzle(self, initial_clues):
        total_clues_to_leave = initial_clues
        current_clues = self.board_size ** 2  # Start with a full board
        while current_clues > total_clues_to_leave:
            if self._remove_symmetric_numbers():
                current_clues -= 2  # Two numbers are removed in each successful operation

    def _remove_symmetric_numbers(self):
        for _ in range(100):  # A limit to avoid infinite loops
            row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            row_opp, col_opp = self.board_size - 1 - row, self.board_size - 1 - col
            if self.generator.board[row][col] != 0 and self.generator.board[row_opp][col_opp] != 0:
                self.generator.board[row][col] = 0
                self.generator.board[row_opp][col_opp] = 0
                return True  # Successful removal
        return False  # Failed to remove after many tries


    def _has_single_solution(self):
        solver = UnifiedSolver(self.generator.board)
        return not solver.has_single_solution()
        #Replaced with the simpler sanity check below due to the exponential time complexity of checking this for every removal

    def _check_puzzle_validity(self):
        unique_numbers = set()
        for row in self.generator.board:
            unique_numbers.update(filter(lambda x: x != 0, row))
        return len(unique_numbers) >= 8

    def print_board(self):
        print(
            f"Difficulty: {self.difficulty.capitalize()}, Clues Provided: {self.num_clues}, Empty Cells: {self.num_empty}")
        for i in range(self.board_size):
            if i % 3 == 0 and i != 0:
                print("-" * (self.board_size * 2 + 3))
            for j in range(self.board_size):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.generator.board[i][j] if self.generator.board[i][j] != 0 else '.', end=" ")
            print()


# Example usage:
sudoku_game = SudokuGame(difficulty='hard')
sudoku_game.generate_game()
sudoku_game.print_board()

