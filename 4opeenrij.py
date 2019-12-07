import math

import numpy as np
import random

import pygame as pygame

ROW_COUNT = 6
COL_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE: int = 2

WINDOW_LENGTH = 4
EMPTY = 0


def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    try:
        col = int(col)
        return board[ROW_COUNT - 1][col] == 0
    except IndexError as e:
        return False
    except ValueError as e:
        return False


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # horizontaal
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # verticaal
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # positief diagonaal

    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # negatief diagonaal
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == opp_piece:
        opp_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100

    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10

    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score


def score_position(board, piece):
    score = 0
    # score center
    center_array = [int(i) for i in list(board[:, COL_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    #horizontaal

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COL_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #vertical
    for c in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #positief diagonaal
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def get_valid_location(board):
    valid_locations = []
    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)

    return valid_locations


def isterminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_location(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_location(board)
    is_terminal = isterminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 100000000000000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000000000000
            else:  #gameover
                return None, 0
        else:  # depth is 0
            return None, score_position(board, AI_PIECE)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def pick_best_move(board, piece):
    valid_locations = get_valid_location(board)
    best_col = random.choice(valid_locations)
    best_score = -10000
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


board = create_board()
print_board(board)
# print(board)
game_over = False
turn = random.randint(PLAYER, AI)

while not game_over:
    if turn == PLAYER:
        col = input("Player 1 make your move(0-6)")
        while not is_valid_location(board, col):
            col = input("Player 1 make your move(0-6)")
        if is_valid_location(board, col):
            col = int(col)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)

            if winning_move(board, PLAYER_PIECE):
                print("PLAYER 1 WINS!!!")
                game_over = True

            turn += 1
            turn = turn % 2

        else:
            turn = PLAYER

    if turn == AI and not game_over:
        # col = int(input("Player 2 make your move(0-6)"))
        # col = random.randint(0, COL_COUNT - 1)
        # col = pick_best_move(board, AI_PIECE)
        col, minimaxscore = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            # pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                print("PLAYER 2 WINS!!!")
                game_over = True

            print_board(board)

            turn += 1
            turn = turn % 2
