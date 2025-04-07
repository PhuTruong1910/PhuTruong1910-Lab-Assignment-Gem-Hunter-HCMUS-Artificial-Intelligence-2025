import argparse
from UI.Execution import execution
# Syntax: python main.py --size <number> --solution <pysat or bruteforce or backtracking>

def command_line_interface():

    filename = {}
    filename[5] = ["testcases/input_1.txt", "testcases/output_1.txt"]
    filename[11] = ["testcases/input_2.txt", "testcases/output_2.txt"]
    filename[20] = ["testcases/input_3.txt", "testcases/output_3.txt"]

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--size', type=int, required=True, help="Size of the grid (n x n)")
    parser.add_argument('--solutions', nargs='+', required=True, help="Which way to solve the grid?")    

    args = parser.parse_args()

    if filename.get(args.size) is None:
        print("Invalid size")
    else:
        execution(filename[args.size][0], filename[args.size][1], args.solutions)    