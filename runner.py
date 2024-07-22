# Main file

import sys
import math
import copy
import string
import time
import os

# Board and pieces
intialPos = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
customPos = '0000000000b00000000b0000000000000w0w0w00000000000000000000000000' 
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
        for i in range(63):
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
            winner = 1
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
        if self.moveAvailable(1):
            return 1
        if self.moveAvailable(-1):
            return -1
        
        sum = 0
        for i in range(8):
            for j in range(8):
                sum += self.board[i][j]
        if sum > 0:
            return 1
        if sum < 0:
            return -1
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
                if (self.board[x-1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
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
                if (self.board[x-1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    return True
            if (direction == '-L'):
                if(self.board[x][y] != 2):
                    return False
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
                if (self.board[x+1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    return True
            if (direction == '-R'):
                if(self.board[x][y] != 2):
                    return False
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
                if (self.board[x+1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
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
                if (self.board[x+1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
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
                if (self.board[x+1][y+1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    return True
            if (direction == '-L'):
                if(self.board[x][y] != -2):
                    return False
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
                if (self.board[x-1][y-1] == 0):
                    if(self.availableCapture(turn)):
                        return False
                    return True
            if (direction == '-R'):
                if(self.board[x][y] != -2):
                    return False
                if(y == 7 or x == 0):
                    return False
                if (self.board[x-1][y+1] > 0):
                    return False
                if (self.board[x-1][y+1] < 0):
                    if(x == 1 or y == 6):
                        return False
        return False
    
    def move(self, x, y, direction, turn):
        lastBoard = copy.deepcopy(self.board)
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

    def undoMove(self):
        self.board = copy.deepcopy(self.lastBoard)
        return True
#AI
def learning(str, evaluation, unity=0):
    with open('evaluations.txt', 'a') as file:
        file.write(f"{str},{evaluation}\n")
    pass


    
def usingExperience():
    # Load the file
    # When the bot is playing, if the string is in the file, use the evaluation
    # If the string is not in the file, use the minimax algorithm to evaluate the string
    # Save the string and evaluation to the file
    pass

def min_value(str, depth = 10, currentV=math.inf):
    tempBoard = Board(str)
    backupBoard = Board(str)
    if depth == 0:
        return evaluate(str)
    if tempBoard.endGame(-1):
        return tempBoard.utility(-1)
    v = math.inf
    for i in range(8):
        for j in range(8):
            if tempBoard.board[i][j] == 0:
                continue
            if tempBoard.moveAllowed(i, j, 'L', -1):
                tempBoard.move(i, j, 'L', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
            if tempBoard.moveAllowed(i, j, 'R', -1):
                tempBoard.move(i, j, 'R', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
            if tempBoard.moveAllowed(i, j, '-L', -1):
                tempBoard.move(i, j, '-L', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
            if tempBoard.moveAllowed(i, j, '-R', -1):
                tempBoard.move(i, j, '-R', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
    return v

def max_value(str, depth = 10, currentV=-math.inf):
    tempBoard = Board(str)
    backupBoard = Board(str)
    if depth == 0:
        return evaluate(str)
    if tempBoard.endGame(1):
        return tempBoard.utility(1)
    v = -math.inf
    for i in range(8):
        for j in range(8):
            if tempBoard.board[i][j] == 0:
                continue
            if tempBoard.moveAllowed(i, j, 'L', 1):
                tempBoard.move(i, j, 'L', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1,))
                tempBoard.board = copy.deepcopy(backupBoard.board)
            if tempBoard.moveAllowed(i, j, 'R', 1):
                tempBoard.move(i, j, 'R', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
            if tempBoard.moveAllowed(i, j, '-L', 1):
                tempBoard.move(i, j, '-L', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
            if tempBoard.moveAllowed(i, j, '-R', 1):
                tempBoard.move(i, j, '-R', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = copy.deepcopy(backupBoard.board)
    return v
                    
def minimax(str, depth, turn):
    print ('Depth= ', depth)
    tempBoard = Board(str)
    backupBoard = Board(str)
    optimalMove = 'N'
    if turn == 1:
        v = -math.inf
        for i in range(8):
            for j in range(8):
                if tempBoard.board[i][j] == 0:
                    continue
                if tempBoard.moveAllowed(i, j, 'L', 1):
                    tempBoard.move(i, j, 'L', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                if tempBoard.moveAllowed(i, j, 'R', 1):
                    tempBoard.move(i, j, 'R', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                if tempBoard.moveAllowed(i, j, '-L', 1):
                    tempBoard.move(i, j, '-L', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                if tempBoard.moveAllowed(i, j, '-R', 1):
                    tempBoard.move(i, j, '-R', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = copy.deepcopy(backupBoard.board)
    else:
        v = math.inf
        for i in range(8):
            for j in range(8):
                if tempBoard.board[i][j] == 0:
                    continue
                
                if tempBoard.moveAllowed(i, j, 'L', -1):
                    tempBoard.move(i, j, 'L', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                        print(i, j, 'L', -1, v)
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                    
                if tempBoard.moveAllowed(i, j, 'R', -1):
                    tempBoard.move(i, j, 'R', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                        print(i, j, 'R', -1, v)
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                    
                if tempBoard.moveAllowed(i, j, '-L', -1):
                    tempBoard.move(i, j, '-L', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                        print(i, j, '-L', -1, v)
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                    
                if tempBoard.moveAllowed(i, j, '-R', -1):
                    tempBoard.move(i, j, '-R', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                        print(i, j, '-R', -1, v)
                    tempBoard.board = copy.deepcopy(backupBoard.board)
    print ('Current evaluation: ' ,v)
    return optimalMove

def tuned_minimax(str, depth, alpha, beta, turn):
    tempBoard = Board(str)
    optimalMove = 'N'
    
    if depth == 0 or tempBoard.endGame(turn):
        return evaluate(str), optimalMove
    
    if turn == 1:
        maxEval = -math.inf
        for i in range(8):
            for j in range(8):
                for d in ['L', 'R', '-L', '-R']:
                    if tempBoard.moveAllowed(i, j, d, 1):
                        tempBoard.move(i, j, d, 1)
                        eval, _ = tuned_minimax(tempBoard.getString(), depth - 1, alpha, beta, -1)
                        if eval > maxEval:
                            maxEval = eval
                            optimalMove = tempBoard.getString()
                        tempBoard.undoMove()
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return maxEval, optimalMove  
    else:
        minEval = math.inf
        for i in range(8):
            for j in range(8):
                for d in ['L', 'R', '-L', '-R']:
                    if tempBoard.moveAllowed(i, j, d, -1):
                        tempBoard.move(i, j, d, -1)
                        eval, _ = tuned_minimax(tempBoard.getString(), depth - 1, alpha, beta, 1)
                        if eval < minEval:
                            minEval = eval
                            optimalMove = tempBoard.getString()
                            print('Depth layer: ', depth, 'Move: ', i, j, d, 'Evaluation: ', eval)
                        tempBoard.undoMove()
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        print('Depth layer: ', depth, 'Evaluation: ', minEval, 'Move: ', optimalMove)
        return minEval, optimalMove                   

def evaluate(string):
    global evalCalls
    evalCalls += 1
    board = Board(string)
    scoreW = 0.000
    scoreB = 0.000
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]
    return (2*round((scoreW) / (scoreB + scoreW),2) - 1)

def botPlay(str = 'A', difficulty=5, turn=1):
    num_pieces = 64 - str.count('0')
    endGameWeigth = 0.025
    depth = math.floor(difficulty / (endGameWeigth * num_pieces + 0.4))
    print ('Depth (bp): ', depth)
    eval, mstr = tuned_minimax(str, depth, -math.inf, math.inf, turn)
    print ('Number of evaluations: ', evalCalls)
    print ('Evaluation: ', eval)
    return mstr
    
            
# play a game
def playGame():
    board = Board(intialPos)
    board.printBoard()
    turn = 1
    while not board.endGame(turn):
        print("Player ", turn, " turn")
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        direction = input("Enter direction: ")
        if board.move(x, y, direction, turn):
            board.printBoard()
            turn = -turn
        else:
            print("Invalid move")
    if board.utility(turn) == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")

def playGameBot():
    board = Board(intialPos)
    board.betterPrintBoard()
    turn = 1
    while not board.endGame(turn):
        print("Player ", turn, " turn")
        if turn == 1:
            x = int(input("Enter x coordinate: "))
            y = int(input("Enter y coordinate: "))
            direction = input("Enter direction: ")
            if board.move(x, y, direction, turn):
                board.betterPrintBoard()
                turn = -turn
            else:
                print("Invalid move")
        else:
            timeStart = time.time()
            curPos = board.getString()
            suggestedPos = botPlay(curPos, 10, turn)
            timeEnd = time.time()
            print('Time to evaluate: ', timeEnd - timeStart)
            print('Number of evaluations: ', evalCalls)
            board.editBoard(suggestedPos)
            board.betterPrintBoard()
            turn = -turn
    if board.utility(turn) == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")

def twoBotGame():
    board = Board(intialPos)
    board.betterPrintBoard()
    turn = 1
    while not board.endGame(turn):
        print("Player ", turn, " turn")
        timeStart = time.time()
        curPos = board.getString()
        suggestedPos = botPlay(curPos, 29, turn)
        timeEnd = time.time()
        print('Time to evaluate: ', timeEnd - timeStart)
        print('Number of evaluations: ', evalCalls)
        board.editBoard(suggestedPos)
        learning(suggestedPos, evaluate(suggestedPos), 0)
        board.betterPrintBoard()
        turn = -turn
    if board.utility(turn) == 1:
        print("Player 1 wins")
        
    else:
        print("Player 2 wins")

def main():
    twoBotGame()

if __name__=="__main__": 
    main()
    