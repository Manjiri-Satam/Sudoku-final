
def cross(A, B):
    "Cross product of strings in A and strings in B."
    return tuple(a + b for a in A for b in B)

class SudokuMath:
    def __init__(self, values):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.squares = cross(self.rows, self.cols)

        self.values = values
        self.dict = dict(zip(self.squares, values)) #Taking the values and assigning each to a square as a dictionary

        #Work on storing all possible values
        

    def print_dict(self):
        return print(self.dict)
    
    def print_sudoku_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.values[i * 9 + j], end=" ")
            print()
    
    def to_2d_list(self):
        """Converts the current puzzle representation into a 2D list format."""
        grid = []
        for r in self.rows:
            row = []
            for c in self.cols:
                value = self.dict[r + c]
                if value == '.':
                    row.append(0)  
                else:
                    row.append(int(value))
            grid.append(row)
        return grid

puzzle1 = SudokuMath(values='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
puzzle1.print_dict()
puzzle1.print_sudoku_board()

class SudokuSolver:
    def __init__(self, board, difficulty='auto'):
        self.board = board
        self.difficulty = difficulty
        self.possible_values = self.compute_possible_values() if difficulty == 'hard' else None

    def solve(self):
        if self.difficulty == 'easy' or self.difficulty == 'auto':
            return self.basic_solve()
        else:
            return self.advanced_solve()

    def basic_solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.basic_solve():
                    return True

                self.board[row][col] = 0

        return False  

    def is_valid(self, row, col, num):
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True
#tryout
    def find_empty_location(self):
        for i in range(9):  
            for j in range(9):  
                if self.board[i][j] == 0:  
                    return (i, j)  
        return None

#More complex solver
class AdvancedSolver:
    def __init__(self, board):
        #code to be sure that we can read the grid. Then we can think about integration
        self.board = board  # 2D list representation of the Sudoku board
        self.possible_values = self.compute_possible_values()
    def solve(self):
        empty = self.find_most_constrained_location()
        if not empty:
            return True
        row, col = empty

        for num in self.possible_values[row][col]:
            if self.is_valid(row,col,num):
                self.board[row][col]=num
                original_possible_values = self.possible_values[row][col]
                self.update_possible_values(row, col, num, True)

                if self.solve():
                    return True
                self.board[row][col] = 0
                self.update_possible_values(row, col, original_possible_values, False)

        return False

    def compute_possible_values(self):
        possible_values = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    self.update_possible_values(row, col, self.board[row][col], True)
        return possible_values

    def update_possible_values(self, row, col, num, is_placing):
        if is_placing:
            self.possible_values[row][col] = {num}
            for k in range(9):
                self.possible_values[row][k].discard(num)
                self.possible_values[k][col].discard(num)
                self.possible_values[3 * (row // 3) + k // 3][3 * (col // 3) + k % 3].discard(num)
        else:  # Reset possible values when backtracking
            for k in range(9):
                self.possible_values[row][k].add(num)
                self.possible_values[k][col].add(num)
                self.possible_values[3 * (row // 3) + k // 3][3 * (col // 3) + k % 3].add(num)

    def find_most_constrained_location(self):
        min_options = float('inf')
        best_spot = None
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    num_options = len(self.possible_values[row][col])
                    if num_options < min_options:
                        min_options = num_options
                        best_spot = (row, col)
        return best_spot






