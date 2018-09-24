"""
 Pygame base template for opening a window
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""
import time
from BigBoard import BigBoard
from utilities import *
from SmallBoard import SmallBoard
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game Size
side_length = 1000
cell_length = side_length // 9


def play_game(x_turn, o_turn, draw = True):
    screen = 0
    size = 0

    if draw:
        pygame.init()

        # Set the width and height of the screen [width, height]
        size = (side_length, side_length)

        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Ultimate tic tac toe")

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

    current_turn = X_PIECE
    game_board = BigBoard()
    current_available_moves = game_board.get_available_moves()

    # Loop until the user clicks the close button.
    game_winner = None
    while game_winner is None:
        # Game logic

        if current_turn == X_PIECE:
            move = x_turn(current_available_moves, game_board, current_turn)
        else:
            move = o_turn(current_available_moves, game_board, current_turn)

        if move != NO_PIECE:
            if len(move) < 4:
                print(current_turn, "could not make a move", move)
            game_board.set_sub_piece(move[0], move[1], move[2], move[3], current_turn)

            if game_board.is_game_won():
                game_winner = current_turn
            elif game_board.is_game_tied():
                game_winner = NO_PIECE

            current_turn = swap_turn(current_turn)
            current_available_moves = game_board.get_next_possible_moves(move[2], move[3])

        if draw:
            # Clear Board
            screen.fill(WHITE)
            # Draw board
            grey_lines = [1, 2, 4, 5, 7, 8]

            for i in grey_lines:
                pygame.draw.rect(screen, GREY,
                                 [side_length * i // 9 - (side_length // 120), 0, side_length // 60, side_length])
                pygame.draw.rect(screen, GREY,
                                 [0, side_length * i // 9 - (side_length / 120), side_length, side_length // 60])

            black_lines = [1, 2]

            for i in black_lines:
                pygame.draw.rect(screen, BLACK, [side_length * i // 3 - (side_length // 120), 0, size[0] // 60, size[1]])
                pygame.draw.rect(screen, BLACK,
                                 [0, side_length * i // 3 - (side_length // 120), side_length, side_length // 60])

            for outer_row in range(3):
                for outer_col in range(3):
                    sub_board = game_board.get_piece(outer_row, outer_col)
                    if isinstance(sub_board, SmallBoard):
                        for inner_row in range(3):
                            for inner_col in range(3):
                                row = outer_row * 3 + inner_row
                                column = outer_col * 3 + inner_col

                                if sub_board.get_piece(inner_row, inner_col) == O_PIECE:
                                    x_pos = cell_length * column + cell_length // 2
                                    y_pos = cell_length * row + cell_length // 2

                                    pygame.draw.circle(screen, RED, [x_pos, y_pos], cell_length // 3,
                                                       int((cell_length // 3) * 0.1))

                                if sub_board.get_piece(inner_row, inner_col) == X_PIECE:
                                    top = cell_length * row + cell_length // 5
                                    left = cell_length * column + cell_length // 5
                                    bottom = top + int(cell_length * 0.6)
                                    right = left + int(cell_length * 0.6)

                                    pygame.draw.line(screen, BLUE, (left, top), (right, bottom), 5)
                                    pygame.draw.line(screen, BLUE, (right, top), (left, bottom), 5)
                    else:
                        if sub_board == O_PIECE:
                            x_pos = cell_length * 3 * outer_col + (cell_length * 3) // 2
                            y_pos = cell_length * 3 * outer_row + (cell_length * 3) // 2

                            pygame.draw.circle(screen, RED, [x_pos, y_pos], cell_length, int(cell_length * 0.1))

                        if sub_board == X_PIECE:
                            top = cell_length * outer_row * 3 + cell_length // 4
                            left = cell_length * outer_col * 3 + cell_length // 4
                            bottom = top + int(cell_length * 2.5)
                            right = left + int(cell_length * 2.5)

                            pygame.draw.line(screen, BLUE, (left, top), (right, bottom), 10)
                            pygame.draw.line(screen, BLUE, (right, top), (left, bottom), 10)

            for move in current_available_moves:
                row: int = move[0] * 3 + move[2]
                column: int = move[1] * 3 + move[3]
                top = cell_length * row + cell_length // 5
                left = cell_length * column + cell_length // 5
                width = int(cell_length * 0.6)
                pygame.draw.rect(screen, GREEN, [left, top, width, width])

            mouse_pos = pygame.mouse.get_pos()
            if current_turn == X_PIECE:
                x_pos = mouse_pos[0]
                y_pos = mouse_pos[1]

                top = y_pos - cell_length // 3
                left = x_pos - cell_length // 3
                bottom = top + int(cell_length * 0.6)
                right = left + int(cell_length * 0.6)

                pygame.draw.line(screen, BLUE, (left, top), (right, bottom), 5)
                pygame.draw.line(screen, BLUE, (right, top), (left, bottom), 5)
            else:
                pygame.draw.circle(screen, RED, mouse_pos, cell_length // 3,
                                   int((cell_length // 3) * 0.1))

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

    # Close the window and quit.
    time.sleep(0.2)
    pygame.quit()
    return game_winner



