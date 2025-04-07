import random
import copy
import re # Import regular expressions for input parsing
import math # For ceiling function

def is_valid(r, c, rows, cols):
    """Check if the coordinates are within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def count_adjacent_traps(grid, r, c, rows, cols):
    """Counts the number of traps ('T') adjacent to cell (r, c)."""
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip the cell itself
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, rows, cols) and grid[nr][nc] == 'T':
                count += 1
    return count

def generate_solvable_minesweeper_grid(rows, cols, trap_probability, reveal_probability):
    """
    Generates ONE instance of a solvable Minesweeper grid based on probabilities.
    Helper function for the main generation loop.

    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.
        trap_probability (float): Probability of a cell being a trap.
        reveal_probability (float): Probability of revealing a number (1-8).

    Returns:
        tuple: (puzzle_grid, solution_grid, actual_blanks) or (None, None, -1) on error
               puzzle_grid (list[list[str]]): The generated puzzle.
               solution_grid (list[list[str]]): The full solution (for potential reuse).
               actual_blanks (int): The number of blank ('_') cells in puzzle_grid.
    """
    if not (isinstance(rows, int) and rows > 0 and
            isinstance(cols, int) and cols > 0 and
            0.0 <= trap_probability <= 1.0 and
            0.0 <= reveal_probability <= 1.0):
        print("Error: Invalid parameters passed to internal generator.")
        return None, None, -1

    # --- Step 1: Create the full solution grid ---
    solution_grid = [['' for _ in range(cols)] for _ in range(rows)]
    # Place traps (ensure at least one safe cell if possible, otherwise logic breaks)
    trap_count = 0
    for r in range(rows):
        for c in range(cols):
            if random.random() < trap_probability:
                solution_grid[r][c] = 'T'
                trap_count +=1
            else:
                solution_grid[r][c] = 'S'

    # If all cells became traps (unlikely but possible), force one to be safe
    if trap_count == rows * cols and rows * cols > 0:
         rr, rc = random.randint(0, rows-1), random.randint(0, cols-1)
         solution_grid[rr][rc] = 'S'

    # Calculate numbers for safe cells (0-8)
    for r in range(rows):
        for c in range(cols):
            if solution_grid[r][c] == 'S':
                num_adjacent = count_adjacent_traps(solution_grid, r, c, rows, cols)
                solution_grid[r][c] = str(num_adjacent) # Store numbers as strings

    # --- Step 2: Create the puzzle grid based on the solution ---
    puzzle_grid = [['_' for _ in range(cols)] for _ in range(rows)]
    actual_blanks = 0
    possible_hints = [] # Store locations of potential hints (1-8)

    for r in range(rows):
        for c in range(cols):
            cell_value = solution_grid[r][c]
            if cell_value == 'T' or cell_value == '0':
                # Traps and 0s are always hidden
                puzzle_grid[r][c] = '_'
                actual_blanks += 1
            else:
                # It's a numbered cell with value '1' through '8'
                possible_hints.append((r, c)) # Track potential hint location
                if random.random() < reveal_probability:
                    # Reveal the number (1-8)
                    puzzle_grid[r][c] = cell_value
                else:
                    # Keep it hidden
                    puzzle_grid[r][c] = '_'
                    actual_blanks += 1

    # --- Optional Step 3: Ensure at least one hint (1-8) is visible if possible ---
    has_hint = any(cell != '_' for row in puzzle_grid for cell in row)

    # If no hints were revealed *and* there were cells that *could* have been hints
    if not has_hint and possible_hints:
        # Force reveal one of the potential hints (1-8)
        r_reveal, c_reveal = random.choice(possible_hints)
        puzzle_grid[r_reveal][c_reveal] = solution_grid[r_reveal][c_reveal]
        actual_blanks -= 1 # Decrement blank count as we just revealed one

    # Ensure blank count isn't negative (shouldn't happen, but safety check)
    actual_blanks = max(0, actual_blanks)

    return puzzle_grid, solution_grid, actual_blanks


def generate_grid_with_target_blanks(rows, cols, trap_probability,
                                      target_min_blanks, target_max_blanks,
                                      max_attempts=30):
    """
    Attempts to generate a solvable Minesweeper grid with a number of blank
    cells within the specified target range.

    Adjusts the reveal probability iteratively to try and meet the target.

    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.
        trap_probability (float): Base probability of a cell being a trap.
        target_min_blanks (int): Minimum desired number of blanks.
        target_max_blanks (int): Maximum desired number of blanks.
        max_attempts (int): Maximum number of generation attempts.

    Returns:
        list[list[str]] or None: The generated puzzle grid if successful within
                                 max_attempts, otherwise None.
    """
    if not (target_min_blanks <= target_max_blanks and target_min_blanks >= 0):
         print("Error: Invalid blank range specified.")
         return None

    # Initial guess for reveal probability
    # If target blanks are high, start with lower reveal prob, and vice versa
    total_cells = rows * cols
    target_avg_blanks = (target_min_blanks + target_max_blanks) / 2
    # Estimate non-blanks needed, relate that to reveal prob (very rough estimate)
    estimated_reveal_prob = 1.0 - (target_avg_blanks / total_cells)
    reveal_prob = max(0.0, min(1.0, estimated_reveal_prob)) # Clamp to [0, 1]
    reveal_step = 0.05 # How much to adjust probability each time

    print(f"Attempting generation for blank range [{target_min_blanks}-{target_max_blanks}]...")

    for attempt in range(max_attempts):
        print(f"  Attempt {attempt + 1}/{max_attempts} (Reveal Prob: {reveal_prob:.2f})...", end="")
        puzzle_grid, _, actual_blanks = generate_solvable_minesweeper_grid(
            rows, cols, trap_probability, reveal_prob
        )

        if puzzle_grid is None: # Error in sub-function
            print(" generation failed.")
            continue # Try again with same probability maybe? Or adjust slightly?

        print(f" Got {actual_blanks} blanks.")

        if target_min_blanks <= actual_blanks <= target_max_blanks:
            print(f"\nSuccess! Found grid with {actual_blanks} blanks within range.")
            return puzzle_grid
        elif actual_blanks < target_min_blanks:
            # Too few blanks -> Need to hide more -> Decrease reveal probability
            reveal_prob = max(0.0, reveal_prob - reveal_step)
        else: # actual_blanks > target_max_blanks
            # Too many blanks -> Need to reveal more -> Increase reveal probability
            reveal_prob = min(1.0, reveal_prob + reveal_step)

    print(f"\nFailed to generate grid within target blank range after {max_attempts} attempts.")
    return None


def write_grid_to_file(grid, filename="output.txt"):
    """Writes the grid to a file in the specified format."""
    if grid is None:
        print(f"Error: Cannot write None grid to {filename}.")
        return
    try:
        with open(filename, 'w') as f:
            for i, row in enumerate(grid):
                # Join elements with ', '
                f.write(', '.join(row))
                # Add newline except for the last row
                if i < len(grid) - 1:
                    f.write('\n')
        print(f"Successfully saved generated test case to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def get_grid_size_from_user():
    """Prompts the user for the grid size N and validates the input."""
    while True:
        try:
            n_str = input("Enter the size N for the NxN grid (e.g., 7): ")
            n_int = int(n_str)
            if n_int > 0:
                return n_int
            else:
                print("Error: Grid size must be a positive integer.")
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")
        except EOFError:
             print("\nInput stream closed. Exiting.")
             return None

def get_blank_range_from_user(max_possible_blanks):
    """Prompts user for the desired blank range (e.g., '10-19') and validates."""
    while True:
        try:
            range_str = input(f"Enter desired blank range (e.g., 10-19, max possible {max_possible_blanks}): ")
            match = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", range_str)
            if match:
                min_b = int(match.group(1))
                max_b = int(match.group(2))

                if min_b < 0 or max_b < 0:
                    print("Error: Blank counts cannot be negative.")
                elif min_b > max_b:
                    print("Error: Minimum blanks cannot be greater than maximum blanks.")
                elif max_b > max_possible_blanks:
                     print(f"Error: Maximum blanks ({max_b}) cannot exceed total cells ({max_possible_blanks}).")
                else:
                    # Suggest rounding up min if needed, or just use the range
                    # Example: if user enters 10-19, min_b=10, max_b=19
                    return min_b, max_b
            else:
                # Handle single number input maybe? e.g., "25" -> range 20-29?
                match_single = re.match(r"^\s*(\d+)\s*$", range_str)
                if match_single:
                    num = int(match_single.group(1))
                    if num < 0:
                         print("Error: Blank count cannot be negative.")
                    elif num > max_possible_blanks:
                         print(f"Error: Blank count ({num}) cannot exceed total cells ({max_possible_blanks}).")
                    else:
                        # Interpret single number 'X' as range [X - X%10, X - X%10 + 9]
                        # e.g., 25 -> min=20, max=29
                        # e.g., 8 -> min=0, max=9
                        # e.g., 30 -> min=30, max=39
                        min_b = math.floor(num / 10) * 10
                        max_b = min_b + 9
                        # Adjust max if it exceeds total cells
                        max_b = min(max_b, max_possible_blanks)
                        # Ensure min isn't greater than adjusted max (e.g., for N=3, input '8', max becomes 9)
                        min_b = min(min_b, max_b)

                        print(f"Interpreting '{num}' as target range: {min_b}-{max_b}")
                        return min_b, max_b
                else:
                    print("Error: Invalid format. Use 'min-max' (e.g., 10-19) or a single number (e.g., 25).")

        except ValueError:
            print("Error: Invalid number entered.")
        except EOFError:
            print("\nInput stream closed. Exiting.")
            return None, None


# --- Configuration ---
TRAP_PROBABILITY = 0.18 # Base trap probability (can influence difficulty)
OUTPUT_FILENAME = "output.txt"
MAX_GENERATION_ATTEMPTS = 30 # Number of tries to hit the blank target

# --- Generate and Save ---
if __name__ == "__main__":
    grid_size = get_grid_size_from_user()

    if grid_size is not None:
        max_blanks = grid_size * grid_size
        min_blanks_target, max_blanks_target = get_blank_range_from_user(max_blanks)

        if min_blanks_target is not None:
            print(f"\nGenerating a {grid_size}x{grid_size} grid...")
            # Call the function that handles the iterative generation
            generated_grid = generate_grid_with_target_blanks(
                rows=grid_size,
                cols=grid_size,
                trap_probability=TRAP_PROBABILITY,
                target_min_blanks=min_blanks_target,
                target_max_blanks=max_blanks_target,
                max_attempts=MAX_GENERATION_ATTEMPTS
            )

            if generated_grid:
                write_grid_to_file(generated_grid, OUTPUT_FILENAME)
                # Optional: Print the grid to console as well
                print("\nGenerated Grid:")
                final_blanks = sum(row.count('_') for row in generated_grid)
                print(f"(Actual Blanks: {final_blanks})")
                for row in generated_grid:
                    print(', '.join(row))
            else:
                print("Could not generate a grid meeting the criteria.")
        else:
            print("Could not obtain valid blank range. Exiting.")
    else:
        print("Could not obtain valid grid size. Exiting.")