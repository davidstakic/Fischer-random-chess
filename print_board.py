from constants import *
from copy import deepcopy
from colorama import Back, Style, init, Fore

# Initialize colorama
init(autoreset=True)

def convert_to_black_chess_symbols(row):
        for i in range(len(row)):
            if row[i] == PAWN:
                row[i] = '♟'
            elif row[i] == KING:
                row[i] = '♚'
            elif row[i] == QUEEN:
                row[i] = '♛'
            elif row[i] == KNIGHT:
                row[i] = '♞'
            elif row[i] == ROOK:
                row[i] = '♜'
            elif row[i] == BISHOP:
                row[i] = '♝'
        return row

def convert_to_white_chess_symbols(row):
    for i in range(len(row)):
        if row[i] == PAWN:
            row[i] = '♙'
        elif row[i] == KING:
            row[i] = '♔'
        elif row[i] == QUEEN:
            row[i] = '♕'
        elif row[i] == KNIGHT:
            row[i] = '♘'
        elif row[i] == ROOK:
            row[i] = '♖'
        elif row[i] == BISHOP:
            row[i] = '♗'
    return row

def print_board(first_row):
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[0] = convert_to_black_chess_symbols(deepcopy(first_row))
    board[7] = convert_to_white_chess_symbols(deepcopy(first_row))
    pawn_row = 8 * [PAWN]
    board[1] = convert_to_black_chess_symbols(deepcopy(pawn_row))
    board[6] = convert_to_white_chess_symbols(deepcopy(pawn_row))

    for i in range(8):
        for j in range(8):
            piece = board[i][j] + ' '
            if (i + j) % 2 == 0:
                cell_color = Back.CYAN
                # cell_color = Back.LIGHTYELLOW_EX
            else:
                cell_color = Back.MAGENTA
                # cell_color = Back.LIGHTGREEN_EX

            if piece != ' ':
                if i == 0 or i == 1:
                    print(f'{cell_color}{Fore.BLACK}{Style.NORMAL}{piece}', end='')
                else:
                    print(f'{cell_color}{Fore.BLACK}{Style.NORMAL}{piece}', end='')
            else:
                print(f'{cell_color} ', end=' ')
        print(Back.RESET)