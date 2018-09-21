import random
from BigBoard import BigBoard
from copy import deepcopy


def simple_heuristic_make_move(available_moves, current_board, piece):
    best_moves = list()
    best_moves_score = 0
    for move in available_moves:
        score = simple_heuristic(move, current_board, piece)
        if score > best_moves_score:
            best_moves = list()
            best_moves.append(move)
            best_moves_score = score
        elif score == best_moves_score:
            best_moves.append(move)

    random_index = random.randint(0, len(best_moves) - 1)
    return best_moves[random_index]


def simple_heuristic(move, current_board, piece):
    copy_board: BigBoard = deepcopy(current_board)
    initial_count = copy_board.get_number_won_sub_boards()
    copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
    after_move_count = copy_board.get_number_won_sub_boards()

    if initial_count < after_move_count:
        score = 5
    else:
        score = 1

    return score