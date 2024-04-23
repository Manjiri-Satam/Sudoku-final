import random
import math

class SudokuGenerator:
    def __init__(self, board_size):
        self.board_size = board_size #Fixed board size for standard Sudoku
        self.subgrid_size = int(math.sqrt(board_size))
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    def generate_full_board(self):
        self._fill_diagonal()
        self._fill_remaining(0, self.subgrid_size)

    def _fill_diagonal(self):
        # Fill diagonal subgrids with random values
        for i in range(0, self.board_size, self.subgrid_size):
            self._fill_subgrid(i, i)

    def _fill_subgrid(self, row, col):
        # Fill a subgrid starting at given row and column
        for i in range(self.subgrid_size):
            for j in range(self.subgrid_size):
                num = self._get_random_num()
                while not self._is_valid_in_subgrid(row, col, num):
                    num = self._get_random_num()
                self.board[row + i][col + j] = num

    def _get_random_num(self):
        # Generate a random number in the range [1, board_size]
        return random.randint(1, self.board_size)

    def _is_valid_in_subgrid(self, row, col, num):
        # Check if the number is not already used in the subgrid
        for i in range(self.subgrid_size):
            for j in range(self.subgrid_size):
                if self.board[row + i][col + j] == num:
                    return False
        return True

    def _fill_remaining(self, i, j):
        # Recursive function to fill the remaining cells
        if i == self.board_size - 1 and j == self.board_size:
            return True

        if j == self.board_size:
            i += 1
            j = 0

        if self.board[i][j] != 0:
            return self._fill_remaining(i, j + 1)

        for num in range(1, self.board_size + 1):
            if self._is_valid(i, j, num):
                self.board[i][j] = num
                if self._fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0

        return False

    def _is_valid(self, i, j, num):
        # Check if it's safe to assign 'num' to cell (i, j)
        return (
            self._is_valid_in_row(i, num)
            and self._is_valid_in_col(j, num)
            and self._is_valid_in_subgrid(i - i % self.subgrid_size, j - j % self.subgrid_size, num)
        )

    def _is_valid_in_row(self, i, num):
        # Check if 'num' is not already used in row 'i'
        return num not in self.board[i]

    def _is_valid_in_col(self, j, num):
        # Check if 'num' is not already used in column 'j'
        return all(self.board[i][j] != num for i in range(self.board_size))

    def print_board(self):
        # Print the Sudoku board with the same visual output as the given code chunk
        for i in range(self.board_size):
            if i % 3 == 0 and i != 0:
                print("-" * (self.board_size * 2 + 3))
            for j in range(self.board_size):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.board[i][j], end=" ")
            print()

if __name__ == "__main__":
    board_size = 9
    sudoku = SudokuGenerator(board_size)
    sudoku.generate_full_board()
    sudoku_full_board = sudoku.print_board()