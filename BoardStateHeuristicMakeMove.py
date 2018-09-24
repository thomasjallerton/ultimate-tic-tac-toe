from BigBoard import BigBoard
from SmallBoard import SmallBoard
from utilities import *
from copy import deepcopy
import random


def board_state_heuristic_make_move(available_moves, current_board: BigBoard, piece):
    best_moves = list()
    best_moves_score = -999999999
    for move in available_moves:
        copy_board: BigBoard = deepcopy(current_board)
        copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
        score = evaluate_board(copy_board, piece)
        if score > best_moves_score:
            best_moves = list()
            best_moves.append(move)
            best_moves_score = score
        elif score == best_moves_score:
            best_moves.append(move)

    random_index = random.randint(0, len(best_moves) - 1)
    return best_moves[random_index]


def evaluate_board(board: BigBoard, piece):
    opponent = swap_turn(piece)

    winner = is_game_won_winner(board.board)
    if winner == piece:
        return 1000000
    elif winner == opponent:
        return -1000000

    opponent_danger_squares = get_danger_squares(board.board, opponent)
    score = len(opponent_danger_squares) * 15
    piece_danger_squares = get_danger_squares(board.board, piece)
    score -= len(piece_danger_squares) * 20

    for iter_row in range(3):
        for iter_col in range(3):
            sub_board = board.get_sub_board(iter_row, iter_col)
            if isinstance(sub_board, SmallBoard):
                if [iter_row, iter_col] in opponent_danger_squares:
                    score += len(get_danger_squares(sub_board.board, opponent)) * 30
                else:
                    score += len(get_danger_squares(sub_board.board, opponent)) * 5

                if [iter_row, iter_col] in piece_danger_squares:
                    score -= len(get_danger_squares(sub_board.board, piece)) * 2
                else:
                    score -= len(get_danger_squares(sub_board.board, piece)) * 5

            elif sub_board == piece:
                score += 15
            elif sub_board == opponent:
                score -= 15

    return score
