from BigBoard import BigBoard
import multiprocessing as mp
from RandomMakeMove import *
from copy import deepcopy
from utilities import swap_turn


def monte_carlo_make_move(available_moves, current_board, piece):
    move_wins = {}
    max_count = -1
    max_move = available_moves[0]

    for move in available_moves:
        move_wins[move_hash(move)] = 0

    output = mp.Queue()
    # Play many games
    processes = [mp.Process(None, monte_carlo_play_one_game, None, (available_moves, deepcopy(current_board), piece,
                                                                    output), {}) for x in range(100)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    results = [output.get() for p in processes]

    for result in results:
        if result[0]:
            hash_res = move_hash(result[0][1])
            move_wins[hash_res] += 1
            count = move_wins[hash_res]
            if count > max_count:
                max_count = count
                max_move = result[0][1]

    return max_move


def monte_carlo_play_one_game(available_moves, current_board: BigBoard, piece, result):
    game_won = False
    first_move = random_make_move(available_moves, current_board, piece)
    move = first_move
    opponent_piece = swap_turn(piece)
    while not game_won:
        current_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
        if current_board.is_game_won():
            # Player won, return won and first move
            result.put([[True, first_move]])
            return
        if current_board.is_game_tied():
            result.put([False, first_move])
            return
        opponent_possible_moves = current_board.get_next_possible_moves(move[2], move[3])
        opponent_move = random_make_move(opponent_possible_moves, current_board, opponent_piece)
        current_board.set_sub_piece(opponent_move[0], opponent_move[1], opponent_move[2], opponent_move[3],
                                    opponent_piece)
        if current_board.is_game_won():
            # Opponent won, return lost and first move
            result.put([False, first_move])
            return
        if current_board.is_game_tied():
            result.put([False, first_move])
            return
        move = random_make_move(current_board.get_next_possible_moves(opponent_move[2], opponent_move[3]),
                                current_board, piece)


def move_hash(move):
    return int("{0}{1}{2}{3}".format(str(move[0]), str(move[1]), str(move[2]), str(move[3])))