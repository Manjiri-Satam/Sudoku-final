import unittest
from sudoku_full_board import SudokuGenerator
from sudoku_game_v5 import SudokuGame
from Solver_experiment_unified import UnifiedSolver
import logging
from sudoku_game_v5 import SudokuGame
from Solver_experiment_unified import UnifiedSolver

class TestSudokuGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate games once for all tests to reduce setup time for each test
        cls.game_easy = SudokuGame(difficulty='easy')
        cls.game_easy.generate_game()
        cls.game_medium = SudokuGame(difficulty='medium')
        cls.game_medium.generate_game()
        cls.game_hard = SudokuGame(difficulty='hard')
        cls.game_hard.generate_game()
        cls.correct_sum = 45  # Sum of numbers 1 through 9 expected in each row, column, and block

    def test_solver_uniqueness(self):
        """Test that the Sudoku solver finds a unique solution for each board."""
        games = {
        'easy': self.game_easy,
        'medium': self.game_medium,
        'hard': self.game_hard
        }

        for difficulty, game in games.items():
            board = game.generator.board.copy()
            solver = UnifiedSolver(board)
            solution1 = solver.solve()
            self.assertIsNotNone(solution1, f"No solution found for {difficulty} puzzle")

            solver = UnifiedSolver(board)
            solution2 = solver.solve()
            self.assertEqual(solution1, solution2, f"Multiple solutions found for {difficulty} puzzle")
        
    def check_unique(self, elements):
        """Helper method to check if all elements in a list are unique (ignoring zero)"""
        elements = [e for e in elements if e != 0]
        return len(elements) == len(set(elements))

    def check_board_validity(self, board):
        """Utility function to check that all rows, columns, and blocks are unique."""
        for i in range(9):
            row = [num for num in board[i] if num != 0]
            col = [board[j][i] for j in range(9) if board[j][i] != 0]
            start_row, start_col = 3 * (i // 3), 3 * (i % 3)
            block = [board[r][c] for r in range(start_row, start_row + 3) for c in range(start_col, start_col + 3) if board[r][c] != 0]

            assert len(set(row)) == len(row), f"Duplicate in row {i}"
            assert len(set(col)) == len(col), f"Duplicate in column {i}"
            assert len(set(block)) == len(block), f"Duplicate in block starting at {start_row},{start_col}"

    def test_full_board_validity(self):
        """Test full board validity for easy difficulty."""
        self.check_board_validity(self.game_easy.generator.board)

    def test_sums_of_rows_cols_blocks(self):
        """Test sums of rows, columns, and blocks for medium difficulty."""
        board = self.game_medium.generator.board
        for index in range(9):
            row = board[index]
            col = [board[row][index] for row in range(9)]
            start_row, start_col = 3 * (index // 3), 3 * (index % 3)
            block = [board[start_row + i][start_col + j] for i in range(3) for j in range(3)]

            self.assertEqual(sum(row), self.correct_sum, "Row does not sum to correct value")
            self.assertEqual(sum(col), self.correct_sum, "Column does not sum to correct value")
            self.assertEqual(sum(block), self.correct_sum, "Block does not sum to correct value")

    def test_puzzle_validity(self):
        """Test puzzle validity and solvability for hard difficulty."""
        self.check_board_validity(self.game_hard.generator.board)
        solver = UnifiedSolver(self.game_hard.generator.board)
        self.assertTrue(solver.solve(), "Generated puzzle is unsolvable")

    def test_solution_validity(self):
        """Test solution validity across all difficulties."""
        for game in [self.game_easy, self.game_medium, self.game_hard]:
            solver = UnifiedSolver(game.generator.board)
            self.assertTrue(solver.solve(), f"Solver failed for {game.difficulty} difficulty")
            self.assertTrue(self.verify_solution(solver.board), "Invalid solution for a sudoku puzzle.")

    def verify_solution(self, board):
        """Check if the solution is valid by ensuring each row, column, and block sums up to the correct sum."""
        for i in range(9):
            row = board[i]
            col = [board[j][i] for j in range(9)]
            start_row, start_col = 3 * (i // 3), 3 * (i % 3)
            block = [board[start_row + r][start_col + c] for r in range(3) for c in range(3)]

            if not (sum(row) == sum(col) == sum(block) == self.correct_sum):
                return False
        return True
    def run_tests(verbosity=2):
        # Create a test suite
        suite = unittest.TestSuite()
        
        # Add tests from your TestSudokuGame test case class
        # This method automatically discovers all methods that start with 'test'
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSudokuGame))
        
        # Create a test runner that will display detailed results
        runner = unittest.TextTestRunner(verbosity=verbosity)
        
        # Run the tests
        runner.run(suite)
# To run the tests
if __name__ == "__main__":
    unittest.main()
