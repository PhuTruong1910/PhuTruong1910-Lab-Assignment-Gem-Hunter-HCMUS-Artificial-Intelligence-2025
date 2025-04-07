import time
from Data.DataHandler import check_cnf
from Data.DataHandler import fill_result

def back_tracking_SAT(cnfs, current_row, literals):
    if current_row == len(cnfs):
        return [], True

    clause = cnfs[current_row]
    satisfied = False
    undecided_literals = []
    
    for lit in clause:
        val = literals.get(lit)
        if val is True:
            satisfied = True
            break
        elif val is None:
            undecided_literals.append(lit)
    
    if satisfied:
        return back_tracking_SAT(cnfs, current_row + 1, literals)
    
    if undecided_literals:
        for lit in undecided_literals:            
            literals[lit] = True
            literals[-lit] = False

            res, solvable = back_tracking_SAT(cnfs, current_row + 1, literals)
            if solvable:
                res += [lit]
                return res, True
            
            literals[lit] = False
            literals[-lit] = True

            res, solvable = back_tracking_SAT(cnfs, current_row + 1, literals)
            if solvable:
                res += [-lit]
                return res, True
            
            del literals[lit]
            del literals[-lit]            

        return [], False 
    else:        
        return [], False 
    
def btSat(grid, cnfs):
    starting_row = 0
    literals = {}

    start_time = time.time()
    result, solvable = back_tracking_SAT(cnfs, starting_row, literals)
    end_time = time.time()

    total_time = end_time - start_time

    grid = fill_result(grid, result)
    return grid, solvable, total_time