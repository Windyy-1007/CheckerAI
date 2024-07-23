    
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
                            optD = str(i) + ' ' + str(j) + ' ' + d
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
                        tempBoard.editBoard(originalBoard)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        return minEval, optimalMove

def stillInBoard(i, j):
    return i >= 0 and i < 8 and j >= 0 and j < 8

def evaluate(string):
    global evalCalls
    evalCalls += 1
    board = bd.Board(string)
    if board.endGame(1):
        return -1
    if board.endGame(-1):
        return 1
    # Basic evaluation function base on the number of pieces
    scoreW = 0.000
    scoreB = 0.000
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]
    pieceW = scoreW
    pieceB = scoreB
    # Heatmap evaluation function
    # Center heatmap
    centerW = 0.7
    promoteLineW = 0.5
    
    for i in [3, 4]:
        for j in [2, 3, 4, 5]:
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]*centerW
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]*centerW
    
    # Unpromoted pieces heatmap
    for j in range(8):
        if board.board[7][j] == 1:
            scoreW += board.board[0][j]*promoteLineW
        if board.board[0][j] == -1:
            scoreB += -board.board[7][j]*promoteLineW

    # Try to trade pieces when ahead.
    if pieceW > pieceB:
        tradeW = min(0.5*(pieceW/pieceB),0.95)
        for i in range(8):
            for j in range(8):
                if board.board[i][j] < 0:
                    if stillInBoard(i+1, j+1):
                        if board.board[i+1][j+1] > 0:
                            scoreW += board.board[i][j]*tradeW
                    if stillInBoard(i+1, j-1):
                        if board.board[i+1][j-1] > 0:
                            scoreW += board.board[i][j]*tradeW
                    if stillInBoard(i-1, j+1):
                        if board.board[i-1][j+1] > 0:
                            scoreW += board.board[i][j]*tradeW
                    if stillInBoard(i-1, j-1):
                        if board.board[i-1][j-1] > 0:
                            scoreW += board.board[i][j]*tradeW
                    if stillInBoard(i, j+2):
                        if board.board[i][j+2] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i, j-2):
                        if board.board[i][j-2] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i+2, j):
                        if board.board[i+2][j] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i-2, j):
                        if board.board[i-2][j] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i+2, j+2):
                        if board.board[i+2][j+2] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i+2, j-2):
                        if board.board[i+2][j-2] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i-2, j+2):
                        if board.board[i-2][j+2] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                    if stillInBoard(i-2, j-2):
                        if board.board[i-2][j-2] > 0:
                            scoreW += board.board[i][j]*tradeW*0.5
                            
    elif pieceW < pieceB:
        tradeB = min(0.5*(pieceB/pieceW),0.95)
        for i in range(8):
            for j in range(8):
                if board.board[i][j] > 0:
                    if stillInBoard(i+1, j+1):
                        if board.board[i+1][j+1] < 0:
                            scoreB += -board.board[i][j]*tradeB
                    if stillInBoard(i+1, j-1):
                        if board.board[i+1][j-1] < 0:
                            scoreB += -board.board[i][j]*tradeB
                    if stillInBoard(i-1, j+1):
                        if board.board[i-1][j+1] < 0:
                            scoreB += -board.board[i][j]*tradeB
                    if stillInBoard(i-1, j-1):
                        if board.board[i-1][j-1] < 0:
                            scoreB += -board.board[i][j]*tradeB
                    if stillInBoard(i, j+2):
                        if board.board[i][j+2] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i, j-2):
                        if board.board[i][j-2] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i+2, j):
                        if board.board[i+2][j] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i-2, j):
                        if board.board[i-2][j] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i+2, j+2):
                        if board.board[i+2][j+2] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i+2, j-2):
                        if board.board[i+2][j-2] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i-2, j+2):
                        if board.board[i-2][j+2] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5
                    if stillInBoard(i-2, j-2):
                        if board.board[i-2][j-2] < 0:
                            scoreB += -board.board[i][j]*tradeB*0.5

                        
    
    # Avoid piece islands in openning
    islandW = 1.5
    islandB = 1.5
    openConsideration = 24
    if pieceW + pieceB > openConsideration:
        for i in range(8):
            if not any(board.board[i][j] > 0 for j in range(8)):
                scoreW -= islandW*((pieceW + pieceB)-openConsideration)/(32-openConsideration)
            if not any(board.board[i][j] < 0 for j in range(8)):
                scoreB -= islandB*((pieceW + pieceB)-openConsideration)/(32-openConsideration)
    
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
    return mstr
    
    