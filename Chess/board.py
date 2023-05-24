from doctest import FAIL_FAST
from shutil import move
from tabnanny import check
from unittest import mock
import numpy as np
import pandas as pd
import pygame
from soupsieve import select

from piece import Bishop
from piece import King
from piece import Queen
from piece import Pawn
from piece import Rook
from piece import Knight
import copy


class Board:
    def __init__(self, rows, cols, fen):
        self.rows = rows
        self.cols = cols
        self.selected_piece = False
        self.whitemove = True
        self.turn = 0
        self.turn_log = []
        self.black_king_pos = (0, 4)
        self.white_king_pos = (7, 4)

        # Turn log : [first 2 digits which piece  + 2 digits start position + 2 digits end positions +  2 digits special actions (None) ]
        # Special actions :
        # Pawn promotion 1 + piece digit
        # Pawn Jump = 02
        # Castle King Side = 03 + 01
        # Castle Queen Side = 03 + 02

        self.piece_id = {'r': 22, 'n': 23, 'b': 24, 'q': 25, 'k': 26,
                         'p': 21, 'R': 12, 'N': 13, 'B': 14, 'Q': 16, 'K': 15, 'P': 11}
        self.pieceClassid = {12: Rook, 13: Knight, 14: Bishop, 11: Pawn,
                             15: King, 16: Queen, 14: Bishop, 13: Knight, 12: Rook, 21: Pawn, 22: Rook, 23: Knight, 24: Bishop, 25: Queen, 26: King}
        self.chessboard = [[0 for i in range(0, 8)]for i in range(0, 8)]
        self.col_values = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.row_values = [i for i in range(0, 8)]
        self.chessboarddf = pd.DataFrame(
            data=self.chessboard, index=self.row_values, columns=self.col_values)

        self.fen = fen
        self.fen = self.fen.replace('/', '')

