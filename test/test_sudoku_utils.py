from src import sudoku_utils
import tempfile
import os


def create_test_file(contents):
    _, file_path = tempfile.mkstemp()
    with open(file_path, "w") as file:
        file.write(contents)
    return file_path


def test_get_matrix():
    input_content = """
000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000
"""
    expected_result = [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]

    file_path = create_test_file(input_content)

    try:
        result = sudoku_utils.get_matrix(file_path)
        assert result == expected_result
    except Exception as e:
        print(f"Error in test_get_matrix: {e}")
        assert False  # Mark the test as failed

    # Cleanup temporary files
    os.remove(file_path)


def test_is_correct():
    # Bad matrix with duplicate in the first row
    bad_matrix = [
        [1, 2, 3, 2, 5, 6, 7, 8, 9],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    try:
        assert sudoku_utils.is_correct(bad_matrix) == 0
    except AssertionError:
        print(
            "Error in test_is_correct: "
            "Expected bad matrix to be flagged as incorrect."
        )
        assert False  # Mark the test as failed

    # Good matrix
    good_matrix = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    try:
        assert sudoku_utils.is_correct(good_matrix) == 1
    except AssertionError:
        print(
            "Error in test_is_correct: "
            "Expected good matrix to be flagged as correct."
        )
        assert False  # Mark the test as failed


def test_matrix_to_format():
    expected_result = """000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000
"""
    input_matrix = [
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 5, 0, 4],
        [0, 0, 0, 0, 5, 0, 1, 6, 9],
        [0, 8, 0, 0, 0, 0, 3, 0, 5],
        [0, 7, 5, 0, 0, 0, 2, 9, 0],
        [4, 0, 6, 0, 0, 0, 0, 8, 0],
        [7, 6, 2, 0, 8, 0, 0, 0, 0],
        [1, 0, 3, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
    ]

    try:
        result = sudoku_utils.matrix_to_format(input_matrix)
        assert result == expected_result
    except Exception as e:
        print(f"Error in test_matrix_to_format: {e}")
        assert False  # Mark the test as failed
