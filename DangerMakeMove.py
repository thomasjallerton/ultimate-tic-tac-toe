from utilities import *
from BigBoard import BigBoard
import random
from copy import deepcopy
from InlineMakeMove import inline_heuristic
from SmallBoard import SmallBoard


def danger_heuristic_make_move(available_moves, current_board: BigBoard, piece):
    best_moves = list()
    best_moves_score = -99999999
    danger_moves = get_danger_squares(current_board.board, piece)
    opponent_danger_moves = get_danger_squares(current_board.board, swap_turn(piece))
    for move in available_moves:
        score = danger_heuristic(move, current_board, piece, danger_moves, opponent_danger_moves)
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


def danger_heuristic(move, current_board: BigBoard, piece, danger_moves: list, opponent_danger_moves: list):
    copy_board: BigBoard = deepcopy(current_board)
    copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)

    score = inline_heuristic(move, current_board, piece)

    # increase score if we are winning a danger board
    for danger in danger_moves:
        if copy_board.board[danger[0]][danger[1]] == piece:
            score += 10

    # Decrease score if we are letting opponent play in a dangerous small board
    if [move[2], move[3]] in danger_moves:
        score -= 20

    # Decrease score if allowing opponent any move if there is a dangerous move
    if [move[2], move[3]] in current_board.get_won_squares() and len(danger_moves) > 0:
        score -= 15

    # Add score if we are playing in a board we can win from
    if [move[0], move[1]] in opponent_danger_moves:
        score += 15

    # Decrease score if we are letting opponent in square we can win from
    if [move[2], move[3]] in opponent_danger_moves:
        score -= 10

    # Decrease score if we are letting opponent in square we are one move from winning in
    if isinstance(copy_board.get_sub_board(move[0], move[1]), SmallBoard):
        sub_board = copy_board.get_sub_board(move[2], move[3])
        if isinstance(sub_board, SmallBoard):
            danger_sub_moves = get_danger_squares(sub_board.board, swap_turn(piece))
            if len(danger_sub_moves) > 0:
                score -= 10

    # add score if blocking opponent in sub board
    if isinstance(copy_board.get_sub_board(move[0], move[1]), SmallBoard):
        danger_sub_moves = get_danger_squares(current_board.get_sub_board(move[0], move[1]).board, piece)
        if len(danger_sub_moves) > 0:
            if [move[2], move[3]] in danger_sub_moves:
                score += 15

    return score
