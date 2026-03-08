from enum import Enum
import numpy as np


Square = tuple[int, int]

class Classic_Board():
    """  
    Class that represent the chess board N x M (index 0)
    """

    def __init__(self, n: int = 8, m: int = 8) -> None:
        """  
        Create a board
        """
        self.n: int = n
        self.m: int = m
        self._matrix = np.zeros((n, m))

        # First and outside square
        self.first_square: Square = (0, 0)
        self.outside_square: Square = (n, 0)

        # Blocked squares for each of the queens
        self.blocked_squares: list[set[Square]] = []

    def get_next_square(self, square: Square) -> Square:
        """  Iterate the board """
        a, b = square
        # The row is complete
        if b == (self.m-1):
            return (a+1, 0)
        else:
            return (a, b+1)
        
    def add_queen(self, square: Square):
        """  Add new blocked squares for this queen """
        self.blocked_squares.append(self.get_blocked_squares_queen(square))

    def remove_last_queen(self):
        """  Remove the blokced squares of the latest queen """
        self.blocked_squares.pop(-1)

    def is_free_square(self, square: Square) -> bool:
        """ Check if the square is blocked """
        for blocked_set in self.blocked_squares:
            if square in blocked_set:
                return False
        return True
    
    def get_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """  Compute the squares blocked by a queen """
        squares: list[Square] = []
        a, b = queen
        # Block the rest of the row
        for i in range(b+1, self.m):
            squares.append( (a, i) )
        # Block the rest of the column
        for j in range(a+1, self.n):
            squares.append( (j, b) )
        # Block the rest of the rigth diagonal
        i, j = a+1, b+1
        while (i < self.n) and (j < self.m):
            squares.append( (i,j) )
            i += 1
            j += 1
        # Block the rest of the left diagonal
        i, j = a+1, b-1
        while (i < self.n) and (j >= 0):
            squares.append( (i,j) )
            i += 1
            j -= 1
        return set(squares)


class Torus_Board(Classic_Board):
    def move_diagonal_right(self, square: Square) -> Square:
        " Move into the right diagonal "
        return ( (square[0] + 1) % self.n, (square[1] + 1) % self.m )
    
    def move_diagonal_left(self, square: Square) -> Square:
        " Move into the left diagonal "
        return ( (square[0] + 1) % self.n, (square[1] - 1) % self.m )

    def get_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """  Compute the squares blocked by a queen in a torus """
        squares: list[Square] = []
        a, b = queen
        # Block the rest of the row
        for i in range(b+1, self.m):
            squares.append( (a, i) )
        # Block the rest of the column
        for j in range(a+1, self.n):
            squares.append( (j, b) )
        # Block the rigth diagonal
        square_diag = self.move_diagonal_right(queen)
        while square_diag != queen:
            squares.append( square_diag )
            square_diag = self.move_diagonal_right(square_diag)
        # Block the left diagonal
        square_diag = self.move_diagonal_left(queen)
        while square_diag != queen:
            squares.append( square_diag )
            square_diag = self.move_diagonal_left(square_diag)
        return set(squares)
    

class Klein1_Board(Classic_Board):
    """ Only twist the horizontal fold"""

    def move_diagonal_right(self, square: Square) -> Square:
        " Move into the right diagonal "
        return ( (square[0] + 1) % self.n, (square[1] + 1) % self.m )
    
    def move_diagonal_left(self, square: Square) -> Square:
        " Move into the left diagonal "
        return ( (square[0] + 1) % self.n, (square[1] - 1) % self.m )

    def get_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """  Compute the squares blocked by a queen in a torus """
        squares: list[Square] = []
        a, b = queen
        # Block the rest of the row
        for i in range(b+1, self.m):
            squares.append( (a, i) )
        # Block the rest of the column
        for j in range(a+1, self.n):
            squares.append( (j, b) )
        # Block the rigth diagonal
        square_diag = self.move_diagonal_right(queen)
        while square_diag != queen:
            squares.append( square_diag )
            square_diag = self.move_diagonal_right(square_diag)
        # Block the left diagonal
        square_diag = self.move_diagonal_left(queen)
        while square_diag != queen:
            squares.append( square_diag )
            square_diag = self.move_diagonal_left(square_diag)
        return set(squares)
    

class Klein2_Board(Classic_Board):
    def get_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """  Compute the squares blocked by a queen """
        ...


class BoardMode(Enum):
    """  
    Different options of chess boards
    """
    Classic = Classic_Board
    Torus = Torus_Board
    Klein1 = Klein1_Board
    Klein2 = Klein2_Board