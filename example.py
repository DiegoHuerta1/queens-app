from solver.QueenSolver import QueenSolver
from solver.Boards import BoardMode


# Define Problem
solver = QueenSolver(n = 5, m = 5, num_queens = 5, mode = BoardMode.Torus)

# Solver
solver.solve_problem()
print(f"Number of solutions: {len(solver.solutions)}")

# See some matrices of solutions
for sol in solver.get_matrix_solutions()[:1]:
    print(sol)


# See some visualizations of solutions
for sol in solver.solutions[:1]:
    fig = solver.plot_solution(sol)
    fig.show()




