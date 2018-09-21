import random
from BigBoard import BigBoard
from copy import deepcopy
from SmallBoard import SmallBoard


def adjacent_heuristic_make_move(available_moves, current_board, piece):
    best_moves = list()
    best_moves_score = 0
    for move in available_moves:
        score = adjacent_heuristic(move, current_board, piece)
        if score > best_moves_score:
            best_moves = list()
            best_moves.append(move)
            best_moves_score = score
        elif score == best_moves_score:
            best_moves.append(move)

    random_index = random.randint(0, len(best_moves) - 1)
    return best_moves[random_index]


def adjacent_heuristic(move, current_board, piece):
    copy_board: BigBoard = deepcopy(current_board)
    initial_count = copy_board.get_number_won_sub_boards()
    copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
    after_move_count = copy_board.get_number_won_sub_boards()

    if initial_count < after_move_count:
        if copy_board.is_adjacent_in_line(move[0], move[1]):
            score = 20
        else:
            score = 15
    else:
        score = sub_board_adjacent_to_existing_piece(move, copy_board, piece)

    return score


def sub_board_adjacent_to_existing_piece(move, current_board: BigBoard, piece):
    sub_board: SmallBoard = current_board.get_sub_board(move[0], move[1])
    if sub_board.get_piece_count(piece) == 1:
        return 1
    else:
        if sub_board.is_adjacent_in_line(move[2], move[3]):
            return 10
        else:
            return 5

