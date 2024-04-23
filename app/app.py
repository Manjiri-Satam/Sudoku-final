from sudoku_game_v5 import SudokuGame
import copy


class UnifiedSolver:
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
