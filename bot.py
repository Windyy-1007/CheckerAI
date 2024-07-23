    
import board as bd
import math
import copy

evalCalls = 0

def usingExperience():
    # Load the file
    # When the bot is playing, if the string is in the file, use the evaluation
    # If the string is not in the file, use the minimax algorithm to evaluate the string
    # Save the string and evaluation to the file
    pass

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
    tempBoard = bd.Board(str)
    originalBoard = str
    optimalMove = ''
    
    if depth == 0 or tempBoard.endGame(turn):
        return evaluate(str), optimalMove
    
    if turn == 1:
        maxEval = -99
        for sqvalue in [1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30, 33, 35, 37, 39, 40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]:
            i = sqvalue // 8
            j = sqvalue % 8
            for d in ['L', 'R', '-L', '-R']:
                if tempBoard.moveAllowed(i, j, d, 1):
                    tempBoard.move(i, j, d, 1)
                    eval, _ = tuned_minimax(tempBoard.getString(), depth - 1, alpha, beta, -1)
                    if eval > maxEval:
                        maxEval = eval
                        optimalMove = tempBoard.getString()
                    tempBoard.editBoard(originalBoard)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return maxEval, optimalMove  
    else:
        minEval = 99
        for sqvalue in [1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 21, 23, 24, 26, 28, 30, 33, 35, 37, 39, 40, 42, 44, 46, 49, 51, 53, 55, 56, 58, 60, 62]:
            i = sqvalue // 8
            j = sqvalue % 8
            for d in ['L', 'R', '-L', '-R']:
                if tempBoard.moveAllowed(i, j, d, -1):
                    tempBoard.move(i, j, d, -1)
                    eval, _ = tuned_minimax(tempBoard.getString(), depth - 1, alpha, beta, 1)
                    if eval < minEval:
                        minEval = eval
                        optimalMove = tempBoard.getString()
                    tempBoard.editBoard(originalBoard)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  
        return minEval, optimalMove

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
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]
    return (2*round((scoreW) / (scoreB + scoreW),2) - 1)

def botPlay(bstr = 'A', difficulty=5, turn=1, moves=0, constantDepth = False):
    if constantDepth:
        depth = difficulty
    else:
        num_pieces = 64 - bstr.count('0')
        endGameWeigth = 0.025
        moveWeigth = 0.1
        depth = math.floor(difficulty / (endGameWeigth * num_pieces + 0.4) + max(moveWeigth*(moves - 50), 0)) 
    print ('Depth (bp): ', depth)
    
    with open('dict6.txt', 'r') as file:
        # Each line will have 3 values: str, mstr, eval
        for line in file:
            if bstr == line.split()[0]:
                eval = line.split()[2]
                print ('Evaluation: ', eval)
                return line.split()[1]
            
    eval, mstr = tuned_minimax(bstr, depth, -math.inf, math.inf, turn)
    # Add str, msr, eval to the file
    # Turn evaluation to string
    with open('dict6.txt', 'a') as file:
        file.write(bstr + ',' + mstr + ',' + str(eval) + '\n')
    print ('Evaluation: ', eval)
    return mstr
    
    