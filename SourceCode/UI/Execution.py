from Data.DataHandler import load_grid
from Data.DataHandler import save_grid_to_file
from Data.Display import display_result
from Tasks.CNFs_Generation import generate_CNF_s
from Tasks.Backtracking import btSat
from Tasks.BruteForce import bfSat
from Tasks.PySat import pySat

def execute_brute_force(grid, cnfs):
    return bfSat(grid, cnfs)    

def execute_back_tracking(grid, cnfs):
    return btSat(grid, cnfs)

def execute_pysat(grid, cnfs):
    return pySat(grid, cnfs)

def execution(input_file, output_file, solutions):
    grid = load_grid(input_file)

    previous_grid = grid.copy()

    cnfs = generate_CNF_s(grid)

    solvable = False
    total_time = -1.0
    
    for solution in solutions:
        if solution == "bruteforce":
            print("***Brute-force solves CNFs***")
            grid, solvable, total_time = execute_brute_force(grid, cnfs)            
        elif solution == "backtracking":
            print("***Backtracking solves CNFs***")
            grid, solvable, total_time = execute_back_tracking(grid, cnfs)            
        elif solution == "pysat":
            print("***pysat library solves CNFs***")
            grid, solvable, total_time = execute_pysat(grid, cnfs)            
    
        if solvable:
            display_result(previous_grid, grid, total_time)
            print("")

            save_grid_to_file(output_file, grid)
        else:
            print("Unsolvable")