import board as bd
import bot as bp
import time

intialPos = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
customPos = '0b0b0b0bb0b0b0b00b0b0b000000000000000000w0w0w0w00w0w0w0ww0w0w0w0' 
evalCalls = 0

def playGame():
    board = bd.Board('0W00000000000000000000000000000000000w00w0w0w00000000000B0000000')
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
    board = bd.Board(intialPos)
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
            suggestedPos = bp.botPlay(curPos, 10, turn)
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
    board = bd.Board(customPos)
    board.betterPrintBoard()
    turn = 1
    while not board.endGame(turn):
        print("Player ", turn, " turn")
        timeStart = time.time()
        curPos = board.getString()
        suggestedPos = bp.botPlay(curPos, 4, turn)
        timeEnd = time.time()
        print('Time to evaluate: ', timeEnd - timeStart)
        board.editBoard(suggestedPos)
        board.betterPrintBoard()
        turn = -turn
    if board.utility(turn) == 1:
        print("Player 1 wins")
        
    else:
        print("Player 2 wins")

def oldBotnewBot():
    board = bd.Board(intialPos)
    board.betterPrintBoard()
    turn = 1
    moves = 0
    global evalCalls
    while not board.endGame(turn) and moves < 1000:
        moves += 1
        print("Player ", turn, " turn")
        if turn == 1:
            timeStart = time.time()
            curPos = board.getString()
            suggestedPos = bp.minimax(curPos, 5, turn)
            timeEnd = time.time()
            print('Time to evaluate: ', timeEnd - timeStart)
            board.editBoard(suggestedPos)
            board.betterPrintBoard()
            turn = -turn
            evalCalls = 0
        else:
            timeStart = time.time()
            curPos = board.getString()
            suggestedPos = bp.botPlay(curPos, 5, turn, moves, False)
            timeEnd = time.time()
            print('Time to evaluate: ', timeEnd - timeStart)
            board.editBoard(suggestedPos)
            board.betterPrintBoard()
            turn = -turn
            evalCalls = 0
            
    if board.utility(turn) == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")    

def main():
    twoBotGame()

if __name__=="__main__": 
    main()
    