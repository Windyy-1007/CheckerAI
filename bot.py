    
import board as bd
import math
import copy

evalCalls = 0

def tuned_minimax(bstr, depth, alpha, beta, turn):
    tempBoard = bd.Board(bstr)
    originalBoard = bstr
    optimalMove = ''
    optD = ''
    
    if tempBoard.endGame(turn):
        return tempBoard.utility(turn), optimalMove
    
    if depth == 0:
        return evaluate(bstr), optimalMove
    
    if turn == 1:
        maxEval = -99
        for i in range(8):
            for j in range(8):
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
        for i in range(8):
            for j in range(8):   
                for d in ['L', 'R', '-L', '-R']:
                    if tempBoard.moveAllowed(i, j, d, -1):
                        tempBoard.move(i, j, d, -1)
                        eval, _ = tuned_minimax(tempBoard.getString(), depth - 1, alpha, beta, 1)
                        if eval < minEval:
                            minEval = eval
                            optimalMove = tempBoard.getString()
                            optD = str(i) + ' ' + str(j) + ' ' + d
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
    return round(2*((scoreW) / (scoreB + scoreW)) - 1, 5)

def botPlay(bstr = 'A', difficulty=5, turn=1, moves=0, constantDepth = False):
    if constantDepth:
        depth = difficulty
    else:
        num_pieces = 64 - bstr.count('0')
        endGameWeigth = 0.025
        moveWeigth = 0.1
        depth = math.floor(difficulty / (endGameWeigth * num_pieces + 0.4) + max(moveWeigth*(moves - 50), 0)) 
    print ('Depth (bp): ', depth)
    
    
    """
    with open('dict6.txt', 'r') as file:
        # Each line will have 3 values: str, mstr, eval
        for line in file:
            if bstr == line.split()[0]:
                eval = line.split()[2]
                print ('Evaluation: ', eval)
                return line.split()[1]
    
    """
            
    eval, mstr = tuned_minimax(bstr, depth, -math.inf, math.inf, turn)
    # Add str, msr, eval to the file
    # Turn evaluation to string
    with open('dict6.txt', 'a') as file:
        file.write(bstr + ',' + mstr + ',' + str(eval) + '\n')
    print ('Evaluation: ', eval)
    global evalCalls
    print ('Number of calculated positions: ', evalCalls)
    evalCalls = 0
    return mstr
    
    