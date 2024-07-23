# Main file

import sys
import math
import copy
import string
import time
import os

# Board and pieces
intialPos = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
customPos = '0b0b0b0bb0b0b0b00b0b0b000000000000000000w0w0w0w00w0w0w0ww0w0w0w0' 
evalCalls = 0

class Board:
    lastBoard = [[0 for i in range(8)] for j in range(8)]
    def __init__(self, str):
        self.board = [[0 for i in range(8)] for j in range(8)]
        for i in range(63):
            if str[i] == 'N':
                break
            row = i // 8
            col = i % 8
            if str[i] == '0':
                continue
            elif str[i] == 'w':
                self.board[row][col] = 1
            elif str[i] == 'b':
                self.board[row][col] = -1
            elif str[i] == 'W':
                self.board[row][col] = 2
            elif str[i] == 'B':
                self.board[row][col] = -2
            else:
                print("Invalid input")
                break
            
    def __del__(self):
        pass
    
    def updateValue(self, x, y, value):
        self.board[x][y] = value
        
    def getValue(self, x, y):
        return self.board[x][y]
    
    def getBoard(self):
        return self.board
    
    def getString(self):
        str = ''
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    str += '0'
                elif self.board[i][j] == 1:
                    str += 'w'
                elif self.board[i][j] == -1:
                    str += 'b'
                elif self.board[i][j] == 2:
                    str += 'W'
                elif self.board[i][j] == -2:
                    str += 'B'
                else:
                    print("Invalid input")
        return str
    
    def printBoard(self):
        #Print 8x8 grid
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] >= 0):
                    print(self.board[i][j], end = '   ')
                else:
                    print(self.board[i][j], end = '  ')
            print()
    
    def editBoard(self, str):
        for i in range(64):
            if str[i] == 'N':
                break
            row = i // 8
            col = i % 8
            if str[i] == '0':
                self.board[row][col] = 0
            elif str[i] == 'w':
                self.board[row][col] = 1
            elif str[i] == 'b':
                self.board[row][col] = -1
            elif str[i] == 'W':
                self.board[row][col] = 2
            elif str[i] == 'B':
                self.board[row][col] = -2
            else:
                print("Invalid input")
                break
    
    #Game Logic
    def endGame(self, turn):
        sum = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] > 0):
                    sum += 1
        if sum == 0:
            winner = -1
            return True
        sum = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] < 0):
                    sum += 1
        if sum == 0:
            return True
        
        if not self.moveAvailable(turn):
            return True
        
        
        
        return False

    def moveAvailable(self, turn):
        for i in range(8):
            for j in range(8):
                if turn == 1:
                    if self.board[i][j] > 0:
                        if self.moveAllowed(i, j, 'L', turn):
                            return True
                        if self.moveAllowed(i, j, 'R', turn):
                            return True
                        if self.moveAllowed(i, j, '-L', turn):
                            return True
                        if self.moveAllowed(i, j, '-R', turn):
                            return True
                if turn == -1:
                    if self.board[i][j] < 0:
                        if self.moveAllowed(i, j, 'L', turn):
                            return True
                        if self.moveAllowed(i, j, 'R', turn):
                            return True
                        if self.moveAllowed(i, j, '-L', turn):
                            return True
                        if self.moveAllowed(i, j, '-R', turn):
                            return True
        return False
 
    def utility(self, turn):
        if not self.endGame(turn):
            return 0
        if not self.moveAvailable(1):
            return -1
        if not self.moveAvailable(-1):
            return 1
        
        countWhite = 0
        countBlack = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] > 0:
                    countWhite += 1
                if self.board[i][j] < 0:
                    countBlack += 1
        if countWhite == 0:
            return -1
        if countBlack == 0:
            return 1
        
        return 0
    
    def availableCapture(self, turn):
        if turn == 1:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 1:
                        if i - 2 >= 0 and j - 2 >= 0 and self.board[i-1][j-1] == -1 and self.board[i-2][j-2] == 0:
                            return True
                        if i - 2 >= 0 and j + 2 < 8 and self.board[i-1][j+1] == -1 and self.board[i-2][j+2] == 0:
                            return True
                        if i - 2 >= 0 and j - 2 >= 0 and self.board[i-1][j-1] == -2 and self.board[i-2][j-2] == 0:
                            return True
                        if i - 2 >= 0 and j + 2 < 8 and self.board[i-1][j+1] == -2 and self.board[i-2][j+2] == 0:
                            return True
        if turn == -1:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == -1:
                        if i + 2 < 8 and j - 2 >= 0 and self.board[i+1][j-1] == 1 and self.board[i+2][j-2] == 0:
                            return True
                        if i + 2 < 8 and j + 2 < 8 and self.board[i+1][j+1] == 1 and self.board[i+2][j+2] == 0:
                            return True
                        if i + 2 < 8 and j - 2 >= 0 and self.board[i+1][j-1] == 2 and self.board[i+2][j-2] == 0:
                            return True
                        if i + 2 < 8 and j + 2 < 8 and self.board[i+1][j+1] == 2 and self.board[i+2][j+2] == 0:
                            return True
    
    def moveAllowed(self, x, y, direction, turn):
        if (self.board[x][y] == 0):
            return False
        if (turn == 1 and self.board[x][y] < 0):
            return False
        if (turn == -1 and self.board[x][y] > 0):
            return False
        if turn == 1:
            if (direction == 'L'):
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] > 0):
                    return False
                if (self.board[x-1][y-1] < 0):
                    if(x == 1 or y == 1):
                        return False
                    if(self.board[x-2][y-2] != 0):
                        return False
                    return True
                if (self.board[x-1][y-1] == 0 and not self.availableCapture(turn)):
                    return True
            if (direction == 'R'):
                if(y == 7 or x == 0):
                    return False
                if (self.board[x-1][y+1] > 0):
                    return False
                if (self.board[x-1][y+1] < 0):
                    if(x == 1 or y == 6):
                        return False
                    if(self.board[x-2][y+2] != 0):
                        return False
                    return True
                if (self.board[x-1][y+1] == 0 and not self.availableCapture(turn)):
                    return True
            if (direction == '-L'):
                if(self.board[x][y] != 2):
                    return False
                if(y == 0 or x == 7):
                    return False
                if (self.board[x+1][y-1] > 0):
                    return False
                if (self.board[x+1][y-1] < 0):
                    if(x == 6 or y == 1):
                        return False
                    if(self.board[x+2][y-2] != 0):
                        return False
                    return True
                if (self.board[x+1][y-1] == 0 and not self.availableCapture(turn)):
                    return True
            if (direction == '-R'):
                if(self.board[x][y] != 2):
                    return False
                if(y == 7 or x == 7):
                    return False
                if (self.board[x+1][y+1] > 0):
                    return False
                if (self.board[x+1][y+1] < 0):
                    if(x == 6 or y == 6):
                        return False
                    if(self.board[x+2][y+2] != 0):
                        return False
                    return True
                if (self.board[x+1][y+1] == 0 and not self.availableCapture(turn)):
                    return True
        if turn == -1:
            if (direction == 'L'):
                if(y == 0 or x == 7):
                    return False
                if (self.board[x+1][y-1] < 0):
                    return False
                if (self.board[x+1][y-1] > 0):
                    if(x == 6 or y == 1):
                        return False
                    if(self.board[x+2][y-2] != 0):
                        return False
                    return True
                if (self.board[x+1][y-1] == 0 and not self.availableCapture(turn)):
                    return True
            if (direction == 'R'):
                if(y == 7 or x == 7):
                    return False
                if (self.board[x+1][y+1] < 0):
                    return False
                if (self.board[x+1][y+1] > 0):
                    if(x == 6 or y == 6):
                        return False
                    if(self.board[x+2][y+2] != 0):
                        return False
                    return True
                if (self.board[x+1][y+1] == 0 and not self.availableCapture(turn)):
                    return True
            if (direction == '-L'):
                if(self.board[x][y] != -2):
                    return False
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] < 0):
                    return False
                if (self.board[x-1][y-1] > 0):
                    if(x == 1 or y == 1):
                        return False
                    if(self.board[x-2][y-2] != 0):
                        return False
                    return True
                if (self.board[x-1][y-1] == 0 and not self.availableCapture(turn)):
                    return True
            if (direction == '-R'):
                if(self.board[x][y] != -2):
                    return False
                if(y == 7 or x == 0):
                    return False
                if (self.board[x-1][y+1] < 0):
                    return False
                if (self.board[x-1][y+1] > 0):
                    if(x == 1 or y == 6):
                        return False
                    if(self.board[x-2][y+2] != 0):
                        return False
                    return True
                if (self.board[x-1][y+1] == 0 and not self.availableCapture(turn)):
                    return True
        return False
    
    def move(self, x, y, direction, turn):
        if (self.board[x][y] == 0):
            return False
        if (turn == 1 and self.board[x][y] < 0):
            return False
        if (turn == -1 and self.board[x][y] > 0):
            return False
        if turn == 1:
            if (direction == 'L'):
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] > 0):
                    return False
                if (self.board[x-1][y-1] < 0):
                    if(x == 1 or y == 1):
                        return False
                    if(self.board[x-2][y-2] != 0):
                        return False
                    self.board[x-2][y-2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x-1][y-1] = 0
                    self.promotion()
                    # Capture multiple piece
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x-2, y-2, i, turn):
                                return True
                    return True
                if (self.board[x-1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x-1][y-1] = self.board[x][y]
                    self.board[x][y] = 0
                    self.promotion()
                    return True
            if (direction == 'R'):
                if(y == 7 or x == 0):
                    return False
                if (self.board[x-1][y+1] > 0):
                    return False
                if (self.board[x-1][y+1] < 0):
                    if(x == 1 or y == 6):
                        return False
                    if(self.board[x-2][y+2] != 0):
                        return False
                    self.board[x-2][y+2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x-1][y+1] = 0
                    self.promotion()
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x-2, y+2, i, turn):
                                return True
                    return True
                if (self.board[x-1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x-1][y+1] = self.board[x][y]
                    self.board[x][y] = 0
                    self.promotion()
                    return True
            if (direction == '-L'):
                if(self.board[x][y] != 2):
                    return False
                if(y == 0 or x == 7):
                    return False
                if (self.board[x+1][y-1] > 0):
                    return False
                if (self.board[x+1][y-1] < 0):
                    if(x == 6 or y == 1):
                        return False
                    if(self.board[x+2][y-2] != 0):
                        return False
                    self.board[x+2][y-2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x+1][y-1] = 0
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x+2, y-2, i, turn):
                                return True
                    return True
                if (self.board[x+1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x+1][y-1] = self.board[x][y]
                    self.board[x][y] = 0
                    return True
            if (direction == '-R'):
                if(self.board[x][y] != 2):
                    return False
                if(y == 7 or x == 7):
                    return False
                if (self.board[x+1][y+1] > 0):
                    return False
                if (self.board[x+1][y+1] < 0):
                    if(x == 6 or y == 6):
                        return False
                    if(self.board[x+2][y+2] != 0):
                        return False
                    self.board[x+2][y+2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x+1][y+1] = 0
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x+2, y+2, i, turn):
                                return True
                    return True
                if (self.board[x+1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x+1][y+1] = self.board[x][y]
                    self.board[x][y] = 0
                    return True                
                
        if turn == -1:
            if (direction == 'L'):
                if(y == 0 or x == 7):
                    return False
                if (self.board[x+1][y-1] < 0):
                    return False
                if (self.board[x+1][y-1] > 0):
                    if(x == 6 or y == 1):
                        return False
                    if(self.board[x+2][y-2] != 0):
                        return False
                    self.board[x+2][y-2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x+1][y-1] = 0
                    self.promotion()
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x+2, y-2, i, turn):
                                return True
                    return True
                if (self.board[x+1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x+1][y-1] = self.board[x][y]
                    self.board[x][y] = 0
                    self.promotion()
                    return True
            if (direction == 'R'):
                if(y == 7 or x == 7):
                    return False
                if (self.board[x+1][y+1] < 0):
                    return False
                if (self.board[x+1][y+1] > 0):
                    if(x == 6 or y == 6):
                        return False
                    if(self.board[x+2][y+2] != 0):
                        return False
                    self.board[x+2][y+2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x+1][y+1] = 0
                    self.promotion()
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x+2, y+2, i, turn):
                                return True
                    return True
                if (self.board[x+1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x+1][y+1] = self.board[x][y]
                    self.board[x][y] = 0
                    self.promotion()
                    return True
            if (direction == '-L'):
                if(self.board[x][y] != -2):
                    return False
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] < 0):
                    return False
                if (self.board[x-1][y-1] > 0):
                    if(x == 1 or y == 1):
                        return False
                    if(self.board[x-2][y-2] != 0):
                        return False
                    self.board[x-2][y-2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x-1][y-1] = 0
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x-2, y-2, i, turn):
                                return True
                    return True
                if (self.board[x-1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x-1][y-1] = self.board[x][y]
                    self.board[x][y] = 0
                    return True
            if (direction == '-R'):
                if(self.board[x][y] != -2):
                    return False
                if(y == 7 or x == 0):
                    return False
                if (self.board[x-1][y+1] < 0):
                    return False
                if (self.board[x-1][y+1] > 0):
                    if(x == 1 or y == 6):
                        return False
                    if(self.board[x-2][y+2] != 0):
                        return False
                    self.board[x-2][y+2] = self.board[x][y]
                    self.board[x][y] = 0
                    self.board[x-1][y+1] = 0
                    if(self.availableCapture(turn)):
                        for i in ['L', 'R', '-L', '-R']:
                            if self.move(x-2, y+2, i, turn):
                                return True
                    return True
                if (self.board[x-1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    self.board[x-1][y+1] = self.board[x][y]
                    self.board[x][y] = 0
                    return True
        return False

    def promotion(self):
        for i in range(8):
            if self.board[0][i] == 1:
                self.board[0][i] = 2
            if self.board[7][i] == -1:
                self.board[7][i] = -2
        return

    def betterPrintBoard(self):
        print('  0 1 2 3 4 5 6 7')
        for i in range(8):
            print(i, end=' ')
            for j in range(8):
                if (self.board[i][j] == 0):
                    print('.', end = ' ')
                
                elif(self.board[i][j] > 0):
                    print(self.board[i][j], end = ' ')
                else:
                    print(self.board[i][j], end = '')
            print()

    def listOfSquares(self, turn):
        # Assign 0 0 as 0 to 7 7 as 63.
        # Return list of square numbers that are occupied by the player
        moveList = []
        for i in range(8):
            for j in range(8):
                if turn == 1:
                    if self.board[i][j] > 0:
                        moveList.append(i*8 + j)
                if turn == -1:
                    if self.board[i][j] < 0:
                        moveList.append(i*8 + j)
    

