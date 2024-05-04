from src import sudoku_simulated_annealing
import dimod


def test_get_bqm():
    # Test Sudoku puzzle
    matrix = [
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
    # Build the BQM
    try:
        bqm = sudoku_simulated_annealing.get_bqm(matrix)
        # Ensure that the BQM is an instance of dimod.BinaryQuadraticModel
        assert isinstance(bqm, dimod.BinaryQuadraticModel)
        # Check if the number of variables in the BQM is correct
        assert len(bqm.variables) == 703
        # 81 cells * 9 digits - 26 fixed values
    except Exception as e:
        print(f"Error in test_get_bqm: {e}")
        assert False  # Mark the test as failed
