import copy
import board as bd
import math
import random

def evaluate(string):
    global evalCalls
    evalCalls += 1
    board = bd.Board(string)
    if board.endGame(1):
        return -1
    if board.endGame(-1):
        return 1
    scoreW = 0.000
    scoreB = 0.000
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
                # Bonus for being in the center
                if (i == 3 or i == 4) and (j == 3 or j == 4):
                    scoreW += 0.5
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]
                # Bonus for being in the center
                if (i == 3 or i == 4) and (j == 3 or j == 4):
                    scoreB += 0.5

    return round(2*((scoreW) / (scoreB + scoreW)) - 1, 5)

def min_value(str, depth = 10, currentV=math.inf):
    tempBoard = bd.Board(str)
    backupBoard = bd.Board(str)
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
    tempBoard = bd.Board(str)
    backupBoard = bd.Board(str)
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
    tempBoard = bd.Board(str)
    backupBoard = bd.Board(str)
    optimalMoves = []
    if turn == 1:
        v = -math.inf
        for i in range(8):
            for j in range(8):
                if tempBoard.board[i][j] == 0:
                    continue
                if tempBoard.moveAllowed(i, j, 'L', 1):
                    tempBoard.move(i, j, 'L', 1)
                    move_value = min_value(tempBoard.getString(), depth - 1)
                    if move_value > v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                if tempBoard.moveAllowed(i, j, 'R', 1):
                    tempBoard.move(i, j, 'R', 1)
                    move_value = min_value(tempBoard.getString(), depth - 1)
                    if move_value > v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                if tempBoard.moveAllowed(i, j, '-L', 1):
                    tempBoard.move(i, j, '-L', 1)
                    move_value = min_value(tempBoard.getString(), depth - 1)
                    if move_value > v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                if tempBoard.moveAllowed(i, j, '-R', 1):
                    tempBoard.move(i, j, '-R', 1)
                    move_value = min_value(tempBoard.getString(), depth - 1)
                    if move_value > v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
    else:
        v = math.inf
        for i in range(8):
            for j in range(8):
                if tempBoard.board[i][j] == 0:
                    continue
                
                if tempBoard.moveAllowed(i, j, 'L', -1):
                    tempBoard.move(i, j, 'L', -1)
                    move_value = max_value(tempBoard.getString(), depth - 1)
                    if move_value < v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                        print(i, j, 'L', -1, v)
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                    
                if tempBoard.moveAllowed(i, j, 'R', -1):
                    tempBoard.move(i, j, 'R', -1)
                    move_value = max_value(tempBoard.getString(), depth - 1)
                    if move_value < v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                        print(i, j, 'R', -1, v)
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                    
                if tempBoard.moveAllowed(i, j, '-L', -1):
                    tempBoard.move(i, j, '-L', -1)
                    move_value = max_value(tempBoard.getString(), depth - 1)
                    if move_value < v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                        print(i, j, '-L', -1, v)
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
                    
                if tempBoard.moveAllowed(i, j, '-R', -1):
                    tempBoard.move(i, j, '-R', -1)
                    move_value = max_value(tempBoard.getString(), depth - 1)
                    if move_value < v:
                        v = move_value
                        optimalMoves = [tempBoard.getString()]
                        print(i, j, '-R', -1, v)
                    elif move_value == v:
                        optimalMoves.append(tempBoard.getString())
                    tempBoard.board = copy.deepcopy(backupBoard.board)
    print ('Current evaluation: ' ,v)
    return random.choice(optimalMoves) if optimalMoves else 'N'