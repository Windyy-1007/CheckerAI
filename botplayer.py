import runner
import math

def minimax(str, depth, player):
    curBoard = runner.Board(str)
    optimal_action_x = 0
    optimal_action_y = 0
    optimal_direction = 'L'
    
    if depth == 0 or curBoard.endGame():
        curBoard.movePiece(optimal_action_x, optimal_action_y, optimal_direction, player)
        return curBoard.getString()
    if player == 1:
        bestVal = -math.inf
        for i in range(8):
            for j in range(8):
                if curBoard.movePiece(i, j, 1):
                    value = minimax(evaluate(curBoard), depth - 1, -1)
                    bestVal = max(bestVal, value)
                    optimal_action_x = i
                    optimal_action_y = j
                    optimal_direction = 'R'
        curBoard.movePiece(optimal_action_x, optimal_action_y,optimal_direction, 1)
        return curBoard.getString()
    else:
        bestVal = math.inf
        for i in range(8):
            for j in range(8):
                if curBoard.movePiece(i, j, 'L', -1):
                    value = minimax(evaluate(curBoard), depth - 1, 1)
                    bestVal = min(bestVal, value)
                    optimal_action_x = i
                    optimal_action_y = j
                    optimal_direction = 'L'
                if curBoard.movePiece(i, j, 'R', -1):
                    value = minimax(evaluate(curBoard), depth - 1, 1)
                    bestVal = min(bestVal, value)
                    optimal_action_x = i
                    optimal_action_y = j
                    optimal_direction = 'R'
        curBoard.movePiece(optimal_action_x, optimal_action_y,optimal_direction, -1)
        return curBoard.getString()

def evaluate(str):
    board = runner.Board(str)
    scoreW = 0
    scoreB = 0
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
            elif board.board[i][j] < 0:
                scoreB += board.board[i][j]
    return (1000 * scoreW) / (1000 * scoreB)
            
def min_value(str, depth):
    board = runner.Board(str)
    if board.endGame():
        return board.utility()
    v = math.inf
    for i in range(8):
        for j in range(8):
            if board.movePiece(i, j, -1):
                v = min(v, max_value(evaluate(board)))
    return v

def max_value(str, depth):
    board = runner.Board(str)
    if board.endGame():
        return board.utility()
    v = -math.inf
    for i in range(8):
        for j in range(8):
            if board.movePiece(i, j, 1):
                v = max(v, min_value(evaluate(board)))
    return v

