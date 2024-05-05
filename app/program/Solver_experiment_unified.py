import copy, random
class UnifiedSolver:
    def __init__(self, board, difficulty='auto'): #takes the difficulty level assigned to the sudoku board generated
        self.board = board #expects a 2D list that represents a sudoku grid 
        self.difficulty = difficulty
        self.possible_values = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in board] #Create al list with all possible values in empty cells.
        if difficulty == 'hard': #this part of the code is for the advance_solver. Compute all possible values per cell, and then uses the constrained function to select those cells with the least amount of possible values. 
            self.compute_possible_values()

    def compute_possible_values(self): # Computes possible numbers for each cell based on the current state of the board.
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.update_possible_values(i, j, self.board[i][j], True)

    def update_possible_values(self, row, col, num, is_placing): #once a cell is selected, and a number is input, then it updates the possible values for all affected cells by this input number. 
        affected_cells = self.get_affected_cells(row, col)
        if is_placing: #this determines if the number is being places or not (so to update or not)
            for r, c in affected_cells:
                self.possible_values[r][c].discard(num)
        else:
            for r, c in affected_cells:
                self.possible_values[r][c].add(num)   

    def solve(self): #to choose or decide which method we'll be using
        if self.difficulty == 'easy': #For very easy puzzles, use basic solve as it will be faster if no recursion is needed.
            return self.basic_solve()
        else:
            return self.advanced_solve()

    def basic_solve(self): #solve board using classic backtracking solution
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):  #validating step to follow sudoku's rules. 
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.basic_solve():
                    return True
                self.board[row][col] = 0
        return False
    
    def advanced_solve(self): #solves sudokus using a constrained propagation method by selecting the cells with the fewest possible values. 
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

                # Backtrack here if the number is not valid. 
                self.board[row][col] = 0
                self.possible_values = original_possible_values

        return False

    def find_empty_location(self):  #Finds the first empty location identified by a 0 on the board to attempt to place a number.
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        print("Warning: no empty location found; check if all is complete")
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
                         best_spot = (i,j) #Adding randomisation in solving order for unique solution check (0.9 chosen emperically by allowing the rate to vary and seeing which had highest detection rates).
                    
        return best_spot

    def is_valid(self, row, col, num): #checks the validity of the number input based on Sudoku's rules. 
        if not ( 1 <= num <= 9):
            raise ValueError("Attempted to place an invalid number outside the range 1-9.")
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        start_row = 3 * (row // 3) #create the three by three sub-matrix to check validity in this inner boxes
        start_col = 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def get_affected_cells(self, row, col): # Returns a set of cells that are affected by changes in the given cell and thus only updating these affected cells possible values. 
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
    
    def has_single_solution(self, attempts=50): #check if the puzzle has a single solution, default is 50 attempts as this was found to have 100% accuracy rate for our test set of sudokus without unique solutions. 
        initial_board = copy.deepcopy(self.board)
        self.compute_possible_values()
        self.advanced_solve()
        first_solution = copy.deepcopy(self.board)

        for _ in range(attempts):
            # Reset the board for the next attempt
            self.board = [[cell for cell in row] for row in initial_board]
            self.possible_values = [[set(range(1, 10)) if cell == 0 else set() for cell in row] for row in self.board]
            
            self.compute_possible_values()
            self.advanced_solve()
            current_solution = copy.deepcopy(self.board)

            if current_solution != first_solution:
                return False

        return True


