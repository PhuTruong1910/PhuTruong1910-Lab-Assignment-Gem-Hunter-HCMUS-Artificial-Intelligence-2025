import itertools

def generate_CNF_s(grid):
    clauses = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '_' and grid[i][j] != '0':
                clauses += make_clauses(grid, i, j);
    
    unique_clauses = []
    for clause in clauses:
        if clause not in unique_clauses:
            unique_clauses.append(clause)

    clauses = unique_clauses        

    return clauses

def make_clauses(grid, row , col):
    number_of_rows = len(grid)
    number_of_cols = len(grid[row])
    integer_value = int(grid[row][col])

    atomic_sentence = []

    for i in range(max(0, row - 1), min(number_of_rows, row + 2)):
        for j in range(max(0, col - 1), min(number_of_cols, col + 2)):
            if grid[i][j] == '_':
                atomic_sentence.append(i * number_of_cols + j + 1)            

    number_of_atomic_senteces = len(atomic_sentence)
          
    cnf = []      
    at_most = list(itertools.combinations(atomic_sentence, integer_value + 1))
    cnf += [[-i for i in clause] for clause in at_most]

    at_least = list(itertools.combinations(atomic_sentence, number_of_atomic_senteces + 1 - integer_value))
    cnf += [[i for i in clause] for clause in at_least]
    
    return cnf