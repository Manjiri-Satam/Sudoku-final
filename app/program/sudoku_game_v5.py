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
            self.num_clues = self.difficulty_levels.get(self.difficulty, self.difficulty_levels['easy'])
            self._remove_numbers_to_puzzle(self.num_clues)
            self.num_empty = self.board_size ** 2 - self.num_clues

            # Check if the puzzle has at least 8 different numbers from 1 to 9
            valid_puzzle = self._check_puzzle_validity()

        return self.generator.board

    def _remove_numbers_to_puzzle(self, initial_clues):
        remaining_clues = self.board_size ** 2 - initial_clues
        tries = 0
        while remaining_clues > 0 and tries < 100:
            self._remove_symmetric_numbers(4 if remaining_clues > 30 else 2)
            remaining_clues -= (4 if remaining_clues > 30 else 2)
            tries += 1
            if not self._has_single_solution():
                # If not a single solution, restore and retry
                self.generator.board = [row[:] for row in self.full_board]
                remaining_clues += (4 if remaining_clues > 30 else 2)
                tries -= 1

    def _remove_symmetric_numbers(self, count):
        cells_to_remove = 4 if count == 4 else 2
        for _ in range(count // 2):
            row1, col1, row2, col2 = self._get_diagonally_opposite_cells()
            self.generator.board[row1][col1] = 0
            self.generator.board[row2][col2] = 0

    def _get_diagonally_opposite_cells(self):
        center = self.board_size // 2
        row = random.randint(0, self.board_size - 1)
        col = random.randint(0, self.board_size - 1)
        row_opp = self.board_size - 1 - row
        col_opp = self.board_size - 1 - col
        return row, col, row_opp, col_opp

    def _has_single_solution(self):
        solver = UnifiedSolver(self.generator.board)
        return not solver.has_single_solution()

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
