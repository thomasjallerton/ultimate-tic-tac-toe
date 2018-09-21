from ultimatetictactoe import cell_length
from pieces import NO_PIECE
import contextlib
with contextlib.redirect_stdout(None):
    import pygame


# Human Player
def human_player(available_moves, current_board, piece):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // cell_length
            row = pos[1] // cell_length
            if column > 8:
                column = 8
            if row > 8:
                row = 8

            small_row = row % 3
            small_col = column % 3

            big_row = row // 3
            big_col = column // 3

            if [big_row, big_col, small_row, small_col] in available_moves:
                return [big_row, big_col, small_row, small_col]
    return NO_PIECE
