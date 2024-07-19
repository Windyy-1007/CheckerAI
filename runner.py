# Main file

import sys
import math

# Board and pieces
intialPos = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
winner = 0

class Board:
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
    def endGame(self):
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
        return False

    def moveAvailable(self, turn):
        for i in range(8):
            for j in range(8):
                if turn == 1:
                    if self.board[i][j] == 1:
                        if i - 1 >= 0 and j - 1 >= 0 and self.board[i-1][j-1] == 0:
                            return True
                        if i - 1 >= 0 and j + 1 < 8 and self.board[i-1][j+1] == 0:
                            return True
                        if self.board[i][j] == 2:
                            if i + 1 < 8 and j - 1 >= 0 and self.board[i+1][j-1] == 0:
                                return True
                            if i + 1 < 8 and j + 1 < 8 and self.board[i+1][j+1] == 0:
                                return True
                if turn == -1:
                    if self.board[i][j] == -1:
                        if i + 1 < 8 and j - 1 >= 0 and self.board[i+1][j-1] == 0:
                            return True
                        if i + 1 < 8 and j + 1 < 8 and self.board[i+1][j+1] == 0:
                            return True
                        if self.board[i][j] == -2:
                            if i - 1 >= 0 and j - 1 >= 0 and self.board[i-1][j-1] == 0:
                                return True
                            if i - 1 >= 0 and j + 1 < 8 and self.board[i-1][j+1] == 0:
                                return True
 
    def utility(self):
        if not self.endGame():
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
        if (turn == 1 and self.board[x][y] == -1):
            return False
        if (turn == -1 and self.board[x][y] == 1):
            return False
        if turn == 1:
            if (direction == 'L'):
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] == 1):
                    return False
                if (self.board[x-1][y-1] == -1):
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
                if (self.board[x-1][y+1] == 1):
                    return False
                if (self.board[x-1][y+1] == -1):
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
                if (self.board[x+1][y-1] == -1):
                    return False
                if (self.board[x+1][y-1] == 1):
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
                if (self.board[x+1][y+1] == -1):
                    return False
                if (self.board[x+1][y+1] == 1):
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
                if (self.board[x+1][y-1] == -1):
                    return False
                if (self.board[x+1][y-1] == 1):
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
                if (self.board[x+1][y+1] == -1):
                    return False
                if (self.board[x+1][y+1] == 1):
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
                if (self.board[x-1][y-1] == 1):
                    return False
                if (self.board[x-1][y-1] == -1):
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
                if (self.board[x-1][y+1] == 1):
                    return False
                if (self.board[x-1][y+1] == -1):
                    if(x == 1 or y == 6):
                        return False
        return False
    
    def move(self, x, y, direction, turn):
        if (self.board[x][y] == 0):
            return False
        if (turn == 1 and self.board[x][y] == -1):
            return False
        if (turn == -1 and self.board[x][y] == 1):
            return False
        if turn == 1:
            if (direction == 'L'):
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] == 1):
                    return False
                if (self.board[x-1][y-1] == -1):
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
            if (direction == 'R'):
                if(y == 7 or x == 0):
                    return False
                if (self.board[x-1][y+1] == 1):
                    return False
                if (self.board[x-1][y+1] == -1):
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
            if (direction == '-L'):
                if(self.board[x][y] != 2):
                    return False
                if(y == 0 or x == 7):
                    return False
                if (self.board[x+1][y-1] == -1):
                    return False
                if (self.board[x+1][y-1] == 1):
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
                if (self.board[x+1][y+1] == -1):
                    return False
                if (self.board[x+1][y+1] == 1):
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
                if (self.board[x+1][y-1] == -1):
                    return False
                if (self.board[x+1][y-1] == 1):
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
            if (direction == 'R'):
                if(y == 7 or x == 7):
                    return False
                if (self.board[x+1][y+1] == -1):
                    return False
                if (self.board[x+1][y+1] == 1):
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
            if (direction == '-L'):
                if(self.board[x][y] != -2):
                    return False
                if(y == 0 or x == 0):
                    return False
                if (self.board[x-1][y-1] == 1):
                    return False
                if (self.board[x-1][y-1] == -1):
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
                if (self.board[x-1][y+1] == 1):
                    return False
                if (self.board[x-1][y+1] == -1):
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

#AI

