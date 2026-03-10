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
    
    def get_all_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """ Consider all squares for visualizations """
        squares: list[Square] = []
        a, b = queen
        #  row
        for i in range(self.m):
            if i != b:
                squares.append( (a, i) )
        # column
        for j in range(self.n):
            if j != a:
                squares.append( (j, b) )
        # rigth diagonal
        i, j = a+1, b+1
        while (i < self.n) and (j < self.m):
            squares.append( (i,j) )
            i += 1
            j += 1
        # lower right
        i, j = a-1, b+1
        while (i >= 0) and (j < self.m):
            squares.append( (i,j) )
            i -= 1
            j += 1
        # left diagonal
        i, j = a+1, b-1
        while (i < self.n) and (j >= 0):
            squares.append( (i,j) )
            i += 1
            j -= 1
        # lower left
        i, j = a-1, b-1
        while (i >= 0) and (j >= 0):
            squares.append( (i,j) )
            i -= 1
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
    
    def get_all_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """ Consider all squares for visualizations """
        squares: list[Square] = []
        a, b = queen
       #  row
        for i in range(self.m):
            if i != b:
                squares.append( (a, i) )
        # column
        for j in range(self.n):
            if j != a:
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
    

def reflect(n: int, x: int) -> int:
    """   
    Given n elements, reflect the element x in {0, ..., n-1}
    """
    return n - x - 1


class Mobius_Board(Classic_Board):
    """ Horizontal twist, no vertical fold"""

    def move_right(self, square: Square) -> tuple[Square, bool]:
        a, b = square
        # Edge case
        if b == (self.m - 1):
            return (reflect(self.n, a), 0), True
        # Just move right
        else:
            return (a, b+1), False

    def move_left(self, square: Square) -> tuple[Square, bool]:
        a, b = square
        # Edge case
        if b == 0:
            return (reflect(self.n, a), self.m - 1), True
        # Just move left
        else:
            return (a, b-1), False
        
    def move_up(self, square: Square) -> Square:
        a, b = square
        # just move up, no fold or twist
        return (a+1, b)
    
    def move_down(self, square: Square) -> Square:
        a, b = square
        return (a-1, b)

    def move_diagonal_right(self, square, move_up: bool) -> tuple[Square, bool]:
        new_square, flipped = self.move_right(square)
        # check new vertical orientation
        move_up_new = not move_up if flipped else move_up
        # move vertically (depending on twists)
        if move_up_new:
            new_square = self.move_up(new_square)
        else:
            new_square = self.move_down(new_square)
        return new_square, move_up_new
        
    def move_diagonal_left(self, square, move_up: bool) -> tuple[Square, bool]:
        new_square, flipped = self.move_left(square)
        # check new vertical orientation
        move_up_new = not move_up if flipped else move_up
        # move vertically (depending on twists)
        if move_up_new:
            new_square = self.move_up(new_square)
        else:
            new_square = self.move_down(new_square)
        return new_square, move_up_new  


    def get_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """  Compute the squares blocked by a queen in a torus """
        squares: list[Square] = []
        a, b = queen
        #  row
        for i in range(self.m):
            if i != b:
                squares.append( (a, i) )
        # column
        for j in range(self.n):
            if j != a:
                squares.append( (j, b) )

        # Block the reflected row
        a_star = reflect(self.n, a)
        for i in range(self.m):
            squares.append( (a_star, i))

        # Block the upper rigth diagonal
        move_up = True
        square, move_up = self.move_diagonal_right(queen, move_up)
        while (0 <= square[0] < self.n) and (square != queen):
            squares.append( square )
            square, move_up = self.move_diagonal_right(square, move_up)
        # Block the upper left diagonal
        move_up = True
        square, move_up = self.move_diagonal_left(queen, move_up)
        while (0 <= square[0] < self.n) and (square != queen):
            squares.append( square )
            square, move_up = self.move_diagonal_left(square, move_up)

        # Block the lower rigth diagonal
        move_up = False
        square, move_up = self.move_diagonal_right(queen, move_up)
        while (0 <= square[0] < self.n) and (square != queen):
            squares.append( square )
            square, move_up = self.move_diagonal_right(square, move_up)
        # Block the lower left diagonal
        move_up = False
        square, move_up = self.move_diagonal_left(queen, move_up)
        while (0 <= square[0] < self.n) and (square != queen):
            squares.append( square )
            square, move_up = self.move_diagonal_left(square, move_up)
        return set(squares)
    

    def get_all_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """ Consider all squares for visualizations """
        return self.get_blocked_squares_queen(queen)


class Klein1_Board(Mobius_Board):
    """ Only twist the horizontal fold"""

    # update up and down (now we have a fold)
    def move_up(self, square: Square) -> Square:
        a, b = square
        return ((a+1) % self.n, b)
    def move_down(self, square: Square) -> Square:
        a, b = square
        return ((a-1) % self.n, b)

    def get_blocked_squares_queen(self, queen: Square) -> set[Square]:
        """  Compute the squares blocked by a queen in a torus """
        squares: list[Square] = []
        a, b = queen
        #  row
        for i in range(self.m):
            if i != b:
                squares.append( (a, i) )
        # column
        for j in range(self.n):
            if j != a:
                squares.append( (j, b) )

        # Block the reflected row
        a_star = reflect(self.n, a)
        for i in range(self.m):
            squares.append( (a_star, i))

        # Block the upper rigth diagonal
        move_up = True
        square, move_up = self.move_diagonal_right(queen, move_up)
        while square != queen:
            squares.append( square )
            square, move_up = self.move_diagonal_right(square, move_up)
        # Block the upper left diagonal
        move_up = True
        square, move_up = self.move_diagonal_left(queen, move_up)
        while square != queen:
            squares.append( square )
            square, move_up = self.move_diagonal_left(square, move_up)

        # Block the lower rigth diagonal
        move_up = False
        square, move_up = self.move_diagonal_right(queen, move_up)
        while square != queen:
            squares.append( square )
            square, move_up = self.move_diagonal_right(square, move_up)
        # Block the lower left diagonal
        move_up = False
        square, move_up = self.move_diagonal_left(queen, move_up)
        while square != queen:
            squares.append( square )
            square, move_up = self.move_diagonal_left(square, move_up)
        return set(squares)



class BoardMode(Enum):
    """  
    Different options of chess boards
    """
    Classic = Classic_Board
    Torus = Torus_Board
    Mobius = Mobius_Board
    Klein1 = Klein1_Board