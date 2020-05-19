import math
import sys

import numpy as np
import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
COLUMN_COUNT = 7
ROW_COUNT = 6
GAMEOVER = False


def draw_board(real_board):
    board = real_board.copy()
    board = np.flip(board, 0)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == PLAYER2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def create_board():
    board = np.zeros((6, 7))
    return board


def is_valid_location(matrix, col):
    return not matrix[0][col]


def valid_location(matrix, col):
    for row in range(ROW_COUNT - 1, -1, -1):
        if matrix[row][col] == 0:
            return row


def drop_piece(matrix, col, player):
    if is_valid_location(matrix, col):
        row = valid_location(matrix, col)
        matrix[row][col] = player
        return True
    return False


def is_won(matrix, player):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if matrix[row][col] == player and matrix[row + 1][col] == player and matrix[row + 2][col] == player and \
                    matrix[row + 3][col] == player:
                print("column win")
                return True

    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if matrix[row][col] == player and matrix[row][col + 1] == player and matrix[row][col + 2] == player and \
                    matrix[row][col + 3] == player:
                print("row win.")
                return True

    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if matrix[row][col] == player and matrix[row + 1][col + 1] == player and matrix[row + 2][
                col + 2] == player and \
                    matrix[row + 3][col + 3] == player:
                print("lef to right  up to down diagonal.")
                return True

    for row in range(ROW_COUNT - 1, ROW_COUNT - 3, -1):
        for col in range(COLUMN_COUNT - 3):
            if matrix[row][col] == player and matrix[row - 1][col + 1] == player and matrix[row - 2][
                col + 2] == player and \
                    matrix[row - 3][col + 3] == player:
                print("lef to right  down to up diagonal.")
                return True

    return False


board = create_board()
print(board)
turnPlayer = PLAYER1
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while GAMEOVER != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turnPlayer == PLAYER1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turnPlayer == PLAYER1:
                # PLAYER 1
                print("You are player1")
                print("pos ", event.pos)
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                drop_piece(board, col, turnPlayer)
                draw_board(board)
                pygame.display.update()
                if is_won(board, turnPlayer):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    GAMEOVER = True
                print(board)
                turnPlayer = PLAYER2
            else:
                # PLAYER 2
                print("YOU ARE PLAYER 2")
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                drop_piece(board, col, turnPlayer)
                draw_board(board)
                pygame.display.update()

                if is_won(board, turnPlayer):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    GAMEOVER = True
                print(board)
                turnPlayer = PLAYER1
pygame.time.wait(3000)
# pygame.display.quit()
# pygame.quit()
# sys.exit()
