from multiprocessing import set_forkserver_preload
from shutil import move
import pygame
import os

# Turn log : [first 2 digits which piece  + 2 digits start position + 2 digits end positions +  2 digits special actions (None) ]
# Special actions :
# Pawn promotion 1 + piece digit
# Pawn Jump = 02
# Pawn Enpassant capture = 03
# Castle King Side = 04 + 01
# Castle Queen Side = 04 + 02


w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))


b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []
for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))
for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))


class Piece():

    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, id):
        self.id = id
        self.row = row
        self.col = col
        if self.id <= 20:
            self.color = 'w'
        else:
            self.color = 'b'
        self.selected = False
        self.moved = False

    def valid_moves(self, board, showboard=None, turn_log=None):
        pass

    def isSelected(self):
        return self.selected

    def draw(self, win, board, showboard, turn_logs):

        if self.color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        x = 5 + round(self.startX + (self.col*self.rect[2]/8))
        y = 5 + round(self.startY + (self.row*self.rect[3]/8))

        win.blit(drawThis, (x, y))

        if (self.selected == True):
            pygame.draw.rect(win, (255, 0, 0), (x, y, 55, 55), 2)
            moves = self.valid_moves(board, showboard, turn_logs)[0]
            # print(moves)
            for move in moves:
                x = 31 + round(self.startX + (move[1]*self.rect[2]/8))
                y = 31 + round(self.startY + (move[0]*self.rect[3]/8))
                pygame.draw.circle(win, (255, 0, 0), (x+2, y+2), 10)

    def generate_king_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        if self.color == 'w':
            if ((i-1 >= 0) & (j-1 >= 0)):
                p = board.iloc[i-1][j-1]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i-1, j-1))
            if ((i >= 0) & (j-1 >= 0)):
                p = board.iloc[i][j-1]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i, j-1))
            if ((i+1 <= 7) & (j-1 >= 0)):
                p = board.iloc[i+1][j-1]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i+1, j-1))

            if ((i-1 >= 0) & (j+1 <= 7)):
                p = board.iloc[i-1][j+1]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i-1, j+1))
            if ((i >= 0) & (j+1 <= 7)):
                p = board.iloc[i][j+1]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i, j+1))
            if ((i+1 <= 7) & (j+1 <= 7)):
                p = board.iloc[i+1][j+1]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i+1, j+1))
            if (i-1 >= 0):
                p = board.iloc[i-1][j]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i-1, j))
            if (i+1 <= 7):
                p = board.iloc[i+1][j]
                if ((p == 0) or ((p >= 20))):
                    moves.append((i+1, j))
        elif self.color == 'b':
            if ((i-1 >= 0) & (j-1 >= 0)):
                p = board.iloc[i-1][j-1]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i-1, j-1))
            if ((i >= 0) & (j-1 >= 0)):
                p = board.iloc[i][j-1]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i, j-1))
            if ((i+1 <= 7) & (j-1 >= 0)):
                p = board.iloc[i+1][j-1]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i+1, j-1))

            if ((i-1 >= 0) & (j+1 <= 7)):
                p = board.iloc[i-1][j+1]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i-1, j+1))
            if ((i >= 0) & (j+1 <= 7)):
                p = board.iloc[i][j+1]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i, j+1))
            if ((i+1 <= 7) & (j+1 <= 7)):
                p = board.iloc[i+1][j+1]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i+1, j+1))
            if (i-1 >= 0):
                p = board.iloc[i-1][j]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i-1, j))
            if (i+1 <= 7):
                p = board.iloc[i+1][j]
                if ((p == 0) or ((p <= 20))):
                    moves.append((i+1, j))
        move_logs = []
        for move in moves:
            move_logs.append(
                [board.iloc[i][j], i, j, move[0], move[1], 0, 0])

        return (moves, move_logs)

    def generate_knight_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        if self.color == 'w':
            # Up 2 left 1

            if ((-1 < (i-2) < 8) & (-1 < (j-1) < 8)):
                p = board.iloc[i-2][j-1]
                if ((p == 0) or ((p >= 20))):
                    moves.append(((i-2), j-1))
            # Up 2 right 1
            if ((-1 < (i-2) < 8) & (-1 < (j+1) < 8)):
                p = board.iloc[i-2][j+1]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i-2), j+1))
            # Up 1 right 2
            if ((-1 < (i-1) < 8) & (-1 < (j+2) < 8)):
                p = board.iloc[i-1][j+1]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i-1), j+2))
            # Up 1 left 2
            if ((-1 < (i-1) < 8) & (-1 < (j-2) < 8)):
                p = board.iloc[i-1][j-2]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i-1), j-2))

            # Down 2 left 1

            if ((0 <= (i+2) <= 7) & (0 <= (j-1) <= 7)):
                p = board.iloc[i+2][j-1]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i+2), j-1))
            # Down 2 right 1
            if ((-1 < (i+2) < 8) & (-1 < (j+1) < 8)):
                p = board.iloc[i+2][j+1]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i+2), j+1))
            # Down 1 right 2
            if ((-1 < (i+1) < 8) & (-1 < (j+2) < 8)):
                p = board.iloc[i+1][j+2]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i+1), j+2))
            # Down 1 left 2
            if ((-1 < (i+1) < 8) & (-1 < (j-2) < 8)):
                p = board.iloc[i+1][j-2]
                if ((p == 0) or (p >= 20)):
                    moves.append(((i+1), j-2))

        if self.color == 'b':
            # Up 2 left 1

            if ((-1 < (i-2) < 8) & (-1 < (j-1) < 8)):
                p = board.iloc[i-2][j-1]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i-2), j-1))
            # Up 2 right 1
            if ((-1 < (i-2) < 8) & (-1 < (j+1) < 8)):
                p = board.iloc[i-2][j+1]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i-2), j+1))
            # Up 1 right 2
            if ((-1 < (i-1) < 8) & (-1 < (j+2) < 8)):
                p = board.iloc[i-1][j+2]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i-1), j+2))
            # Up 1 left 2
            if ((-1 < (i-1) < 8) & (-1 < (j-2) < 8)):
                p = board.iloc[i-1][j-2]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i-1), j-2))

            # Down 2 left 1

            if ((0 <= (i+2) <= 7) & (0 <= (j-1) <= 7)):
                p = board.iloc[i+2][j-1]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i+2), j-1))
            # Down 2 right 1
            if ((-1 < (i+2) < 8) & (-1 < (j+1) < 8)):
                p = board.iloc[i+2][j+1]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i+2), j+1))
            # Down 1 right 2
            if ((-1 < (i+1) < 8) & (-1 < (j+2) < 8)):
                p = board.iloc[i+1][j+2]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i+1), j+2))
            # Down 1 left 2
            if ((-1 < (i+1) < 8) & (-1 < (j-2) < 8)):
                p = board.iloc[i+1][j-2]
                if ((p == 0) or (p <= 20)):
                    moves.append(((i+1), j-2))
        move_logs = []
        for move in moves:
            move_logs.append(
                [board.iloc[i][j], i, j, move[0], move[1], 0, 0])

        return (moves, move_logs)

    def generate_pawn_moves(self, board):
        i = self.row
        j = self.col
        moves = []

        if self.first:

            if self.color == 'w':

                if i == 6:
                    p = board.iloc[i-1][j]
                    if p == 0:
                        moves.append(((i-1), j))
                    p = board.iloc[i-2][j]
                    if p == 0:
                        moves.append(((i-2), j))

                elif i > 0:
                    p = board.iloc[i-1][j]
                    if p == 0:
                        moves.append(((i-1), j))
                # to the left
                if (j-1 >= 0):
                    p = board.iloc[i-1][j-1]
                    if (p >= 20):
                        moves.append(((i-1), (j-1)))
                # to the right
                if (j+1 <= 7):
                    p = board.iloc[i-1][j+1]
                    if (p >= 20):
                        moves.append(((i-1), (j+1)))

            if self.color == 'b':

                if i == 1:
                    p = board.iloc[i+1][j]
                    if p == 0:
                        moves.append(((i+1), j))
                    p = board.iloc[i+2][j]
                    if p == 0:
                        moves.append(((i+2), j))

                elif i < 7:
                    p = board.iloc[i+1][j]
                    if p == 0:
                        moves.append(((i+1), j))
                 # to the left
                if (j-1 >= 0):
                    p = board.iloc[i+1][j-1]
                    if ((p <= 20) & (p != 0)):
                        moves.append(((i+1), (j-1)))
                # to the right
                if (j+1 <= 7):
                    p = board.iloc[i+1][j+1]
                    if ((p <= 20) & (p != 0)):
                        moves.append(((i+1), (j+1)))
        move_logs = []
        for move in moves:
            if ((move[0] - i == 2) or (i - move[0] == 2)):
                move_logs.append(
                    [board.iloc[i][j], i, j, move[0], move[1], 2, 0])
            else:
                move_logs.append(
                    [board.iloc[i][j], i, j, move[0], move[1], 0, 0])
        # print(moves)
        # print(move_logs)
        return ((moves, move_logs))

    def generate_bishop_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        if self.color == 'w':
            # Diagonal Up Left
            for x in range(1, 8):
                if (((i-x) >= 0) & ((j-x) >= 0)):
                    p = board.iloc[i-x][j-x]
                    if p == 0:
                        moves.append(((i-x), (j-x)))
                    else:
                        if p >= 20:
                            moves.append(((i-x), (j-x)))
                            break
                        else:
                            break
                else:
                    break
            # Diagonal Up Right
            for x in range(1, 8):
                if (((i-x) >= 0) & ((j+x) <= 7)):
                    p = board.iloc[i-x][j+x]
                    if p == 0:
                        moves.append(((i-x), (j+x)))
                    else:
                        if p >= 20:
                            moves.append(((i-x), (j+x)))
                            break
                        else:
                            break
                else:
                    break
            # Diagonal Down Left
            for x in range(1, 8):
                if (((i+x) <= 7) & ((j-x) >= 0)):
                    p = board.iloc[i+x][j-x]
                    if p == 0:
                        moves.append(((i+x), (j-x)))
                    else:
                        if p >= 20:
                            moves.append(((i+x), (j-x)))
                            break
                        else:
                            break
                else:
                    break
            # Diagonal Down Right
            for x in range(1, 8):
                if (((i+x) <= 7) & ((j+x) <= 7)):
                    p = board.iloc[i+x][j+x]
                    if p == 0:
                        moves.append(((i+x), (j+x)))
                    else:
                        if p >= 20:
                            moves.append(((i+x), (j+x)))
                            break
                        else:
                            break
                else:
                    break

        elif self.color == 'b':
            # Diagonal Up Left
            for x in range(1, 8):
                if (((i-x) >= 0) & ((j-x) >= 0)):
                    p = board.iloc[i-x][j-x]
                    if p == 0:
                        moves.append(((i-x), (j-x)))
                    else:
                        if p <= 20:
                            moves.append(((i-x), (j-x)))
                            break
                        else:
                            break
                else:
                    break
            # Diagonal Up Right
            for x in range(1, 8):
                if (((i-x) >= 0) & ((j+x) <= 7)):
                    p = board.iloc[i-x][j+x]
                    if p == 0:
                        moves.append(((i-x), (j+x)))
                    else:
                        if p <= 20:
                            moves.append(((i-x), (j+x)))
                            break
                        else:
                            break
                else:
                    break
            # Diagonal Down Left
            for x in range(1, 8):
                if (((i+x) <= 7) & ((j-x) >= 0)):
                    p = board.iloc[i+x][j-x]
                    if p == 0:
                        moves.append(((i+x), (j-x)))
                    else:
                        if p <= 20:
                            moves.append(((i+x), (j-x)))
                            break
                        else:
                            break
                else:
                    break
            # Diagonal Down Right
            for x in range(1, 8):
                if (((i+x) <= 7) & ((j+x) <= 7)):
                    p = board.iloc[i+x][j+x]
                    if p == 0:
                        moves.append(((i+x), (j+x)))
                    else:
                        if p <= 20:
                            moves.append(((i+x), (j+x)))
                            break
                        else:
                            break
                else:
                    break
        move_logs = []
        for move in moves:
            move_logs.append(
                [board.iloc[i][j], i, j, move[0], move[1], 0, 0])

        return (moves, move_logs)

    def generate_rook_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        #print((i, j))

        if self.color == 'b':
            # Down
            for y in range(i+1, 8):
                p = board.iloc[y][j]
                if p == 0:
                    moves.append((y, j))
                else:
                    if p <= 19:
                        moves.append(((y), j))
                        break
                    else:
                        break
            # Left
            for x in range(j-1, -1, -1):
                p = board.iloc[i][x]
                if p == 0:
                    moves.append((i, x))
                else:
                    if p <= 19:
                        moves.append((i, x))
                        break
                    else:
                        break
            # Right
            for x in range(j+1, 8):
                p = board.iloc[i][x]
                if p == 0:
                    moves.append((i, x))
                else:
                    if p <= 19:
                        moves.append((i, x))
                        break
                    else:
                        break
            # Up

            for y in range(i-1, -1, -1):
                p = board.iloc[y][j]
                if p == 0:
                    moves.append((y, j))
                else:
                    if p <= 19:
                        moves.append((y, j))
                        break
                    else:
                        break
        elif self.color == 'w':
            # print(board)
            # Down
            for y in range(i+1, 8):
                p = board.iloc[y][j]
                if p == 0:
                    moves.append((y, j))
                else:
                    if p >= 19:
                        moves.append((y, j))
                        break
                    else:
                        break
            # Left
            for x in range(j-1, -1, -1):
                p = board.iloc[i][x]
                if p == 0:
                    moves.append((i, x))
                else:
                    if p >= 19:
                        moves.append((i, x))
                        break
                    else:
                        break
            # Right
            for x in range(j+1, 8):
                p = board.iloc[i][x]
                if p == 0:
                    moves.append((i, x))
                else:
                    if p >= 19:
                        moves.append((i, x))
                        break
                    else:
                        break
            # Up

            for y in range(i-1, -1, -1):
                p = board.iloc[y][j]
                if p == 0:
                    moves.append((y, j))
                else:
                    if p >= 19:
                        moves.append(((y), j))
                        break
                    else:
                        break
        move_logs = []
        for move in moves:
            move_logs.append(
                [board.iloc[i][j], i, j, move[0], move[1], 0, 0])

        return (moves, move_logs)

    def generate_pawn_enpassant_moves(self, board, turn_log):
        i = self.row
        j = self.col
        moves = []
        moves_log = []
        if (len(turn_log) >= 1):
            if self.color == 'w':
                if ((turn_log[-1][5] == 2) & (turn_log[-1][0] == 21)):
                    if ((turn_log[-1][3] == (i)) & (turn_log[-1][4] == (j-1))):
                        moves.append((i-1, j-1))
                    elif ((turn_log[-1][3] == (i)) & (turn_log[-1][4] == (j+1))):
                        moves.append((i-1, j+1))
            elif self.color == 'b':
                if ((turn_log[-1][5] == 2) & (turn_log[-1][0] == 11)):
                    if ((turn_log[-1][3] == (i)) & (turn_log[-1][4] == (j-1))):
                        moves.append((i+1, j-1))
                    elif ((turn_log[-1][3] == (i)) & (turn_log[-1][4] == (j+1))):
                        moves.append((i+1, j+1))
            for move in moves:
                moves_log.append(
                    [board.iloc[i][j], i, j, move[0], move[1], 3, 0])
        return (moves, moves_log)

    def generate_king_castle_moves(self, board, showboard, turn_log=None):
        i = self.row
        j = self.col
        moves = []
        moves_log = []
        opponent_checked_squares = []

        if self.color == 'w':
            for row in range(0, 8):
                for col in range(0, 8):
                    if ((board.iloc[row][col] >= 20) and (board.iloc[row][col] != 0)):
                        valid_moves = showboard[row][col].valid_moves(
                            board, showboard, turn_log, False)[0]
                        opponent_checked_squares.extend(valid_moves)

            if self.moved == False:
                # Castle King Side:
                if (board.iloc[7][7] == 12):
                    if (showboard[7][7].moved == False):
                        if((board.iloc[7][6] == 0) and ((board.iloc[7][5] == 0))):
                            if(((7, 5) not in opponent_checked_squares) and ((7, 6) not in opponent_checked_squares)):
                                moves.append((7, 6))
                                moves_log.append(
                                    [board.iloc[i][j], i, j, 7, 6, 4, 1])

              # Castle Queen Side:

                if (board.iloc[7][0] == 12):
                    if (showboard[7][0].moved == False):
                        if((board.iloc[7][1] == 0) and (board.iloc[7][2] == 0) and (board.iloc[7][3] == 0)):
                            if(((7, 1) not in opponent_checked_squares) and ((7, 2) not in opponent_checked_squares) and ((7, 3) not in opponent_checked_squares)):
                                moves.append((7, 2))
                                moves_log.append(
                                    [board.iloc[i][j], i, j, 7, 2, 4, 2])
        elif self.color == 'b':
            for row in range(0, 8):
                for col in range(0, 8):
                    if ((board.iloc[row][col] <= 20) and (board.iloc[row][col] != 0)):
                        valid_moves = showboard[row][col].valid_moves(
                            board, showboard, turn_log, False)[0]
                        opponent_checked_squares.extend(valid_moves)

            if self.moved == False:

                # Castle King Side:
                if (board.iloc[0][7] == 22):
                    if (showboard[0][7].moved == False):
                        if((board.iloc[0][6] == 0) and ((board.iloc[0][5] == 0))):
                            if(((0, 6) not in opponent_checked_squares) and ((0, 5) not in opponent_checked_squares)):
                                moves.append((0, 6))
                                moves_log.append(
                                    [board.iloc[i][j], i, j, 0, 6, 4, 1])

              # Castle Queen Side:

                if (board.iloc[0][0] == 22):
                    if (showboard[0][0].moved == False):
                        if((board.iloc[0][1] == 0) and (board.iloc[0][2] == 0) and (board.iloc[0][3] == 0)):
                            if(((0, 1) not in opponent_checked_squares) and ((0, 2) not in opponent_checked_squares) and ((0, 3) not in opponent_checked_squares)):
                                moves.append((0, 2))
                                moves_log.append(
                                    [board.iloc[i][j], i, j, 0, 2, 4, 2])
        return (moves, moves_log)

        pass

    def is_king_in_check(self, board, showboard, turn_log):

        checked_squared = []
        chessboarddf = board
        i = self.row
        j = self.col

        if (self.color == 'w'):

            for row in range(0, 8):
                for col in range(0, 8):

                    if ((chessboarddf.iloc[row][col] >= 20) and (chessboarddf.iloc[row][col] != 0)):
                        # print(chessboarddf.iloc[row][col])
                        valid_moves = showboard[row][col].valid_moves(
                            chessboarddf, showboard, turn_log, False)[0]
                        #print('piece valid moves: \n')
                        # print(valid_moves)
                        checked_squared.extend(valid_moves)
            # print('Here \n')
            # print(checked_squared)
            # print((i, j) in checked_squared)
            return ((i, j) in checked_squared)

        elif(self.color == 'b'):
            for row in range(0, chessboarddf.shape[0]):
                for col in range(0, chessboarddf.shape[1]):
                    if ((chessboarddf.iloc[row][col] <= 20) and (chessboarddf.iloc[row][col] != 0)):
                        valid_moves = showboard[row][col].valid_moves(
                            chessboarddf, showboard, turn_log, False)[0]
                        checked_squared.extend(valid_moves)
            # print(checked_squared)
            # print((i, j) in checked_squared)

            return ((i, j) in checked_squared)


