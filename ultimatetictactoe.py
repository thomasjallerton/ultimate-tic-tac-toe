"""
 Pygame base template for opening a window
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""
import pygame
import random
import time
from copy import deepcopy

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define pieces
X_PIECE = "X"
O_PIECE = "O"
NO_PIECE = "EMPTY"
GAME_TIED = "TIED"

# Game Size
side_length = 1000
cell_length = side_length // 9


def is_game_won(board):
    # Check if won
    top_left_piece = board[0][0]
    if top_left_piece != NO_PIECE:
        if (top_left_piece == board[1][0]) & (
                top_left_piece == board[2][0]):
            return True
        if (top_left_piece == board[0][1]) & (
                top_left_piece == board[0][2]):
            return True

    middle_piece = board[1][1]
    if middle_piece != NO_PIECE:
        if (middle_piece == board[0][1]) & (
                middle_piece == board[2][1]):
            return True
        if (middle_piece == board[1][0]) & (
                middle_piece == board[1][2]):
            return True
        if (middle_piece == board[0][0]) & (
                middle_piece == board[2][2]):
            return True
        if (middle_piece == board[2][0]) & (
                middle_piece == board[0][2]):
            return True

    bottom_right_piece = board[2][2]
    if bottom_right_piece != NO_PIECE:
        if (bottom_right_piece == board[2][0]) & (
                bottom_right_piece == board[2][1]):
            return True
        if (bottom_right_piece == board[0][2]) & (
                bottom_right_piece == board[1][2]):
            return True


def get_danger_squares(board, piece):
    opponent = swap_turn(piece)
    squares = []

    # find danger in rows
    for iter_row in range(3):
        for iter_col in range(3):
            if board[iter_row][iter_col % 3] == opponent \
                    and board[iter_row][(iter_col + 1) % 3] == opponent:
                squares.append([iter_row, (iter_col + 2) % 3])

    # find danger in columns
    for iter_col in range(3):
        for iter_row in range(3):
            if board[iter_row % 3][iter_col] == opponent \
                    and board[(iter_row + 1) % 3][iter_col] == opponent:
                squares.append([(iter_row + 2) % 3, iter_col])

    # find danger in top left to bottom right diagonal
    for existing in range(3):
        other_existing = (existing + 1) % 3
        danger_move = (existing + 2) % 3
        if board[existing][existing] == opponent and board[other_existing][other_existing] == opponent:
            squares.append([danger_move, danger_move])

    # find danger in bottom left to top right diagonal
    if board[2][0] == opponent and board[1][1] == opponent:
        squares.append([0, 2])
    if board[0][2] == opponent and board[2][2] == opponent:
        squares.append([1, 1])
    if board[1][1] == opponent and board[0][2] == opponent:
        squares.append([2, 0])

    return squares


# --------------------------------------------------------------------------------------------------
class SmallBoard:
    def __init__(self, outer_row, outer_col):
        self.board = [[NO_PIECE for i in range(3)] for j in range(3)]
        self.outer_row = outer_row
        self.outer_col = outer_col

    def is_game_tied(self):
        if is_game_won(self.board):
            return True

        for iter_row in range(3):
            for iter_column in range(3):
                if self.board[iter_row][iter_column] == NO_PIECE:
                    return False
        return True

    def get_available_moves(self):
        available_moves = []

        for iter_row in range(3):
            for iter_column in range(3):
                if self.board[iter_row][iter_column] == NO_PIECE:
                    available_moves.append([self.outer_row, self.outer_col, iter_row, iter_column])
        return available_moves

    def set_piece(self, inner_row, inner_col, piece):
        self.board[inner_row][inner_col] = piece

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_piece_count(self, piece):
        count = 0
        for iter_row in range(3):
            for iter_column in range(3):
                if self.board[iter_row][iter_column] == piece:
                    count += 1
        return count

    def is_adjacent(self, row, col):
        piece = self.board[row][col]
        if (row == 1 and col == 1) or (row % 2 == 0 and col % 2 == 0):  # if corner or centre
            for iter_row in range(max(row - 1, 0), min(row + 2, 3)):
                for iter_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if (iter_row != row or iter_col != col) and self.board[iter_row][iter_col] == piece:
                        return True
        else:  # if middle side
            for iter_row in range(max(row - 1, 0), min(row + 2, 3)):
                for iter_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if ((iter_row == row) ^ (iter_col == col)) and self.board[iter_row][iter_col] == piece:
                        return True
        return False


# --------------------------------------------------------------------------------------------------
class BigBoard:
    def __init__(self):
        self.board = [[SmallBoard(row_iter, col_iter) for col_iter in range(3)] for row_iter in range(3)]

    def is_game_won(self):
        if is_game_won(self.board):
            return True
        else:
            return False

    def is_game_tied(self):
        for iter_row in range(3):
            for iter_column in range(3):
                if isinstance(self.board[iter_row][iter_column], SmallBoard):
                    return False
        return True

    def set_board_piece_if_won(self, played_row, played_column, players_turn):
        if is_game_won(self.board[played_row][played_column].board):
            self.board[played_row][played_column] = players_turn
        elif self.board[played_row][played_column].is_game_tied():
            self.board[played_row][played_column] = NO_PIECE

    def get_available_moves(self):
        available_moves = []
        for iter_row in range(3):
            for iter_column in range(3):
                if isinstance(self.board[iter_row][iter_column], SmallBoard):
                    available_moves += self.board[iter_row][iter_column].get_available_moves()
        return available_moves

    def get_next_possible_moves(self, selected_row, selected_column):
        if isinstance(self.board[selected_row][selected_column], SmallBoard):
            return self.board[selected_row][selected_column].get_available_moves()
        else:
            return self.get_available_moves()

    def set_sub_piece(self, outer_row, outer_col, inner_row, inner_col, piece):
        self.board[outer_row][outer_col].set_piece(inner_row, inner_col, piece)
        self.set_board_piece_if_won(outer_row, outer_col, piece)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_number_won_sub_boards(self):
        count = 0
        for iter_row in range(3):
            for iter_column in range(3):
                if not isinstance(self.board[iter_row][iter_column], SmallBoard):
                    count += 1
        return count

    def get_sub_board(self, row, column):
        return self.board[row][column]

    def is_adjacent(self, row, col):
        piece = self.board[row][col]
        if (row == 1 and col == 1) or (row % 2 == 0 and col % 2 == 0):  # if corner or centre
            for iter_row in range(max(row - 1, 0), min(row + 2, 3)):
                for iter_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if (iter_row != row or iter_col != col) and self.board[iter_row][iter_col] == piece:
                        return True
        else:  # if middle side
            for iter_row in range(max(row - 1, 0), min(row + 2, 3)):
                for iter_col in range(max(col - 1, 0), min(col + 2, 3)):
                    if ((iter_row == row) ^ (iter_col == col)) and self.board[iter_row][iter_col] == piece:
                        return True
        return False


# -------- Random AI ----------------------
def random_make_move(available_moves, current_board, piece):
    move = random.randint(0, len(available_moves) - 1)
    return available_moves[move]


# -------- Don't play danger moves Heuristic AI ---------------
def danger_heuristic_make_move(available_moves, current_board: BigBoard, piece):
    best_moves = list()
    best_moves_score = 0
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


def danger_heuristic(move, current_board, piece, danger_moves):
    copy_board: BigBoard = deepcopy(current_board)
    initial_count = copy_board.get_number_won_sub_boards()
    copy_board.set_sub_piece(move[0], move[1], move[2], move[3], piece)
    after_move_count = copy_board.get_number_won_sub_boards()

    if initial_count < after_move_count:
        if is_game_won(copy_board.board):
            score = 10000
        elif copy_board.is_adjacent(move[0], move[1]):
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

    # add score if blocking opponent in sub board
    if isinstance(copy_board.get_sub_board(move[0], move[1]), SmallBoard):
        danger_sub_moves = get_danger_squares(copy_board.get_sub_board(move[0], move[1]).board, piece)
        if [move[2], move[3]] in danger_sub_moves:
            score += 10

    return score


# -------- Adjacent Heuristic AI -------------------
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
        if copy_board.is_adjacent(move[0], move[1]):
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
        if sub_board.is_adjacent(move[2], move[3]):
            return 10
        else:
            return 5


# ---------- Play moves that win Heuristic AI ----------------
def simple_heuristic_make_move(available_moves, current_board, piece):
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


# -----------Utility Functions---------------------------------------------------------
def swap_turn(piece):
    if piece == X_PIECE:
        return O_PIECE
    else:
        return X_PIECE


# -------- Main Program Loop --------------
def play_game(x_turn, o_turn):
    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (side_length, side_length)

    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

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
            game_board.set_sub_piece(move[0], move[1], move[2], move[3], current_turn)

            if game_board.is_game_won():
                game_winner = current_turn

            if game_board.is_game_tied():
                game_winner = NO_PIECE

            current_turn = swap_turn(current_turn)
            current_available_moves = game_board.get_next_possible_moves(move[2], move[3])

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


x_count = 0
o_count = 0
ties = 0
for i in range(100):
    winner = play_game(simple_heuristic_make_move, danger_heuristic_make_move)
    print("Played " + str(i + 1) + " games")
    if winner == O_PIECE:
        o_count += 1
    elif winner == X_PIECE:
        x_count += 1
    else:
        ties += 1

print("X Wins: " + str(x_count) + ", O Wins: " + str(o_count) + ", Ties: " + str(ties))
