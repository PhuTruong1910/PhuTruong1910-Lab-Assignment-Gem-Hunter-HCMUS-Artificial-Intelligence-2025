import itertools
import time
from Data.DataHandler import check_cnf
from Data.DataHandler import fill_result

def brute_force_SAT(cnfs, current_row, literals, solvable=True):
    if current_row == len(cnfs):
        return [], solvable
    
    previous_state = solvable

    undecided_literals = {i for i in cnfs[current_row] if i not in literals.keys()}    
    undecided_literals = [*undecided_literals]
    
    list_unit_clauses = []
    if undecided_literals:            
        for i in range(len(undecided_literals)):
            list_unit_clauses += [list(comb) for comb in itertools.combinations(undecided_literals, i + 1)]        
        
        for i in range(len(list_unit_clauses)):
            list_unit_clauses[i] += [-lit for lit in undecided_literals if lit not in list_unit_clauses[i]]  

        list_unit_clauses += [[-i for i in undecided_literals]]                         

    additional = {}
    position = 0    
    if undecided_literals: 
        for i in range(len(list_unit_clauses)):
            for lit in list_unit_clauses[i]:
                literals[lit] = True
                literals[-lit] = False 
            
            current_state = check_cnf(cnfs[current_row], literals)

            next_state = True if previous_state and current_state else False

            additional, solvable = brute_force_SAT(cnfs, current_row + 1, literals, next_state)

            if solvable: 
                position = i
                break
            else:
                for lit in list_unit_clauses[i]:                    
                    del literals[lit]
                    del literals[-lit]
    else:
        current_state = check_cnf(cnfs[current_row], literals)
        
        next_state = True if previous_state and current_state else False

        additional, solvable = brute_force_SAT(cnfs, current_row + 1, literals, next_state)    

    if solvable:
        result = []
        if undecided_literals:            
            for lit in list_unit_clauses[position]:
                result.append(lit)
        
        result.extend(additional)
        return result, solvable
    else:
        return [], False

def bfSat(grid, cnfs):
    starting_row = 0
    literals = {}
    estimated_result = True

    start_time = time.time()
    result, real_result = brute_force_SAT(cnfs, starting_row, literals, estimated_result)
    end_time = time.time()

    total_time = end_time - start_time
    
    grid = fill_result(grid, result)
    return grid, real_result, total_time