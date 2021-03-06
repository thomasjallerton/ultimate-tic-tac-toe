from ultimatetictactoe import play_game
from pieces import *
from HumanPlayer import human_player
from DangerMakeMove import danger_heuristic_make_move
from HeuristicMonteCarloishMakeMove import heuristic_monte_carloish_make_move
from MonteCarloMakeMove import monte_carlo_make_move
from InlineMakeMove import inline_heuristic_make_move
from RandomMakeMove import random_make_move
from MinimaxMakeMove import minimax_heuristic_make_move
from BoardStateHeuristicMakeMove import board_state_heuristic_make_move
import multiprocessing as mp


if __name__ == '__main__':
    x_count = 0
    o_count = 0
    ties = 0

    for i in range(100):
        winner = play_game(minimax_heuristic_make_move, human_player, True)
        if winner == O_PIECE:
            o_count += 1
            winner_str = "O won!"
        elif winner == X_PIECE:
            x_count += 1
            winner_str = "X won!"
        else:
            ties += 1
            winner_str = "Tie!"
        print("Played " + str(i + 1) + " games, " + winner_str)

    print("X Wins: " + str(x_count) + ", O Wins: " + str(o_count) + ", Ties: " + str(ties))
