import numpy as np
import json
import matplotlib.pyplot as plt

from solver.Boards import Square, BoardMode


# Configuration for logging
import logging
with open("config.json") as f:
    config = json.load(f)
level_name = config.get("log_level", "WARNING").upper()
level = getattr(logging, level_name, logging.WARNING)
logging.basicConfig(filename="queens_log.log", level=level)



class QueenSolver():
    """  
    Solver of the chess queens problem
    """

    def __init__(self, n: int = 8, m: int = 8, num_queens: int = 8,
                 mode: BoardMode = BoardMode.Classic) -> None:
        """  
        Keep track of two chains, for solutions, and options (put queen or not)
        """
        self.n = n
        self.m = m
        self.num_queens = num_queens

        # Create the initial board (empty)
        self.board = mode.value(n = n, m = m)
        self.outside_square: Square = self.board.outside_square

        # Store all found solutions
        self.solutions: list[list[Square]] = []


    def solve_problem(self):
        """   
        Solve the problem using backtracking
        """
        # Keep track of the queens
        queen_coord: list[Square] = []
        # start in the first square
        square = self.board.first_square
        logging.debug("Starting the solver!")

        # stop when we are outside the board with 0 queens
        while (square != self.outside_square) or len(queen_coord) > 0:
            logging.debug(f"Square: {square}")
            
            # Check if we completed the board (or the problem)
            if (square == self.outside_square) or (len(queen_coord)==self.num_queens):
                logging.debug(f"Board is complete")

                # If we have a solution
                if len(queen_coord) == self.num_queens:
                    self.solutions.append(queen_coord.copy())
                    logging.debug(f"We have a solution!!")
                    logging.debug(f"\t{queen_coord}")

                # Go back to last queen and remove it
                if len(queen_coord) > 0:
                    square = queen_coord.pop(-1)
                    self.board.remove_last_queen()
                    logging.debug(f"Remove queen at {square}")
                    # Move
                    square = self.board.get_next_square(square)
                    continue

            # If possible, place a queen
            if self.board.is_free_square(square):
                self.board.add_queen(square)
                queen_coord.append(square)
                logging.debug(f"Placing queen")

            # Move
            square = self.board.get_next_square(square)
        

    def get_matrix_solutions(self) -> list[np.ndarray]:
        """  Get solutions in nice format after solver """
        matrix_sol: list[np.ndarray] = []
        # For each solution
        for sol in self.solutions:
            matrix = np.zeros((self.n, self.m))
            # Place each queen
            for queen in sol:
                matrix[queen] = 1
            matrix_sol.append(matrix)
        return matrix_sol
    
    def plot_solution(self, solution: list[Square]):
        """
        Return a matplotlib figure with the chessboard visualization
        """
        fig, ax = plt.subplots(figsize=(3, 3))

        # draw board
        for i in range(self.n):
            for j in range(self.m):
                color = "#EEEED2" if (i + j) % 2 == 0 else "#769656"
                square = plt.Rectangle( # type: ignore
                    (j, self.n - i - 1),
                    1,
                    1,
                    facecolor=color
                )
                ax.add_patch(square)

        # draw queens
        for (i, j) in solution:
            ax.text(
                j + 0.5,
                self.n - i - 0.5,
                "♛",
                ha="center",
                va="center",
                fontsize=18
            )

        # final parameters
        ax.set_xlim(0, self.m)
        ax.set_ylim(0, self.n)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        return fig
            
                
            
        





    






