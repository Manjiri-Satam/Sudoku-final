# Contains the the Sudoku Class from  (Louis, 29.04)
# Contains Sudoku_Game Class  which is a coppy from sudoku_game_v5 (Manjjiri, 29.04)


class Sudoku:
    def __init__(self, board, difficulty='auto'):
        self.board = board
        self.difficulty = difficulty
        self.possible_values = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in board]
        if difficulty == 'hard':
            self.compute_possible_values()

    def compute_possible_values(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.update_possible_values(i, j, self.board[i][j], True)

    def update_possible_values(self, row, col, num, is_placing):
        affected_cells = self.get_affected_cells(row, col)
        if is_placing:
            for r, c in affected_cells:
                self.possible_values[r][c].discard(num)
        else:
            for r, c in affected_cells:
                self.possible_values[r][c].add(num)

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

    def advanced_solve(self):
        empty = self.find_most_constrained_location()
        if not empty:
            return True
        row, col = empty

        for num in sorted(self.possible_values[row][col]):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                original_possible_values = copy.deepcopy(self.possible_values)
                self.update_possible_values(row, col, num, True)

                if self.advanced_solve():
                    return True

                # Backtrack
                self.board[row][col] = 0
                self.possible_values = original_possible_values

        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def find_most_constrained_location(self):
        min_options = float('inf')
        best_spot = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.possible_values[i][j]) < min_options:
                    min_options = len(self.possible_values[i][j])
                    best_spot = (i, j)
        return best_spot

    def is_valid(self, row, col, num):
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def get_affected_cells(self, row, col):
        affected = set()
        for i in range(9):
            affected.add((row, i))
            affected.add((i, col))
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                affected.add((start_row + i, start_col + j))
        affected.discard((row, col))  # Exclude the cell itself
        return affected
    
    def check_grid_items(self):
        list_bool = []
        for x in range(9):
            list_bool_row = []
            for y in range(9):
                if self.board[x][y] == 0:
                    list_bool_row.append(True)  # Consider empty cells as valid for this context
                else:
                    num = self.board[x][y]
                    # Check for number's occurrence in row, column, and box
                    is_valid = (self.board[x].count(num) == 1 and
                                [self.board[i][y] for i in range(9)].count(num) == 1 and
                                [self.board[i][j] for i in range(x//3*3, (x//3+1)*3)
                                for j in range(y//3*3, (y//3+1)*3)].count(num) == 1)
                    list_bool_row.append(is_valid)
            list_bool.append(list_bool_row)
        return list_bool


def input_num(self, x, y, num):
    """
    Inputs a number in the specified x, y location in self.grid

    Parameters:
    x (int): x location where num should be placed
    y (int): y location where num should be placed
    num (int): number between 1-9 that should be inputted in the
        appropriate x, y location in self.grid
    """
    self.board[x][y] = num


def return_array(self):
    """
    Returns the grid attribute of a Sudoku object
    """
    return self.board


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
        # Placeholder for single solution check logic
        # Implement using a backtracking solver or integrate an existing solver
        return True  # Assuming a placeholder that always returns True

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



'''
def check_grid_items(self):
       """
       Checks each location in self.grid to see if there is more than one
           instance of a number in a given row, column, or box

       Returns:
       list: a 2D list of booleans. Each location corresponds to a location
           in the Sudoku and is False if more than one instance of a number 
           appears in the row, column, or box or is True otherwise
       """
       list_bool = []
       has_added = False
       for x in range(9):
           list_bool_row = []
           for y in range(9):
               if self.grid[x][y] == 0:
                   list_bool_row.append(False)
                   has_added = True
               else:
                   list_r, list_c, list_b = self.create_RCB_lists(x, y)
                   num = self.grid[x][y]

                   # append False if there is more than one instance of
                   #   a number in any of the lists
                   if list_r.count(num) > 1 or list_c.count(num) > 1 or list_b.count(num) > 1:
                       list_bool_row.append(False)
                       has_added = True

                   # if False hasn't been appended, append True
                   if not has_added:
                       list_bool_row.append(True)
                       has_added = True
               has_added = False
           list_bool.append(list_bool_row)

       return list_bool

####### maybe we can use the structure of our is_valid to make a is_valid_grid
def check_grid(self):
       """
       Checks each location in self.grid to ensure a valid Sudoku  

       Returns:
       boolean: True if Sudoku is valid, False if it is not
       """
       for x in range(9):
           for y in range(9):
               if self.grid[x][y] == 0:
                   return False
               else:
                   list_r, list_c, list_b = self.create_RCB_lists(x, y)

                   # check if all numbers 1-9 are in each list
                   for num in range(1, 10):
                       if num not in list_r:
                           return False
                       if num not in list_c:
                           return False
                       if num not in list_b:
                           return False


#######dont think we need this one, just for completenss
def create_RCB_lists(self, x, y):
       """
       Creates three separate lists of all numbers in a given row,
           column, and box

       Parameters:
       x (int): x location that should be checked
       y (int): y location that should be checked

       Returns:
       tuple: three elements in the tuple that correspond to the
           row list, column list, and box list
       """
       # create a list of all numbers in a given row
       list_r = self.grid[x]

       # create a list of all numbers in a given column
       list_c = []
       for i in range(9):
           list_c.append(self.grid[i][y])

       # create a list of all numbers in a given box
       list_b = []
       mod_r = (x + 1) % 3
       mod_c = (y + 1) % 3
       if mod_r == 0:
           list_mr = [x, x - 1, x - 2]
       elif mod_r == 1:
           list_mr = [x, x + 1, x + 2]
       else:
           list_mr = [x - 1, x, x + 1]

       if mod_c == 0:
           list_mc = [y, y - 1, y - 2]
       elif mod_c == 1:
           list_mc = [y, y + 1, y + 2]
       else:
           list_mc = [y - 1, y, y + 1]

       for i in list_mr:
           for j in list_mc:
               list_b.append(self.grid[i][j])

       return (list_r, list_c, list_b)
