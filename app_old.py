import streamlit as st

from solver.QueenSolver import QueenSolver
from solver.Boards import BoardMode

# streamlit run app.py


st.title("N-Queens Solver")


# parameters
n = st.sidebar.number_input("Rows", 1, 20, 8)
m = st.sidebar.number_input("Columns", 1, 20, 8)

num_queens = st.sidebar.number_input(
    "Number of queens",
    1,
    max(n, m),
    min(n, m)
)

mode_name = st.sidebar.selectbox(
    "Board type",
    [mode.name for mode in BoardMode]
)
mode = BoardMode[mode_name]

num_show = st.sidebar.number_input(
    "Number of solutions to display",
    1,
    20,
    5
)

# Buton to solve problem
run_solver = st.sidebar.button("Solve")
if run_solver:

    # Use solver and save solutions
    solver = QueenSolver(
        n=n,
        m=m,
        num_queens=num_queens,
        mode=mode
    )
    solver.solve_problem()
    solutions = solver.solutions

    # Total count
    st.write(f"Total solutions: {len(solver.solutions)}")

    # Individual plots
    for k, sol in enumerate(solutions[:num_show]):
        st.subheader(f"Solution {k+1}")
        fig = solver.plot_solution(sol)
        st.pyplot(fig, width='content')