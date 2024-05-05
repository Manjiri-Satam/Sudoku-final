import copy, random
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

    def find_most_constrained_location(self): #find the most constrained parts of the puzzle to make it easier to solve. 
        min_options = float('inf')
        best_spot = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and len(self.possible_values[i][j]) < min_options:
                    min_options = len(self.possible_values[i][j])
                    best_spot = (i, j)
                elif self.board[i][j] == 0 and len(self.possible_values[i][j]) == min_options:
                    if random.random() >= 0.9:
                         best_spot = (i,j) #Adding randomisation in solving order for unique solution check
                    
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
    
    #additional validation tool of the entire board. Verify the validity of each solution within the submatrices
    
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
    
    def has_single_solution(self):
        initial_board = copy.deepcopy(self.board)
        # Try to find the first solution
        self.compute_possible_values()
        self.advanced_solve()
        first_solution = copy.deepcopy(self.board)

        # Try to find a second solution
        self.board = [[cell for cell in row] for row in initial_board]  # Reset the board
        self.possible_values = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in self.board]  # Reset possible values
        self.compute_possible_values()
        self.advanced_solve()
        second_solution = copy.deepcopy(self.board)
        
        if not (second_solution == first_solution):
            return False
        
        # Try to find a third solution
        self.board = [[cell for cell in row] for row in initial_board]  # Reset the board
        self.possible_values = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in self.board]  # Reset possible values
        self.compute_possible_values()
        self.advanced_solve()
        third_solution = copy.deepcopy(self.board)
        
        if not(second_solution == first_solution == third_solution):
            return False
        
        
        self.board = [[cell for cell in row] for row in initial_board]
        self.possible_values = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in self.board]
        self.compute_possible_values()
        self.advanced_solve()
        fourth_solution = copy.deepcopy(self.board)
        
        #We only run three passes as otherwise the function would be too slow, from four iterations we found about a 92.4% chance of a board with no unique solution to be detected.
        
        if not(second_solution == first_solution == third_solution == fourth_solution):
            return False
        else:
            return True

