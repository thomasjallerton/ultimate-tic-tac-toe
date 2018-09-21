from utilities import is_game_won
from pieces import *


class SmallBoard:
    def __init__(self, outer_row, outer_col):
        self.board = [[NO_PIECE for i in range(3)] for j in range(3)]
        self.outer_row = outer_row
        self.outer_col = outer_col

    def is_game_tied(self):
        if is_game_won(self.board):
            return True

        for iter_row in range(3):
            for iter_column in range(3):
                if self.board[iter_row][iter_column] == NO_PIECE:
                    return False
        return True

    def get_available_moves(self):
        available_moves = []

        for iter_row in range(3):
            for iter_column in range(3):
                if self.board[iter_row][iter_column] == NO_PIECE:
                    available_moves.append([self.outer_row, self.outer_col, iter_row, iter_column])
        return available_moves

    def set_piece(self, inner_row, inner_col, piece):
        self.board[inner_row][inner_col] = piece

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_piece_count(self, piece):
        count = 0
        for iter_row in range(3):
            for iter_column in range(3):
                if self.board[iter_row][iter_column] == piece:
                    count += 1
        return count

    def is_adjacent_in_line(self, row, col):
        piece = self.board[row][col]
        if (row == 1 and col == 1) or (row % 2 == 0 and col % 2 == 0):  # if corner or centre
            for iter_row in range(max(row - 1, 0), min(row + 2, 3)):
                for iter_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if (iter_row != row or iter_col != col) and self.board[iter_row][iter_col] == piece:
                        return True
            if row % 2 == 0 and col % 2 == 0:  # if corner
                for iter_row in range(0, 2, 2):
                    for iter_col in range(0, 3, 2):
                        if (iter_row != row or iter_col != col) and self.board[iter_row][iter_col] == piece:
                            return True

        else:  # if middle side
            for iter_row in range(max(row - 1, 0), min(row + 2, 3)):
                for iter_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if ((iter_row == row) ^ (iter_col == col)) and self.board[iter_row][iter_col] == piece:
                        return True
            # Get opposite side
            if row == 1:
                new_col = (col + 2) % 4
                if self.board[row][new_col] == piece:
                    return True
            if col == 1:
                new_row = (row + 2) % 4
                if self.board[new_row][col] == piece:
                    return True
        return False