def min_value(str, depth = 10):
    tempBoard = Board(str)
    backupBoard = Board(str)
    if depth == 0:
        return evaluate(str)
    if tempBoard.endGame():
        return tempBoard.utility()
    v = math.inf
    for i in range(8):
        for j in range(8):
            if tempBoard.board[i][j] == 0:
                continue
            if tempBoard.moveAllowed(i, j, 'L', -1):
                tempBoard.move(i, j, 'L', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
            if tempBoard.moveAllowed(i, j, 'R', -1):
                tempBoard.move(i, j, 'R', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
            if tempBoard.moveAllowed(i, j, '-L', -1):
                tempBoard.move(i, j, '-L', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
            if tempBoard.moveAllowed(i, j, '-R', -1):
                tempBoard.move(i, j, '-R', -1)
                v = min(v, max_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
    return v

def max_value(str, depth = 10):
    tempBoard = Board(str)
    backupBoard = Board(str)
    if depth == 0:
        return evaluate(str)
    if tempBoard.endGame():
        return tempBoard.utility()
    v = -math.inf
    for i in range(8):
        for j in range(8):
            if tempBoard.board[i][j] == 0:
                continue
            if tempBoard.moveAllowed(i, j, 'L', 1):
                tempBoard.move(i, j, 'L', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
            if tempBoard.moveAllowed(i, j, 'R', 1):
                tempBoard.move(i, j, 'R', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
            if tempBoard.moveAllowed(i, j, '-L', 1):
                tempBoard.move(i, j, '-L', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
            if tempBoard.moveAllowed(i, j, '-R', 1):
                tempBoard.move(i, j, '-R', 1)
                v = max(v, min_value(tempBoard.getString(), depth - 1))
                tempBoard.board = backupBoard.board
    return v
                    
def minimax(str, depth, turn):
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
                    tempBoard.board = backupBoard.board
                if tempBoard.moveAllowed(i, j, 'R', 1):
                    tempBoard.move(i, j, 'R', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = backupBoard.board
                if tempBoard.moveAllowed(i, j, '-L', 1):
                    tempBoard.move(i, j, '-L', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = backupBoard.board
                if tempBoard.moveAllowed(i, j, '-R', 1):
                    tempBoard.move(i, j, '-R', 1)
                    if(min_value(tempBoard.getString(), depth - 1) > v):
                        v = min_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = backupBoard.board
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
                    tempBoard.board = backupBoard.board
                if tempBoard.moveAllowed(i, j, 'R', -1):
                    tempBoard.move(i, j, 'R', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = backupBoard.board
                if tempBoard.moveAllowed(i, j, '-L', -1):
                    tempBoard.move(i, j, '-L', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = backupBoard.board
                if tempBoard.moveAllowed(i, j, '-R', -1):
                    tempBoard.move(i, j, '-R', -1)
                    if(max_value(tempBoard.getString(), depth - 1) < v):
                        v = max_value(tempBoard.getString(), depth - 1)
                        optimalMove = tempBoard.getString()
                    tempBoard.board = backupBoard.board
    print ('v' ,v)
    return optimalMove

def evaluate(string):
    board = Board(string)
    scoreW = 0.000
    scoreB = 0.000
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]
    return (scoreW) / (scoreB + scoreW)
            
evaluate('0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0')

# play a game
def playGame():
    board = Board(intialPos)
    board.printBoard()
    turn = 1
    while not board.endGame():
        print("Player ", turn, " turn")
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        direction = input("Enter direction: ")
        if board.move(x, y, direction, turn):
            board.printBoard()
            turn = -turn
        else:
            print("Invalid move")
    if winner == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")

def playGameBot():
    board = Board(intialPos)
    board.printBoard()
    turn = 1
    while not board.endGame():
        print("Player ", turn, " turn")
        if turn == 1:
            x = int(input("Enter x coordinate: "))
            y = int(input("Enter y coordinate: "))
            direction = input("Enter direction: ")
            if board.move(x, y, direction, turn):
                board.printBoard()
                turn = -turn
            else:
                print("Invalid move")
        else:
            curPos = board.getString()
            suggestedPos = minimax(curPos, 5, -1)
            board.editBoard(suggestedPos)
            board.printBoard()
            turn = -turn
    if winner == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")

def main():
    playGameBot()

if __name__=="__main__": 
    main()