class Bishop(Piece):
    img = 0

    def valid_moves(self, board, showboard=None, turn_log=None, run=True):
        moves = []
        moves_log = []
        generated_moves = self.generate_bishop_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])

        return moves, moves_log


class King(Piece):
    img = 1

    def __init__(self, row, col, id):
        super().__init__(row, col, id)
        self.moved = False
        self.checked = False

    def valid_moves(self, board, showboard=None, turn_log=None, run=True):
        moves = []
        moves_log = []
        generated_moves = self.generate_king_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])
        if (run):
            if (self.is_king_in_check(board, showboard, turn_log) == False):
                generated_moves = self.generate_king_castle_moves(
                    board, showboard)
                moves.extend(generated_moves[0])
                moves_log.extend(generated_moves[1])
        return moves, moves_log


class Knight(Piece):
    img = 2

    def valid_moves(self, board, showboard=None, turn_log=None, run=True):
        moves = []
        moves_log = []
        generated_moves = self.generate_knight_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])
        return moves, moves_log


class Pawn(Piece):
    img = 3

    def __init__(self, row, col, id):
        super().__init__(row, col, id)
        self.first = True
        self.queen = False
        self.en_passant = False

    def valid_moves(self, board, showboard=None, turn_log=None, run=True):
        moves = []
        moves_log = []
        generated_moves = self.generate_pawn_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])
        if (run):
            generated_moves = self.generate_pawn_enpassant_moves(
                board, turn_log)
            moves.extend(generated_moves[0])
            moves_log.extend(generated_moves[1])

        return moves, moves_log


class Queen(Piece):
    img = 4

    def valid_moves(self, board, showboard=None, turn_log=None, run=True):
        moves = []
        moves_log = []
        generated_moves = self.generate_bishop_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])
        generated_moves = self.generate_rook_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])
        return moves, moves_log


class Rook(Piece):
    img = 5

    def __init__(self, row, col, id):
        super().__init__(row, col, id)
        self.moved = False

    def valid_moves(self, board, showboard=None, turn_log=None, run=True):
        moves = []
        moves_log = []
        generated_moves = self.generate_rook_moves(board)
        moves.extend(generated_moves[0])
        moves_log.extend(generated_moves[1])
        # print(moves)

        return moves, moves_log
