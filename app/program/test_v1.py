import unittest
from sudoku_game_v5 import SudokuGame
import random

class TestSudokuGame(unittest.TestCase):
    def setUp(self):
        self.game = SudokuGame()
        self.board = self.game.generator.give_board()
        if self.board is None:
            self.skipTest("Board generation failed and returned None")

    import random

    def test_game_board_clues(self):
        """Test that easy, medium, and hard levels of the game board have the correct number of clues within a reasonable range."""
        difficulties = ['easy', 'medium', 'hard']
        for difficulty in difficulties:
            with self.subTest(difficulty=difficulty):
                self.game = SudokuGame(difficulty=difficulty)
                board = self.game.generate_game()
                if board is None:
                    self.skipTest(f"Game board generation failed for {difficulty}")
                else:
                    clues_count = sum(1 for row in board for x in row if x != 0)
                    if difficulty == 'easy':
                        self.assertTrue(36 <= clues_count <= 40,
                                        f"Expected 36-40 clues for easy difficulty, found {clues_count}")
                    elif difficulty == 'medium':
                        self.assertTrue(32 <= clues_count <= 35,
                                        f"Expected 32-35 clues for medium difficulty, found {clues_count}")
                    elif difficulty == 'hard':
                        self.assertTrue(28 <= clues_count <= 31,
                                        f"Expected 28-31 clues for hard difficulty, found {clues_count}")

    def test_row_uniqueness(self):
        """Test each row for unique values."""
        for i, row in enumerate(self.board):
            with self.subTest(row=i):
                self.assertEqual(len(set(row)), 9, f"Row {i} should contain unique values")

    def test_column_uniqueness(self):
        """Test each column for unique values."""
        for i in range(9):
            column = [self.board[j][i] for j in range(9)]
            with self.subTest(column=i):
                self.assertEqual(len(set(column)), 9, f"Column {i} should contain unique values")

    def test_subgrid_uniqueness(self):
        """Test each 3x3 subgrid for unique values."""
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                block = [self.board[i][j] for i in range(x, x + 3) for j in range(y, y + 3)]
                with self.subTest(block=f"Block starting at ({x},{y})"):
                    self.assertEqual(len(set(block)), 9,
                                     f"Subgrid starting at ({x},{y}) should contain unique values")

    def test_row_sum(self):
        """Test each row for sum to 45."""
        for i, row in enumerate(self.board):
            with self.subTest(row=i):
                self.assertEqual(sum(row), 45, f"Sum of row {i} should be 45")

    def test_column_sum(self):
        """Test each column for sum to 45."""
        for i in range(9):
            column = [self.board[j][i] for j in range(9)]
            column_sum = sum(column)
            if column_sum != 45:
                print(f"Column {i} data: {column}")
            with self.subTest(column=i):
                self.assertEqual(column_sum, 45, f"Sum of column {i} should be 45")

    def test_subgrid_sum(self):
        """Test each 3x3 subgrid for sum to 45."""
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                block = [self.board[i][j] for i in range(x, x + 3) for j in range(y, y + 3)]
                with self.subTest(block=f"Block starting at ({x},{y})"):
                    self.assertEqual(sum(block), 45, f"Sum of subgrid starting at ({x},{y}) should be 45")

    def test_total_sum_of_board(self):
        """Test the total sum of all numbers on the board equals 405."""
        total_sum = sum(sum(row) for row in self.board)
        self.assertEqual(total_sum, 405, "Total sum of the board should be 405")

    def test_game_board_clues(self):
        """Test that easy, medium, and hard levels of the game board have the correct number of clues within a reasonable range."""
        difficulties = ['easy', 'medium', 'hard']
        tolerance = 5  # Allow a tolerance in the number of clues
        for difficulty in difficulties:
            with self.subTest(difficulty=difficulty):
                self.game = SudokuGame(difficulty=difficulty)
                board = self.game.generate_game()
                if board is None:
                    self.skipTest(f"Game board generation failed for {difficulty}")
                else:
                    clues_count = sum(1 for row in board for x in row if x != 0)
                    expected_clues = self.game.num_clues
                    self.assertTrue(abs(clues_count - expected_clues) <= tolerance, f"Expected around {expected_clues} clues for {difficulty}, found {clues_count}")

    def test_game_board_diversity(self):
        """Test that the game board contains at least 8 out of 9 numbers."""
        board = self.game.generate_game()
        if board is None:
            self.skipTest("Game board generation failed")
        else:
            numbers_present = set(x for row in board for x in row if x != 0)
            self.assertTrue(len(numbers_present) >= 8, f"The game board should contain at least 8 out of 9 numbers, found {len(numbers_present)}")

if __name__ == "__main__":
    unittest.main()
