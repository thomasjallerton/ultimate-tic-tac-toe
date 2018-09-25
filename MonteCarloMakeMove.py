from BigBoard import BigBoard
from RandomMakeMove import *
from copy import deepcopy
from utilities import swap_turn
from pieces import *
import datetime
from math import log, sqrt

C = 1.4
calculation_time = datetime.timedelta(milliseconds=5000)
plays = {}
wins = {}


def monte_carlo_make_move(available_moves, current_board, piece):

    games = 0
    begin = datetime.datetime.utcnow()

    if not available_moves:
        return
    if len(available_moves) == 1:
        return available_moves[0]

    while datetime.datetime.utcnow() - begin < calculation_time:
        monte_carlo_play_one_game(available_moves, current_board, piece)
        games += 1

    moves_states = list()
    for move in available_moves:
        copy_state: BigBoard = deepcopy(current_board)
        copy_state.make_move(move, piece)
        moves_states.append((move, copy_state.hash()))

    percent_wins, move = max(
        (wins.get((piece, S), 0) /
         plays.get((piece, S), 1),
         p)
        for p, S in moves_states
    )
    return move


def monte_carlo_play_one_game(available_moves, current_board: BigBoard, piece):
    visited_states = set()

    next_moves = available_moves
    state = deepcopy(current_board)
    player = piece

    while True:

        moves_states = [(p, state.get_hash_of_next_move(p, piece)) for p in next_moves]

        if all(plays.get((player, S)) for p, S in moves_states):
            # If we have stats on all of the legal moves here, use them.
            log_total = log(sum(plays[(player, S)] for p, S in moves_states))
            value, move = max(
                ((wins[(player, S)] / plays[(player, S)]) +
                 C * sqrt(log_total / plays[(player, S)]), p)
                for p, S in moves_states
            )
        else:
            move = random_make_move(next_moves, state, player)

        state.make_move(move, player)
        state_hash = state.hash()

        if (player, state_hash) not in plays:
            plays[(player, state_hash)] = 0
            wins[(player, state_hash)] = 0

        visited_states.add((player, state.hash()))

        player = swap_turn(player)
        winner = state.is_game_won_winner()
        if winner != NO_PIECE:
            break

        if state.is_game_tied():
            break

        next_moves = state.get_next_possible_moves(move[0], move[1])

    for player, state in visited_states:
        if (player, state) not in plays:
            continue
        plays[(player, state)] += 1
        if player == winner:
            wins[(player, state)] += 1
