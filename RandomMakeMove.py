import random


def random_make_move(available_moves, current_board, piece):
    move = random.randint(0, len(available_moves) - 1)
    return available_moves[move]
