    
import board as bd
import math
import copy

evalCalls = 0
transposition_table = {}


def quick_material_score(bstr):
    return bstr.count('w') + 2 * bstr.count('W') - bstr.count('b') - 2 * bstr.count('B')


def generate_ordered_moves(tempBoard, originalBoard, turn):
    moves = []
    original_zeros = originalBoard.count('0')

    for i in range(8):
        for j in range(8):
            for d in ['L', 'R', '-L', '-R']:
                if tempBoard.moveAllowed(i, j, d, turn):
                    tempBoard.move(i, j, d, turn)
                    next_bstr = tempBoard.getString()
                    tempBoard.editBoard(originalBoard)

                    capture_score = next_bstr.count('0') - original_zeros
                    material_score = quick_material_score(next_bstr)
                    if turn == -1:
                        material_score = -material_score

                    moves.append((capture_score, material_score, next_bstr))

    moves.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [item[2] for item in moves]

def tuned_minimax(bstr, depth, alpha, beta, turn):
    key = (bstr, depth, turn)
    if key in transposition_table:
        return transposition_table[key]

    tempBoard = bd.Board(bstr)
    originalBoard = bstr
    optimalMove = ''
    
    if tempBoard.endGame(turn):
        result = (tempBoard.utility(turn), optimalMove)
        transposition_table[key] = result
        return result
    
    if depth == 0:
        result = (evaluate(bstr), optimalMove)
        transposition_table[key] = result
        return result

    legal_moves = generate_ordered_moves(tempBoard, originalBoard, turn)
    if not legal_moves:
        result = (tempBoard.utility(turn), optimalMove)
        transposition_table[key] = result
        return result
    
    if turn == 1:
        maxEval = -99
        for next_bstr in legal_moves:
            eval, _ = tuned_minimax(next_bstr, depth - 1, alpha, beta, -1)
            if eval > maxEval:
                maxEval = eval
                optimalMove = next_bstr
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        result = (maxEval, optimalMove)
        transposition_table[key] = result
        return result
    else:
        minEval = 99
        for next_bstr in legal_moves:
            eval, _ = tuned_minimax(next_bstr, depth - 1, alpha, beta, 1)
            if eval < minEval:
                minEval = eval
                optimalMove = next_bstr
            beta = min(beta, eval)
            if beta <= alpha:
                break
        result = (minEval, optimalMove)
        transposition_table[key] = result
        return result

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


def material_ratio(bstr):
    board = bd.Board(bstr)
    scoreW = 0.0
    scoreB = 0.0
    for i in range(8):
        for j in range(8):
            if board.board[i][j] > 0:
                scoreW += board.board[i][j]
            elif board.board[i][j] < 0:
                scoreB += -board.board[i][j]

    total = scoreW + scoreB
    if total == 0:
        return 0.0
    return (scoreW - scoreB) / total


def boosted_depth_for_endgame(bstr, turn, depth):
    if depth < 0:
        return depth

    pieces = 64 - bstr.count('0')
    bonus = 0

    # Endgames are tactical; increase depth when board is simplified.
    if pieces <= 10:
        bonus += 2
    if pieces <= 6:
        bonus += 2

    # If side to move is already ahead in a small endgame, search deeper to convert.
    ratio = material_ratio(bstr)
    ahead = (turn == 1 and ratio > 0.2) or (turn == -1 and ratio < -0.2)
    if pieces <= 12 and ahead:
        bonus += 2

    return min(depth + bonus, 14)

def botPlay(bstr = 'A', difficulty=5, turn=1, moves=0, constantDepth = False):
    transposition_table.clear()
    if constantDepth:
        depth = difficulty
    else:
        num_pieces = 64 - bstr.count('0')
        endGameWeigth = 0.025
        moveWeigth = 0.1
        depth = math.floor(difficulty / (endGameWeigth * num_pieces + 0.4) + max(moveWeigth*(moves - 50), 0)) 
    boosted_depth = boosted_depth_for_endgame(bstr, turn, depth)
    print ('Depth (bp): ', depth, '->', boosted_depth)
    
    
    """
    with open('dict6.txt', 'r') as file:
        # Each line will have 3 values: str, mstr, eval
        for line in file:
            if bstr == line.split()[0]:
                eval = line.split()[2]
                print ('Evaluation: ', eval)
                return line.split()[1]
    
    """
            
    eval, mstr = tuned_minimax(bstr, boosted_depth, -math.inf, math.inf, turn)
    # Add str, msr, eval to the file
    # Turn evaluation to string
    with open('dict6.txt', 'a') as file:
        file.write(bstr + ',' + mstr + ',' + str(eval) + '\n')
    print ('Evaluation: ', eval)
    global evalCalls
    print ('Number of calculated positions: ', evalCalls)
    evalCalls = 0
    return mstr
    
    