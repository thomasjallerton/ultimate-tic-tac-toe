from utilities import *
from BigBoard import BigBoard
import random
from copy import deepcopy
from InlineMakeMove import sub_board_adjacent_to_existing_piece
from SmallBoard import SmallBoard


def danger_heuristic_make_move(available_moves, current_board: BigBoard, piece):
    best_moves = list()
    best_moves_score = -99999999
    danger_moves = get_danger_squares(current_board.board, piece)
    for move in available_moves:
        score = danger_heuristic(move, current_board, piece, danger_moves)
        if score > best_moves_score:
            best_moves = list()
            best_moves.append(move)
            best_moves_score = score
        elif score == best_moves_score:
            best_moves.append(move)

    if len(best_moves) == 0:
        print("No best moves!")

    random_index = random.randint(0, len(best_moves) - 1)
    return best_moves[random_index]


def danger_heuristic(move, current_board: BigBoard, piece, danger_moves: list):
    copy_board: BigBoard = deepcopy(current_board)
    initial_count = copy_board.get_number_won_sub_boards()
    copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
    after_move_count = copy_board.get_number_won_sub_boards()

    if initial_count < after_move_count:
        if is_game_won(copy_board.board):
            score = 10000
        elif copy_board.is_adjacent_in_line(move[0], move[1]):
            score = 20
        else:
            score = 15

        # increase score if we are winning a danger board
        for danger in danger_moves:
            if copy_board.board[danger[0]][danger[1]] == piece:
                score += 10
    else:
        score = sub_board_adjacent_to_existing_piece(move, copy_board, piece)

    if [move[2], move[3]] in danger_moves:
        score -= 20

    # Decrease score if allowing opponent any move if there is a dangerous move
    if [move[2], move[3]] in current_board.get_won_squares() and len(danger_moves) > 0:
        score -= 10

    # add score if blocking opponent in sub board
    if isinstance(copy_board.get_sub_board(move[0], move[1]), SmallBoard):
        danger_sub_moves = get_danger_squares(copy_board.get_sub_board(move[0], move[1]).board, piece)
        if len(danger_sub_moves) > 0:
            if [move[2], move[3]] in danger_sub_moves:
                score += 15

    return score
