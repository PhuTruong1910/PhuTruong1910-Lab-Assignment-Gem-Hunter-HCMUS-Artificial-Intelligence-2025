SEPERATOR = '|'

def display_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(f"{grid[i][j]}{', ' if j < len(grid[i]) -1 else ''}", end='')
        
        print(f"{'\n' if i < len(grid) - 1 else ''}", end='')

    print("")

def display_cnf_s(cnf_s):
    for clause in cnf_s:
        print(clause)

def display_two_grids(left_grid, right_grid, seperator=SEPERATOR):
    for i in range(len(left_grid)):
        for j in range(len(left_grid[i])):
            print(left_grid[i][j], end='')
            if j < len(left_grid[i]) - 1:
                print(', ', end='')

        print(f"  {seperator}  ", end='')

        for j in range(len(right_grid[i])):
            print(right_grid[i][j], end='')
            if j < len(right_grid[i]) - 1:
                print(', ', end='')

        print('')    

def save_grid_to_file(filename, grid):
    f = open(filename, "w")
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            f.write(f"{grid[i][j]}{', ' if j < len(grid[i]) - 1 else ''}")         
        
        f.write(f"{'\n' if i < len(grid) - 1 else ''}")

    f.close()

def display_result(previous_grid, solved_grid, executed_time):
    before_script = "Before solving"
    after_script = "After solving"

    real_lenght_of_grid = 3 * len(previous_grid) - 2

    length_to_print_after_script = real_lenght_of_grid - len(before_script) + 2 if real_lenght_of_grid >= len(before_script) else 1

    print(f"{before_script}: {' ' * length_to_print_after_script} {after_script}:")
    display_two_grids(previous_grid, solved_grid)
    print(f"\n===>Executed Time: {executed_time:.5f}(s)")    