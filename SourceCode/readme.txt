HOW TO RUN PROGRAM?

Step 1: 
-Make sure your terminal is at "..\SourceCode" directory

Step 2: 
-Follow this syntax: python main.py --size <number> --solutions <pysat or bruteforce or backtracking>
-Explain: 
   +Number: a integer number which is the size of the grid (5 or 11 or 20) (number x number) 
   +Solutions: the way you choose the solve the problem (pysat or bruteforce or backtracking)
   E.g: python main.py --size 5 --solutions pysat
        python main.py --size 11 --solutions pysat bruteforce
        python main.py --size 11 --solutions pysat bruteforce backtracking
        python main.py --size 11 --solutions bruteforce backtracking pysat