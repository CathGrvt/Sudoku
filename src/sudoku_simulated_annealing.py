"""!@file sudoku_simulated_annealing.py
@brief Module containing tools for Sudoku solver.

@details This module contains bqm construction and simulated annealing sampler.

@author C. Grivot
"""


import dimod
from dimod.generators.constraints import combinations
from dwave.samplers import SimulatedAnnealingSampler
import sys
import concurrent.futures
import copy
import time
import functools
from functools import partial


# Decorator to measure the execution time of a function
def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        assert callable(func), "func is not callable"
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds.")
        return value

    return wrapper


# Decorator to log function calls
def logging_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(
            f"Calling {func.__name__} with arguments {args} "
            " and keyword arguments {kwargs}"
        )
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


def get_bqm(matrix):
    """!@brief get the bqm.

    @details
    This function gets the BinaryQuadraticModel of a matrix using contraints.

    @param matrix The matrix to get the bqm from.
    @return bqm the final BinaryQuadraticModel.
    """

    # Set up
    n = 9  # Number of rows/columns in sudoku
    m = 3  # Number of rows in a box
    digits = range(1, 10)

    bqm = dimod.BinaryQuadraticModel(dimod.BINARY)
    # need to check if dimod.SPIN is better and how it differs

    # Constraint: Each cell can only select one digit
    for row in range(n):
        for col in range(n):
            cell_digits = [f"{row},{col}_{digit}" for digit in digits]
            one_digit_bqm = combinations(cell_digits, 1)
            bqm.update(one_digit_bqm)

    # Constraint: Each row of cells cannot have duplicate digits
    for row in range(n):
        for digit in digits:
            row_cells = [f"{row},{col}_{digit}" for col in range(n)]
            row_bqm = combinations(row_cells, 1)
            bqm.update(row_bqm)

    # Constraint: Each column of cells cannot have duplicate digits
    for col in range(n):
        for digit in digits:
            col_cells = [f"{row},{col}_{digit}" for row in range(n)]
            col_bqm = combinations(col_cells, 1)
            bqm.update(col_bqm)

    # Constraint: Each box cannot have duplicates
    # Build indices of a basic box
    box_indices = [(row, col) for row in range(m) for col in range(m)]

    # Build full sudoku array
    for row_scalar in range(m):
        for col_scalar in range(m):
            for digit in digits:
                # Shifts for moving box inside sudoku matrix
                row_shift = row_scalar * m
                col_shift = col_scalar * m

                # Build the labels for a box
                box = [
                    f"{row + row_shift},{col + col_shift}_{digit}"
                    for row, col in box_indices
                ]
                box_bqm = combinations(box, 1)
                bqm.update(box_bqm)

    # Constraint: Fix known values
    for row, line in enumerate(matrix):
        for col, value in enumerate(line):
            if value > 0:
                # Each cell can only select one digit.
                # Hence, for a given cell at row r and column c,
                # we have 9 labels. Namely,
                # ["r,c_1", "r,c_2", ..., "r,c_8", "r,c_9"]
                #
                # Due to this same constraint, we can only select one of these
                # 9 labels (achieved by 'generators.combinations(..)').
                #
                # The 1 below indicates that we are selecting the label
                # produced by f"{row},{col}_{value}", fixing known values.
                # All other labels
                # with the same 'row' and 'col' will be discouraged from being
                # selected.
                bqm.fix_variable(f"{row},{col}_{value}", 1)

    return bqm


def solve_simulated_annealing(bqm, matrix):
    """!@brief solves sudoku using simulated annealing.

    @details This function uses one of dwave samplers, SImulated annealing,
    to solve a sudoku and returns it as a matrix.

    @param bqm The bqm with instaured constraints.
    @param matrix the initial sudoku.
    @return result The final sudoku.
    """

    try:
        sampler = SimulatedAnnealingSampler()
        solution = sampler.sample(bqm, num_reads=10000)
        # 100 reads/samples, increase this to have a better result
        # 10000 is a good value

    except Exception as e:
        print(f"Error during simulated annealing: {e}")
        sys.exit(1)

    best_solution = solution.first.sample
    solution_list = [key for key, value in best_solution.items() if value == 1]
    # A value of 1 indicates
    # that the variable is selected or "on" in the solution

    result = copy.deepcopy(matrix)

    for label in solution_list:
        coord, digit = label.split("_")
        # Remember that we have ["r,c_1", "r,c_2", ..., "r,c_8", "r,c_9"]
        row, col = map(int, coord.split(","))

        if result[row][col] > 0:
            # Avoid overwriting cells in the Sudoku puzzle
            # that were initially filled with values

            continue

        result[row][col] = int(digit)

    return result


@timing_decorator
def solve_parallel(bqm, matrix, start_points=5):
    """!@brief solves sudoku using parallel simulated annealing.

    @details This function uses parallelisation
    to solve a sudoku and returns it as a matrix.

    @param bqm The bqm with instaured constraints.
    @param matrix the initial sudoku.
    @param start_points The number of initial states to use.
    @return result The final sudoku.
    """
    # Use functools.partial to create a function with fixed arguments
    partial_solve = partial(solve_simulated_annealing, bqm, matrix)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit tasks with different initial states
        futures = [executor.submit(partial_solve) for _ in range(start_points)]

    # Get results from parallel runs
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # Return the best result
    best_result = min(results, key=lambda x: x[1])
    return best_result
