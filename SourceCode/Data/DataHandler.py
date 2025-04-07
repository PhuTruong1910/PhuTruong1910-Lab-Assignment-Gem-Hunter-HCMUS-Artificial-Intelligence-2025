from Data.Display import display_two_grids
from Data.Display import save_grid_to_file

def load_grid(filename):
    f = open(filename, "r")
    grid = []
    
    line = f.readline()
    while (line):        
        line = line.replace("\n", "")
        grid.append(line.split(", "))        
        line = f.readline()
    
    f.close()

    return grid

# After solving the problem, the program should fill in all blanks with the results.
def fill_result(grid, truth):
    # grid: the 2D list
    # truth: the 1D list containing all unit clauses

    grid = [['T' if i * len(grid[i]) + j + 1 in truth else 'G' if grid[i][j] == '_' else grid[i][j]
                 for j in range(len(grid[i]))] for i in range(len(grid))]

    return grid        

def check_cnf(cnf, bridge):
    undecided_literal = False

    for literal in cnf:
        if bridge.get(literal) == True:
            return True
        # elif bridge.get(literal) is None:
        #     undecided_literal = True
    return False
    # return None if undecided_literal else False