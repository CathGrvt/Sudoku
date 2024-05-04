"""!@file sudoku_utils.py
@brief Module containing tools for fractions.

@details This module contains tools to solve the sudoku.

@author C. Grivot
"""


def get_matrix(file_path):
    """!@brief get the matrix from the sudoku.

    @details
    This function transforms the sudoku into a matrix from its initial format.

    @param file_path The path to the sudoku file.
    @return matrix The sudoku matrix.
    """
    try:
        with open(file_path, "r") as file:
            input_sudoku = file.read()
    except FileNotFoundError:
        print(f"Warning: File '{file_path}' not found. Using default input.")
        with open("Data/input.txt", "r") as file:
            input_sudoku = file.read()

    # Remove any spaces or vertical bars and split the input string into rows
    rows = input_sudoku.replace("|", "").replace("---+---+---", "").split("\n")

    # Filter out empty rows using list comprehension
    rows = [row for row in rows if any(row)]

    # Split each row into individual digits and convert them to integers
    matrix = [[int(num) for num in filter(str.isdigit, row)] for row in rows]

    if len(matrix) != 9 or any(len(row) != 9 for row in matrix):
        raise ValueError("Invalid Sudoku matrix. Check the input file.")

    return matrix


def is_correct(matrix):
    """!@brief Check if Sudoku matrix is correct

    @details This function verifies if the solution matrix is correct,
    that the sudoku is correctly solved.

    @param matrix The matrix to verify.
    @return True if the matrix is correct, False otherwise.
    """
    n = 9  # Number of rows/columns
    m = 3  # Number of boxes rows/columns
    digits = set(range(1, 10))

    # Verifying rows
    if any(set(row) != digits for row in matrix):
        print("Error in a row")
        return False

    # Verifying columns
    if any(set(matrix[i][j] for i in range(n)) != digits for j in range(n)):
        print("Error in a column")
        return False

    # Verifying boxes
    boxes = [
        [
            matrix[i + r_scalar * m][j + c_scalar * m]
            for i, j in [(i, j) for i in range(m) for j in range(m)]
        ]
        for r_scalar in range(m)
        for c_scalar in range(m)
    ]
    if any(set(box) != digits for box in boxes):
        print("Error in a box")
        return False
    print("Solution is correct!")
    return True


def matrix_to_format(matrix):
    """!@brief get the right format from the matrix.

    @details
    This function transforms the sudoku matrix into its initial format.

    @param matrix The sudoku matrix
    @return result The sudoku in the right format.
    """
    result = ""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            result += "---+---+---\n"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                result += "|"
            result += str(matrix[i][j])
        result += "\n"
    return result
