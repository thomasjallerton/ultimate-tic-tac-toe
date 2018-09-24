from BigBoard import BigBoard
from BoardStateHeuristicMakeMove import evaluate_board
from copy import deepcopy
from utilities import swap_turn
import random


def minimax_heuristic_make_move(available_moves, current_board: BigBoard, piece):
    best_moves = list()
    best_moves_score = -999999999
    for move in available_moves:
        score = evaluate_move(move, current_board, piece)
        if score > best_moves_score:
            best_moves = list()
            best_moves.append(move)
            best_moves_score = score
        elif score == best_moves_score:
            best_moves.append(move)

    random_index = random.randint(0, len(best_moves) - 1)
    return best_moves[random_index]


def evaluate_move(move, current_board: BigBoard, piece):
    opponent = swap_turn(piece)
    worst_score = 9999999
    our_move_board = deepcopy(current_board)
    our_move_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)

    opponent_moves = our_move_board.get_next_possible_moves(move[2], move[3])

    for opponent_move in opponent_moves:
        opponent_move_board = deepcopy(our_move_board)
        opponent_move_board.set_sub_piece(opponent_move[0], opponent_move[1], opponent_move[2], opponent_move[3], opponent)
        move_score = evaluate_board(opponent_move_board, piece)
        if move_score < worst_score:
            worst_score = move_score

    return worst_score
