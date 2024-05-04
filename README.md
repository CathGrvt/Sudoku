# Sudoku Solver

This project implements a Sudoku solver using simulated annealing.

## Project Structure

The project follows the following folder structure:

- **src/:** Contains the main scripts for solving Sudoku using simulated annealing.
  - `solve_sudoku.py`: Main script for solving Sudoku puzzles.
  - `sudoku_simulated_annealing.py`: Simulated annealing implementation.
  - `sudoku_utils.py`: Utility functions for Sudoku operations.

- **test/:** Includes unit tests for the Sudoku solver.
  - `test_sudoku_solver.py`: Unit tests for the Sudoku solver.
  - `test_simulated_annealing.py`: Unit tests for simulated annealing and bqm.


- **docs/:** Documentation related files.
  - `Doxyfile`: Doxygen configuration file.
  - `report/:` Directory for project reports.
    - `report.tex`: LaTeX source file for the project report.
    - `report.pdf`: Generated PDF of the report.

- **.gitignore:** Git ignore file.

- **.pre_commit_config:** Configuration for pre-commit hooks.

- **Dockerfile:** Dockerfile for containerization.

- **environment.yml:** Conda environment file.

- **README.md:** Project README file.

## Getting Started

To get started with the Sudoku solver, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://gitlab.developers.cam.ac.uk/phy/data-intensive-science-mphil/c1_assessment/cg845.git
   ```

2. Install project dependencies:

   ```bash
   conda env create -f environment.yml
   conda activate sudoku_solver
   ```

3. Run the Sudoku solver:

   ```bash
   python src/solve_sudoku.py input.txt
   ```

## Using the Docker Container
   ```bash
   git clone https://gitlab.developers.cam.ac.uk/phy/data-intensive-science-mphil/c1_assessment/cg845.git
   docker build -t conda .
   docker run --rm -ti conda
   python src/solve_sudoku.py input.txt
   ```
## Unit Tests

Ensure the correctness of the Sudoku solver by running the unit tests:

```bash
pytest
```
## Performance Metrics

To provide insight into the performance of the code, the following details were recorded:

- **Machine Specifications:**
  - Windows Subsystem for Linux (WSL) on windows of a standard laptop

- **Execution Time:**
  - The code took approximately 3 minutes to run.

## Documentation

For detailed documentation, refer to the [project report](docs/report/report.pdf).

To build your own local copy of the documentation you can run:
```bash
doxygen
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Times I Have Used ChatGPT:

1. **Prompt 2: How can I consider optimizing or parallelizing a simulated_annealing function?**
   - **Answer:**
    ```python
    import concurrent.futures

    def solve_simulated_annealing_parallel(problem, num_start_points=5):
      with concurrent.futures.ProcessPoolExecutor() as executor:
          futures = [executor.submit(solve_simulated_annealing, problem) for _ in range(num_start_points)]

      # Get results from parallel runs
      results = [future.result() for future in concurrent.futures.as_completed(futures)]

      # Return the best result
      best_result = min(results, key=lambda x: x[1])
      return best_result

    # Usage
    best_solution, best_cost = solve_simulated_annealing_parallel(your_problem_instance)
    print(f"Best Solution: {best_solution}, Best Cost: {best_cost}")
    ```

   **Modification I have made:**
   ```python
   def solve_simulated_annealing_parallel(bqm, matrix, num_start_points=5):
       with concurrent.futures.ProcessPoolExecutor() as executor:
           futures = [
               executor.submit(solve_simulated_annealing(bqm, matrix))
               for _ in range(num_start_points)
           ]

       # Get results from parallel runs
       results = [f.result() for f in concurrent.futures.as_completed(futures)]

       # Return the best result
       best_result = min(results, key=lambda x: x[1])
       return best_result
   ```

2. **Prompt 1: Give me a full sudoku in the matrix format that is correct.**
   - **Answer:**
     ```plaintext
     [
         [5, 3, 4, 6, 7, 8, 9, 1, 2],
         [6, 7, 2, 1, 9, 5, 3, 4, 8],
         [1, 9, 8, 3, 4, 2, 5, 6, 7],
         [8, 5, 9, 7, 6, 1, 4, 2, 3],
         [4, 2, 6, 8, 5, 3, 7, 9, 1],
         [7, 1, 3, 9, 2, 4, 8, 5, 6],
         [9, 6, 1, 5, 3, 7, 2, 8, 4],
         [2, 8, 7, 4, 1, 9, 6, 3, 5],
         [3, 4, 5, 2, 8, 6, 1, 7, 9]
     ]
     ```

   **Usage:**
   In `def test_is_correct():` as a good matrix input.
