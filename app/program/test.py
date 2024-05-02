import unittest
from sudoku_full_board import SudokuGenerator
from sudoku_game_v5 import SudokuGame
from Solver_experiment_unified import UnifiedSolver


class TestSudokuGame(unittest.TestCase):
    def setUp(self):
        self.game_easy = SudokuGame(difficulty='easy')
        self.game_medium = SudokuGame(difficulty='medium')
        self.game_hard = SudokuGame(difficulty='hard')

        # Ensure games are ready with a generated board.
        self.game_easy.generate_game()
        self.game_medium.generate_game()
        self.game_hard.generate_game()
        self.correct_sum = 45 

    def check_unique(self, elements):
        """Helper method to check if all elements in a list are unique (ignoring zero)"""
        elements = [e for e in elements if e != 0]
        return len(elements) == len(set(elements))

    def test_full_board_validity(self):
        """Test that the full board generated is valid: all rows, columns, and blocks have unique non-zero elements."""
        board = self.game_easy.generator.board
        for row in board:
            self.assertTrue(self.check_unique(row), "Row has duplicates or incorrect elements")
        for col in range(9):
            col_elems = [board[row][col] for row in range(9)]
            self.assertTrue(self.check_unique(col_elems), "Column has duplicates or incorrect elements")
        for block in range(9):
            block_elems = []
            start_row, start_col = 3 * (block // 3), 3 * (block % 3)
            for i in range(3):
                for j in range(3):
                    block_elems.append(board[start_row + i][start_col + j])
            self.assertTrue(self.check_unique(block_elems), "Block has duplicates or incorrect elements")

    def test_sums_of_rows_cols_blocks(self):
        """Test that each row, column, and 3x3 block sums to the correct number (45 for a filled board)."""
        board = self.game_easy.generator.board
        for row in board:
            self.assertEqual(sum(row), self.correct_sum, "Row does not sum to 45")
        for col in range(9):
            col_sum = sum(board[row][col] for row in range(9))
            self.assertEqual(col_sum, self.correct_sum, "Column does not sum to 45")
        for block in range(9):
            block_sum = 0
            start_row, start_col = 3 * (block // 3), 3 * (block % 3)
            for i in range(3):
                for j in range(3):
                    block_sum += board[start_row + i][start_col + j]
            self.assertEqual(block_sum, self.correct_sum, "3x3 Block does not sum to 45")

    def test_puzzle_validity(self):
        """Test that the puzzle is valid: rows, columns, and blocks have unique elements where filled and correct sums."""
        self.game_easy.generate_game()
        board = self.game_easy.generator.board
        # Similar tests as full board validity, adjusted for a board that includes zeros (empty cells)
        def get_column(col):
            return [board[row][col] for row in range(9)]
    
        def get_block(block):
            start_row, start_col = 3 * (block // 3), 3 * (block % 3)
            return [board[r][c] for r in range(start_row, start_row + 3) for c in range(start_col, start_col + 3)] 
        for i in range(9):
            row = [num for num in board[i] if num != 0]
            col = [num for num in get_column(i) if num != 0]
            blk = [num for num in get_block(i) if num != 0]
            self.assertEqual(len(row), len(set(row)), "Duplicate in row")
            self.assertEqual(len(col), len(set(col)), "Duplicate in column")
            self.assertEqual(len(blk), len(set(blk)), "Duplicate in block")

    
        # Check sums in rows, columns, and blocks only account for non-zero values being unique
        # We skip the sum check here as the puzzle is not completely filled
    #functions to test solver logic. 
    def test_solver_easy(self):
        """Test that the solver successfully solves an easy difficulty puzzle."""
        solver = UnifiedSolver(self.game_easy.board)
        self.assertTrue(solver.solve(), "Solver failed to solve an easy puzzle")

    def test_solver_medium(self):
        """Test that the solver successfully solves a medium difficulty puzzle."""
        solver = UnifiedSolver(self.game_medium.board)
        self.assertTrue(solver.solve(), "Solver failed to solve a medium puzzle")

    def test_solver_hard(self):
        """Test that the solver successfully solves a hard difficulty puzzle."""
        solver = UnifiedSolver(self.game_hard.board)
        self.assertTrue(solver.solve(), "Solver failed to solve a hard puzzle")
    
    def verify_solution(self, board):
        """Helper method to verify that a solved Sudoku board is correct."""
        correct_sum = 45  # Sum of numbers 1 through 9
        # Check rows, columns and 3x3 blocks
        for i in range(9):
            row = board[i]
            column = [board[j][i] for j in range(9)]
            if sum(row) != correct_sum or sum(column) != correct_sum:
                return False
            if i % 3 == 0:
                for j in range(0, 9, 3):
                    block = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                    if sum(block) != correct_sum:
                        return False
        return True
    
    def test_solution_validity(self):
        """Test that the solutions generated by the solver are valid for each difficulty."""
        for game in [self.game_easy, self.game_medium, self.game_hard]:
            solver = UnifiedSolver(game.board)
            solver.solve()
            self.assertTrue(self.verify_solution(solver.board))
    



# To run the tests
if __name__ == "__main__":
    unittest.main()
