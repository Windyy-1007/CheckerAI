import runner
import math

def min_value(str, depth):
    tempBoard = runner.Board(str)
    backupBoard = runner.Board(str)
    if depth == 0:
        print (evaluate(str))
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

def max_value(str, depth):
    tempBoard = runner.Board(str)
    backupBoard = runner.Board(str)
    if depth == 0:
        print (evaluate(str))
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
    tempBoard = runner.Board(str)
    backupBoard = runner.Board(str)
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
    print (v)
    print ('\n')
    return optimalMove

def evaluate(string):
    board = runner.Board(string)
    scoreW = 0.000
    scoreB = 0.000
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
            elif board.board[i][j] < 0:
                scoreB += board.board[i][j]
    print (scoreW / (scoreB + scoreW))
    return (scoreW) / (scoreB + scoreW)
            
evaluate('0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0')