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

mode = st.sidebar.selectbox(
    "Board type",
    list(BoardMode)
)

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
    st.session_state["solver"] = solver
    st.session_state["solutions"] = solver.solutions
    st.session_state["count"] = len(solver.solutions)


# show results after running
if "solver" in st.session_state:
    solver = st.session_state["solver"]
    solutions = st.session_state["solutions"]

    # Total count
    st.write(f"Total solutions: {st.session_state['count']}")

    # Individual plots
    for k, sol in enumerate(solutions[:num_show]):
        st.subheader(f"Solution {k+1}")
        fig = solver.plot_solution(sol)
        st.pyplot(fig, width='content')