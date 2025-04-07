import time
from pysat.solvers import Solver
from Data.DataHandler import fill_result

def pySat(grid, cnf_s):
    s = Solver()

    for clause in cnf_s:
        s.add_clause(clause)

    start_time = time.time()
    solvable = s.solve()
    end_time = time.time()

    if solvable == True:
        model = s.get_model()          
        
        grid = fill_result(grid, model)        

    s.delete()

    run_time = end_time - start_time

    return grid, solvable, run_time