import random
from BigBoard import BigBoard
from copy import deepcopy
from SmallBoard import SmallBoard
from utilities import *


def inline_heuristic_make_move(available_moves, current_board, piece):
    best_moves = list()
    best_moves_score = 0
    for move in available_moves:
        score = inline_heuristic(move, current_board, piece)
        if score > best_moves_score:
            best_moves = list()
            best_moves.append(move)
            best_moves_score = score
        elif score == best_moves_score:
            best_moves.append(move)

    random_index = random.randint(0, len(best_moves) - 1)
    return best_moves[random_index]


def inline_heuristic(move, current_board: BigBoard, piece):
    copy_board: BigBoard = deepcopy(current_board)
    initial_count = copy_board.get_number_won_sub_boards()
    copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
    after_move_count = copy_board.get_number_won_sub_boards()
    opponent = swap_turn(piece)

    if initial_count < after_move_count:
        if is_game_won(copy_board.board):
            score = 10000
        elif len(get_danger_squares(current_board.board, opponent)) < len(get_danger_squares(copy_board.board, opponent)):
            score = 20
        else:
            score = 15
    else:
        sub_board: SmallBoard = current_board.get_sub_board(move[0], move[1]).board
        copy_sub_board: SmallBoard = copy_board.get_sub_board(move[0], move[1]).board
        if len(get_danger_squares(sub_board, opponent)) < len(get_danger_squares(copy_sub_board, opponent)):
            score = 10
        else:
            score = 5

    return score


