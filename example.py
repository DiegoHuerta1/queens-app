import matplotlib.pyplot as plt

from solver.QueenSolver import QueenSolver
from solver.Boards import BoardMode


# Define Problem
solver = QueenSolver(n = 5, m = 5, num_queens = 5, mode = BoardMode.Torus)

# Solver
solver.solve_problem()
sol_matrices = solver.get_matrix_solutions()
print(f"Number of solutions: {len(sol_matrices)}")

# See some solutions
for i in range(min(5, len(sol_matrices))):
    # Matrix form
    print(sol_matrices[i])
    # Plot
    fig = solver.plot_solution(solver.solutions[i])
    plt.show()





