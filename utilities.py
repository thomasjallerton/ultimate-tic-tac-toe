from pieces import *


def is_game_won_winner(board):
    # Check if won
    top_left_piece = board[0][0]
    if top_left_piece != NO_PIECE:
        if (top_left_piece == board[1][0]) & (
                top_left_piece == board[2][0]):
            return top_left_piece
        if (top_left_piece == board[0][1]) & (
                top_left_piece == board[0][2]):
            return top_left_piece

    middle_piece = board[1][1]
    if middle_piece != NO_PIECE:
        if (middle_piece == board[0][1]) & (
                middle_piece == board[2][1]):
            return middle_piece
        if (middle_piece == board[1][0]) & (
                middle_piece == board[1][2]):
            return middle_piece
        if (middle_piece == board[0][0]) & (
                middle_piece == board[2][2]):
            return middle_piece
        if (middle_piece == board[2][0]) & (
                middle_piece == board[0][2]):
            return middle_piece

    bottom_right_piece = board[2][2]
    if bottom_right_piece != NO_PIECE:
        if (bottom_right_piece == board[2][0]) & (
                bottom_right_piece == board[2][1]):
            return bottom_right_piece
        if (bottom_right_piece == board[0][2]) & (
                bottom_right_piece == board[1][2]):
            return bottom_right_piece

    return NO_PIECE


def is_game_won(board):
    return is_game_won_winner(board) != NO_PIECE


def get_danger_squares(board, piece):
    opponent = swap_turn(piece)
    squares = []

    # find danger in rows
    for iter_row in range(3):
        for iter_col in range(3):
            if board[iter_row][iter_col % 3] == opponent \
                    and board[iter_row][(iter_col + 1) % 3] == opponent \
                    and board[iter_row][(iter_col + 2) % 3] != piece:
                squares.append([iter_row, (iter_col + 2) % 3])

    # find danger in columns
    for iter_col in range(3):
        for iter_row in range(3):
            if board[iter_row % 3][iter_col] == opponent \
                    and board[(iter_row + 1) % 3][iter_col] == opponent \
                    and board[(iter_row + 2) % 3][iter_col] != piece:
                squares.append([(iter_row + 2) % 3, iter_col])

    # find danger in top left to bottom right diagonal
    for existing in range(3):
        other_existing = (existing + 1) % 3
        danger_move = (existing + 2) % 3
        if board[existing][existing] == opponent and board[other_existing][other_existing] == opponent \
                and board[danger_move][danger_move] != piece:
            squares.append([danger_move, danger_move])

    # find danger in bottom left to top right diagonal
    if board[2][0] == opponent and board[1][1] == opponent and board[0][2] != piece:
        squares.append([0, 2])
    if board[0][2] == opponent and board[2][0] == opponent and board[1][1] != piece:
        squares.append([1, 1])
    if board[1][1] == opponent and board[0][2] == opponent and board[2][0] != piece:
        squares.append([2, 0])

    return squares


def swap_turn(piece):
    if piece == X_PIECE:
        return O_PIECE
    else:
        return X_PIECE

