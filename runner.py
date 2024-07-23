import board as bd
import bot as bp
import minimaxV1 as v1
import botV2 as bv2
import time
import pygame

# Constant and Pygame setup
WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH // 8
RADIUS = SQUARE_SIZE // 2 - 5
WHITE = (255, 255, 255)
WHITEGREEN = (239, 255, 251)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (95, 208, 104)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
##


intialPos = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
customPos = '0b0b0b0bb0b0b0b00b0b0b000000000000000000w0w0w0w00w0w0w0ww0w0w0w0' 
evalCalls = 0

#To force draw:
def countPieces(bstr):
    #Count how many 0 in the string
    count = 0
    for i in range(64):
        if bstr[i] == '0':
            count += 1
    return count

    board = bd.Board(intialPos)
    board.betterPrintBoard()
    turn = 1
    moves = 0
    global evalCalls
    while not board.endGame(turn) and moves < 51:
        cp1 = countPieces(board.getString())
        print("Player ", turn, " turn")
        if turn == 1:
            timeStart = time.time()
            curPos = board.getString()
            suggestedPos = bv2.botPlay(curPos, 6, turn, moves, True)
            timeEnd = time.time()
            print('Time to evaluate: ', timeEnd - timeStart)
            board.editBoard(suggestedPos)
            board.betterPrintBoard()
            turn = -turn
            evalCalls = 0
        else:
            timeStart = time.time()
            curPos = board.getString()
            suggestedPos = bp.botPlay(curPos, 6, turn, moves, True)
            timeEnd = time.time()
            print('Time to evaluate: ', timeEnd - timeStart)
            board.editBoard(suggestedPos)
            board.betterPrintBoard()
            turn = -turn
            evalCalls = 0
        cp2 = countPieces(board.getString())
        if cp1 == cp2:
            moves += 1
        else:
            moves = 0
            
    if board.utility(turn) == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")    

# bstr is a string with 64 characters symbolize board: w is white piece, b is black piece, 0 is empty, W is white king, B is black king
def drawBoard(bstr):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(SCREEN, WHITEGREEN, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(SCREEN, GREEN, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(bstr):
    RADIUS = SQUARE_SIZE // 2 - 10
    for i in range(64):
        row = i // 8
        col = i % 8
        if bstr[i] == 'w':
            pygame.draw.circle(SCREEN, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
        elif bstr[i] == 'b':
            pygame.draw.circle(SCREEN, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
        elif bstr[i] == 'W':
            pygame.draw.circle(SCREEN, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            pygame.draw.circle(SCREEN, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS // 2)
        elif bstr[i] == 'B':
            pygame.draw.circle(SCREEN, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)
            pygame.draw.circle(SCREEN, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS // 2)
            

def main():
    MODE = 0
    DEPTH = 5
    # Mode = 0: Play game angainst bot
    # Mode = 1: Two bots play against each other
    # Depth = 6 take on average 1.5 seconds to run a move
    # Depth = 8 take roughly 15 seconds to run a move
    # Depth = 10 take roughly 2 minutes to run a move
    
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    x = -1
    y = -1
    x2 = -1
    y2 = -1
    direction = ''
    turn = 1
    board = bd.Board(intialPos)
    pygame.display.set_caption('Checkers')
    pygame.display.set_icon(pygame.image.load('icon.png'))
    drawBoard(board.getString())
    drawPieces(board.getString())
    pygame.display.update()
    if MODE == 0:
        while run:
            clock.tick(60)
            if turn == 1:
                SCREEN.fill(WHITE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if x == -1 and y == -1:
                                x = pos[0] // SQUARE_SIZE
                                y = pos[1] // SQUARE_SIZE
                                x2 = -1
                                y2 = -1
                                print('From: ', x, y)
                                drawBoard(board.getString())
                                pygame.draw.rect(SCREEN, RED, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                drawPieces(board.getString())
                                pygame.display.update()
                            else:
                                x2 = pos[0] // SQUARE_SIZE
                                y2 = pos[1] // SQUARE_SIZE
                                direction = ''
                                if x2 > x and y2 > y:
                                    direction = '-R'
                                elif x2 > x and y2 < y:
                                    direction = 'R'
                                elif x2 < x and y2 > y:
                                    direction = '-L'
                                elif x2 < x and y2 < y:
                                    direction = 'L'
                                if (x != -1 and y != -1 and x2 != -1 and y2 != -1):                 
                                    if board.move(y, x, direction, turn):
                                        print(x, y, direction)
                                        turn = -turn
                                        SCREEN.fill(WHITE)
                                        drawBoard(board.getString())
                                        drawPieces(board.getString())
                                        pygame.display.update()
                                    else:
                                        print("Invalid move", x, y, direction)                                    
                                x = -1
                                y = -1
                                direction = ''
                                print('To: ', x2, y2)
                                break
                SCREEN.fill(WHITE)
            else:
                print("Player ", turn, " turn")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                timeStart = time.time()
                curPos = board.getString()
                suggestedPos = bp.botPlay(curPos, DEPTH, turn, 0, True)
                timeEnd = time.time()
                print('Time to evaluate: ', timeEnd - timeStart)
                print('Number of evaluations: ', evalCalls)
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
        if board.utility(turn) == 1:
            print("Player 1 wins")
        else:
            print("Player 2 wins")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

        pygame.display.update()
        pygame.quit()
    if MODE == 1:
        while run:
            clock.tick(60)
            
            if turn == 1:
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
                print("Player ", turn, " turn")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                timeStart = time.time()
                curPos = board.getString()
                suggestedPos = bp.botPlay(curPos, DEPTH, turn, 0, True)
                timeEnd = time.time()
                print('Time to evaluate: ', timeEnd - timeStart)
                print('Number of evaluations: ', evalCalls)
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
            else:
                print("Player ", turn, " turn")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        run = False
                timeStart = time.time()
                curPos = board.getString()
                suggestedPos = bp.botPlay(curPos, DEPTH, turn, 0, True)
                timeEnd = time.time()
                print('Time to evaluate: ', timeEnd - timeStart)
                print('Number of evaluations: ', evalCalls)
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
        if board.utility(turn) == 1:
            print("Player 1 wins")
        else:
            print("Player 2 wins")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

        pygame.display.update()
        pygame.quit()            
if __name__=="__main__": 
    main()
    