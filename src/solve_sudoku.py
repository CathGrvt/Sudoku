"""!@mainpage
@section intro_sec Introduction
This project implements a Sudoku solver using simulated annealing.

@author C. Grivot

@file solve_sudoku.py
@brief Main script for cg845/src.
@details
This script imports tools from sudoku_simulated_annealing.py and sudoku_utils
and uses it to solve sudokus.
@package sudoku_simulated_annealing
@package sudoku_utils
"""

import cProfile
import sudoku_utils
import sudoku_simulated_annealing as ssa
import sys


def main():
    # Read sudoku file as matrix
    matrix = sudoku_utils.get_matrix(filename)

    # Get the BQM
    bqm = ssa.get_bqm(matrix)

    # Solve the suddoku, need to add time it wrapper
    result = ssa.solve_parallel(bqm, matrix)

    # Print solution in the right format
    print(sudoku_utils.matrix_to_format(result))

    # Verify that the solution is correct
    sudoku_utils.is_correct(result)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(
            "Error: Too many command line arguments. Usage: python "
            "{} <sudoku filepath>".format(sys.argv[0])
        )
        sys.exit(1)
    if "run_as_profile" in sys.argv:
        filename = "Data/input.txt"
        print(
            "Warning: using default input file, '{}'. Second Warning: "
            "Profiling right now".format(filename)
        )
        # Run with profiling
        cProfile.run("main()", sort="cumulative")
        exit()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        main()
    else:
        filename = "Data/input.txt"
        print(
            "Warning: using default input file, '{}'. Usage: python "
            "{} <sudoku filepath>".format(filename, sys.argv[0])
        )
        main()
