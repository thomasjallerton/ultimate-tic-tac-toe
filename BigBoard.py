from SmallBoard import SmallBoard
from utilities import *
from pieces import *


class BigBoard:
    def __init__(self):
        self.board = [[SmallBoard(row_iter, col_iter) for col_iter in range(3)] for row_iter in range(3)]

    def is_game_won(self):
        if is_game_won(self.board):
            return True
        else:
            return False

    def is_game_tied(self):
        for iter_row in range(3):
            for iter_column in range(3):
                if isinstance(self.board[iter_row][iter_column], SmallBoard):
                    return False
        return True

    def set_board_piece_if_won(self, played_row, played_column, players_turn):
        if is_game_won(self.board[played_row][played_column].board):
            self.board[played_row][played_column] = players_turn
        elif self.board[played_row][played_column].is_game_tied():
            self.board[played_row][played_column] = NO_PIECE

    def get_available_moves(self):
        available_moves = []
        for iter_row in range(3):
            for iter_column in range(3):
                if isinstance(self.board[iter_row][iter_column], SmallBoard):
                    available_moves += self.board[iter_row][iter_column].get_available_moves()
        return available_moves

    def get_next_possible_moves(self, selected_row, selected_column):
        if isinstance(self.board[selected_row][selected_column], SmallBoard):
            return self.board[selected_row][selected_column].get_available_moves()
        else:
            return self.get_available_moves()

    def set_sub_piece(self, outer_row, outer_col, inner_row, inner_col, piece):
        self.board[outer_row][outer_col].set_piece(inner_row, inner_col, piece)
        self.set_board_piece_if_won(outer_row, outer_col, piece)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_number_won_sub_boards(self):
        count = 0
        for iter_row in range(3):
            for iter_column in range(3):
                if not isinstance(self.board[iter_row][iter_column], SmallBoard):
                    count += 1
        return count

    def get_sub_board(self, row, column):
        return self.board[row][column]

    def get_won_squares(self):
        won_squares = []
        for iter_row in range(3):
            for iter_col in range(3):
                if not isinstance(self.board[iter_row][iter_col], SmallBoard):
                    won_squares.append([iter_row, iter_col])
        return won_squares
