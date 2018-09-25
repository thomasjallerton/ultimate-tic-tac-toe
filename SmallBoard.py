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

    def hash(self):
        board = self.board
        return str(board[0][0]) + str(board[0][1]) + str(board[0][2]) + str(board[1][0]) + str(board[1][1]) + \
            str(board[1][2]) + str(board[2][0]) + str(board[2][1]) + str(board[2][2])