# black pieces
        """
        self.board[0][0] = Rook(0, 0, "b", 12)
        self.board[0][1] = Knight(0, 1, "b", 13)
        self.board[0][2] = Bishop(0, 2, "b", 14)
        self.board[0][3] = Queen(0, 3, "b", 15)
        self.board[0][4] = King(0, 4, "b", 16)
        self.board[0][5] = Bishop(0, 5, "b", 14)
        self.board[0][6] = Knight(0, 6, "b", 13)
        self.board[0][7] = Rook(0, 7, "b", 12)

        self.board[1][0] = Pawn(1, 0, "b", 11)
        self.board[1][1] = Pawn(1, 1, "b", 11)
        self.board[1][2] = Pawn(1, 2, "b", 11)
        self.board[1][3] = Pawn(1, 3, "b", 11)
        self.board[1][4] = Pawn(1, 4, "b", 11)
        self.board[1][5] = Pawn(1, 5, "b", 11)
        self.board[1][6] = Pawn(1, 6, "b", 11)
        self.board[1][7] = Pawn(1, 7, "b", 11)
    # white pieces
        self.board[7][0] = Rook(7, 0, "w", 22)


        self.board[6][0] = Pawn(6, 0, "w", 21)
        self.board[6][1] = Pawn(6, 1, "w", 21)
        self.board[6][2] = Pawn(6, 2, "w", 21)
        self.board[6][3] = Pawn(6, 3, "w", 21)
        self.board[6][4] = Pawn(6, 4, "w", 21)print
        self.board[6][5] = Pawn(6, 5, "w", 21)
        self.board[6][6] = Pawn(6, 6, "w", 21)
        self.board[6][7] = Pawn(6, 7, "w", 21)
        """

    def initializeboard(self):
        row = 0
        col = 0
        for cord in self.fen:
            if cord.isnumeric():
                col += int(cord)
            else:
                self.chessboarddf.iloc[row][col] = self.piece_id[cord]
                col += 1
            if col >= self.cols:
                col = col - 8
                row += 1
                if row > self.rows:
                    break
        # Make Data board

        self.showboard = [[0 for i in range(0, 8)]for i in range(0, 8)]

        for row in range(0, self.chessboarddf.shape[0]):
            for col in range(0, self.chessboarddf.shape[1]):
                if self.chessboarddf.iloc[row][col] != 0:
                    print('ID:', self.chessboarddf.iloc[row][col])
                    self.showboard[row][col] = self.pieceClassid[self.chessboarddf.iloc[row][col]](
                        row, col, self.chessboarddf.iloc[row][col])
                    print('piece added')
                else:
                    self.showboard[row][col] = 0
        # Make Show board

        print(self.showboard)
        print(self.chessboarddf)

    def draw(self, win, board):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.chessboarddf.iloc[i][j] != 0:
                    self.showboard[i][j].draw(
                        win, board, self.showboard, self.turn_log)
        if self.selected_piece != False:
            self.showboard[self.selected_piece[0]
                           ][self.selected_piece[1]].draw(win, board, self.showboard, self.turn_log)

    def is_king_in_check_by_move(self, start, end):
        board = copy.deepcopy(self.chessboarddf)
        showboard = copy.deepcopy(self.showboard)

        board.iloc[end[0]][end[1]] = board.iloc[start[0]][start[1]]
        showboard[end[0]][end[1]] = showboard[start[0]][start[1]]
        board.iloc[start[0]][start[1]] = 0
        showboard[start[0]][start[1]] = 0
        showboard[end[0]][end[1]].row = end[0]
        showboard[end[0]][end[1]].col = end[1]

        if (self.whitemove):
            for x in range(0, 8):
                for y in range(0, 8):
                    if board.iloc[x][y] == 15:
                        self.white_king_pos = (x, y)
            #print('Black KING POS: \n')
            # print(self.white_king_pos)
            return showboard[self.white_king_pos[0]][self.white_king_pos[1]].is_king_in_check(board, showboard, self.turn_log)
        else:
            for x in range(0, 8):
                for y in range(0, 8):
                    if board.iloc[x][y] == 26:
                        self.black_king_pos = (x, y)
            #print('White KING POS: \n')
            # print(self.black_king_pos)
            return showboard[self.black_king_pos[0]][self.black_king_pos[1]].is_king_in_check(board, showboard, self.turn_log)

    def is_king_checkmated(self):

        if (self.whitemove):
            for x in range(0, 8):
                for y in range(0, 8):
                    if self.chessboarddf.iloc[x][y] == 15:
                        self.white_king_pos = (x, y)
                        king_checked = self.showboard[self.white_king_pos[0]][self.white_king_pos[1]].is_king_in_check(
                            self.chessboarddf, self.showboard, self.turn_log)
        else:
            for x in range(0, 8):
                for y in range(0, 8):
                    if self.chessboarddf.iloc[x][y] == 26:
                        self.black_king_pos = (x, y)
                        king_checked = self.showboard[self.black_king_pos[0]][self.black_king_pos[1]].is_king_in_check(
                            self.chessboarddf, self.showboard, self.turn_log)
        if (king_checked == True):
            possible_moves = []
            if (self.whitemove):
                for row in range(0, 8):
                    for col in range(0, 8):

                        if ((self.chessboarddf.iloc[row][col] <= 20) and (self.chessboarddf.iloc[row][col] != 0)):
                            # print(chessboarddf.iloc[row][col])
                            piece_valid_moves = self.showboard[row][col].valid_moves(
                                self.chessboarddf, self.showboard, self.turn_log, False)
                            valid_moves = piece_valid_moves[0]
                            valid_moves_command = piece_valid_moves[1]

                            for i in range(0, len(valid_moves)):
                                if (self.is_king_in_check_by_move((row, col), (valid_moves[i][0], valid_moves[i][1])) == False):
                                    possible_moves.extend(
                                        valid_moves_command[i])

                            #print('piece valid moves: \n')
                            # print(valid_moves)
            elif (self.whitemove == False):
                for row in range(0, 8):
                    for col in range(0, 8):

                        if ((self.chessboarddf.iloc[row][col] >= 20) and (self.chessboarddf.iloc[row][col] != 0)):
                            # print(chessboarddf.iloc[row][col])
                            piece_valid_moves = self.showboard[row][col].valid_moves(
                                self.chessboarddf, self.showboard, self.turn_log, False)
                            valid_moves = piece_valid_moves[0]
                            valid_moves_command = piece_valid_moves[1]

                            for i in range(0, len(valid_moves)):
                                if (self.is_king_in_check_by_move((row, col), (valid_moves[i][0], valid_moves[i][1])) == False):
                                    possible_moves.extend(
                                        valid_moves_command[i])
            if len(possible_moves) >= 1:
                print('There are {} moves that can be make from this position'.format(
                    len(possible_moves)))
            else:
                if (self.whitemove):
                    print("Black is victorious, White is checkmated")
                    pygame.QUIT
                else:
                    print('White is victorious, Black is checkmated')
                    pygame.QUIT

    def select(self, inrow, incol):
        # print(self.selected_piece)
        if self.selected_piece:
            self.move(self.selected_piece, (inrow, incol))
        else:
            for i in range(self.cols):
                for j in range(self.rows):
                    if self.chessboarddf.iloc[j][i] != 0:
                        self.showboard[j][i].selected = False

            if self.chessboarddf.iloc[inrow][incol] != 0:
                if ((self.chessboarddf.iloc[inrow][incol] <= 19) == self.whitemove):
                    self.showboard[inrow][incol].selected = True
                    # print(self.whitemove)
                    self.selected_piece = (inrow, incol)

    def move(self, start, end):
        piece_valid_moves = self.showboard[start[0]][start[1]].valid_moves(
            self.chessboarddf, self.showboard, self.turn_log)
        move_index = -1

        # print(piece_valid_moves)
        for i in range(0, len(piece_valid_moves[0])):
            if piece_valid_moves[0][i] == end:
                move_index = i
                #print('Ran here 2')
                # print(i)

        if (move_index != -1):
            if (self.is_king_in_check_by_move(start, end) == False):
                # if (self.is_king_in_check(start,end)):

                #print('Ran here')
                # print(self.chessboarddf)
                # print(self.showboard)
                # print(piece_valid_moves)
                piece_valid_moves_command = piece_valid_moves[1][move_index]

                if ((piece_valid_moves_command[5] == 0) or (piece_valid_moves_command[5] == 2)):
                    # Find Index of the list:
                    selected_piece = self.showboard[start[0]][start[1]]

                    # removed = self.chessboarddf[end[1]][end[0]]
                    self.showboard[start[0]][start[1]].row = end[0]
                    self.showboard[start[0]][start[1]].col = end[1]
                    self.showboard[start[0]][start[1]].selected = False
                    self.showboard[end[0]][end[1]
                                           ] = self.showboard[start[0]][start[1]]
                    self.showboard[start[0]][start[1]] = 0
                    self.chessboarddf.iloc[end[0]][end[1]
                                                   ] = self.chessboarddf.iloc[start[0]][start[1]]
                    self.chessboarddf.iloc[start[0]][start[1]] = 0

                    if ((self.chessboarddf.iloc[end[0]][end[1]] == 21) or (self.chessboarddf.iloc[end[0]][end[1]] == 11)):
                        # Pawn promotion
                        if ((end[0] == 7) or (end[0] == 0)):
                            piece_valid_moves_command[5] = 1
                            self.promotionchoice = -1
                            while ((self.promotionchoice >= 5) or (self.promotionchoice <= 0)):
                                self.promotionchoice = int(
                                    input("1.Queen,2.Rook,3.Knight,4.Bishop"))
                            if self.showboard[end[0]][end[1]].color == 'w':
                                piece_valid_moves_command[6] = self.promotionchoice
                                if self.promotionchoice == 1:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[16](
                                        end[0], end[1], 16)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 16

                                elif self.promotionchoice == 2:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[12](
                                        end[0], end[1], 12)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 12
                                elif self.promotionchoice == 3:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[13](
                                        end[0], end[1], 13)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 13
                                elif self.promotionchoice == 4:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[14](
                                        end[0], end[1], 14)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 14

                            elif self.showboard[end[0]][end[1]].color == 'b':
                                piece_valid_moves_command[6] = self.promotionchoice

                                if self.promotionchoice == 1:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[25](
                                        end[0], end[1], 25)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 25

                                elif self.promotionchoice == 2:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[22](
                                        end[0], end[1], 22)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 22
                                elif self.promotionchoice == 3:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[23](
                                        end[0], end[1], 23)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 23
                                elif self.promotionchoice == 4:

                                    self.showboard[end[0]][end[1]
                                                           ] = self.pieceClassid[24](
                                        end[0], end[1], 24)
                                    self.chessboarddf.iloc[end[0]][end[1]] = 24

                        # Pawn Enpassant?
                elif (piece_valid_moves_command[5] == 3):
                    #print('Ran here')
                    if piece_valid_moves_command[0] == 21:
                        self.showboard[start[0]][start[1]].row = end[0]
                        self.showboard[start[0]][start[1]].col = end[1]
                        self.showboard[start[0]][start[1]].selected = False
                        self.showboard[end[0]][end[1]
                                               ] = self.showboard[start[0]][start[1]]

                        self.showboard[start[0]][start[1]] = 0
                        self.chessboarddf.iloc[end[0]][end[1]
                                                       ] = self.chessboarddf.iloc[start[0]][start[1]]
                        self.chessboarddf.iloc[start[0]][start[1]] = 0

                        self.showboard[end[0]-1][end[1]] = 0
                        self.chessboarddf.iloc[end[0]-1][end[1]] = 0

                    elif piece_valid_moves_command[0] == 11:
                        self.showboard[start[0]][start[1]].row = end[0]
                        self.showboard[start[0]][start[1]].col = end[1]
                        self.showboard[start[0]][start[1]].selected = False
                        self.showboard[end[0]][end[1]
                                               ] = self.showboard[start[0]][start[1]]

                        self.showboard[start[0]][start[1]] = 0
                        self.chessboarddf.iloc[end[0]][end[1]
                                                       ] = self.chessboarddf.iloc[start[0]][start[1]]
                        self.chessboarddf.iloc[start[0]][start[1]] = 0

                        self.showboard[end[0]+1][end[1]] = 0
                        self.chessboarddf.iloc[end[0]+1][end[1]] = 0
                # King Castle?
                elif (piece_valid_moves_command[5] == 4):
                    #print('Ran here 1')
                    # White
                    if (piece_valid_moves_command[0] == 15):
                        if (piece_valid_moves_command[6] == 1):
                            # Move the Rook
                            self.showboard[7][7].row = 7
                            self.showboard[7][7].col = 5
                            self.showboard[7][5] = self.showboard[7][7]
                            self.chessboarddf.iloc[7][5] = self.chessboarddf.iloc[7][7]
                            self.chessboarddf.iloc[7][7] = 0
                            self.showboard[7][7] = 0

                            # Move the King
                            self.showboard[start[0]][start[1]].row = end[0]
                            self.showboard[start[0]][start[1]].col = end[1]
                            self.showboard[start[0]][start[1]].selected = False
                            self.showboard[end[0]][end[1]
                                                   ] = self.showboard[start[0]][start[1]]

                            self.showboard[start[0]][start[1]] = 0
                            self.chessboarddf.iloc[end[0]][end[1]
                                                           ] = self.chessboarddf.iloc[start[0]][start[1]]
                            self.chessboarddf.iloc[start[0]][start[1]] = 0

                        elif(piece_valid_moves_command[6] == 2):
                            # Move the Rook
                            self.showboard[7][0].row = 7
                            self.showboard[7][0].col = 3
                            self.showboard[7][3] = self.showboard[7][0]
                            self.chessboarddf.iloc[7][3] = self.chessboarddf.iloc[7][0]
                            self.chessboarddf.iloc[7][0] = 0
                            self.showboard[7][0] = 0

                            # Move the King
                            self.showboard[start[0]][start[1]].row = end[0]
                            self.showboard[start[0]][start[1]].col = end[1]
                            self.showboard[start[0]][start[1]].selected = False
                            self.showboard[end[0]][end[1]
                                                   ] = self.showboard[start[0]][start[1]]

                            self.showboard[start[0]][start[1]] = 0
                            self.chessboarddf.iloc[end[0]][end[1]
                                                           ] = self.chessboarddf.iloc[start[0]][start[1]]
                            self.chessboarddf.iloc[start[0]][start[1]] = 0
                    # Black
                    elif (piece_valid_moves_command[0] == 26):
                        #print('Ran here 2')
                        if (piece_valid_moves_command[6] == 1):
                            # Move the Rook
                            #print('Ran here 3')
                            self.showboard[0][7].row = 0
                            self.showboard[0][7].col = 5
                            self.showboard[0][5] = self.showboard[0][7]
                            self.chessboarddf.iloc[0][5] = self.chessboarddf.iloc[0][7]
                            self.chessboarddf.iloc[0][7] = 0
                            self.showboard[0][7] = 0

                            # Move the King
                            self.showboard[start[0]][start[1]].row = end[0]
                            self.showboard[start[0]][start[1]].col = end[1]
                            self.showboard[start[0]][start[1]].selected = False
                            self.showboard[end[0]][end[1]
                                                   ] = self.showboard[start[0]][start[1]]

                            self.showboard[start[0]][start[1]] = 0
                            self.chessboarddf.iloc[end[0]][end[1]
                                                           ] = self.chessboarddf.iloc[start[0]][start[1]]
                            self.chessboarddf.iloc[start[0]][start[1]] = 0

                        elif(piece_valid_moves_command[6] == 2):
                            # Move the Rook
                            self.showboard[0][0].row = 0
                            self.showboard[0][0].col = 3
                            self.showboard[0][3] = self.showboard[0][0]
                            self.chessboarddf.iloc[0][3] = self.chessboarddf.iloc[0][0]
                            self.chessboarddf.iloc[0][0] = 0
                            self.showboard[0][0] = 0

                            # Move the King
                            self.showboard[start[0]][start[1]].row = end[0]
                            self.showboard[start[0]][start[1]].col = end[1]
                            self.showboard[start[0]][start[1]].selected = False
                            self.showboard[end[0]][end[1]
                                                   ] = self.showboard[start[0]][start[1]]

                            self.showboard[start[0]][start[1]] = 0
                            self.chessboarddf.iloc[end[0]][end[1]
                                                           ] = self.chessboarddf.iloc[start[0]][start[1]]
                            self.chessboarddf.iloc[start[0]][start[1]] = 0

                    # Update King Position
                self.showboard[end[0]][end[1]].moved = True
                self.turn_log.append(piece_valid_moves_command)
                # print(self.turn_log)
                #print('Turn {}:'.format(self.turn))
                print(self.chessboarddf)
                self.selected_piece = False
                self.whitemove = (self.whitemove != True)
                print('\n')
                self.is_king_checkmated()
                self.turn += 1

            else:
                self.showboard[self.selected_piece[0]
                               ][self.selected_piece[1]].selected = False
                self.selected_piece = False

        else:
            self.showboard[self.selected_piece[0]
                           ][self.selected_piece[1]].selected = False
            self.selected_piece = False
