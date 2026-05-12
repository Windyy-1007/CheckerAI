import board as bd
import bot as bp
import minimaxV1 as v1
import botV2 as bv2
import learnbot as lb
import time
import pygame
import argparse
import random


def move_had_capture_or_promotion(bstr_before: str, bstr_after: str) -> bool:
    """
    Check if a move involved a capture (piece removed) or promotion (w→W or b→B).
    """
    # Check for capture: any piece disappeared
    for i in range(64):
        if bstr_before[i] in 'wbWB' and bstr_after[i] == '0':
            return True
        if bstr_before[i] == '0' and bstr_after[i] in 'wbWB':
            return False  # piece appeared, but check promotion below
    
    # Check for promotion: w→W or b→B
    for i in range(64):
        if (bstr_before[i] == 'w' and bstr_after[i] == 'W') or \
           (bstr_before[i] == 'b' and bstr_after[i] == 'B'):
            return True
    
    return False

# Constant and Pygame setup
WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH // 8
RADIUS = SQUARE_SIZE // 2 - 5
WHITE = (255, 255, 255)
WHITEGREEN = (239, 255, 251)
WHITERED = (255, 164, 164)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (95, 208, 104)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
##


intialPos = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
customPos = intialPos 
evalCalls = 0

#To force draw:
def countPieces(bstr):
    #Count how many 0 in the string
    count = 0
    for i in range(64):
        if bstr[i] == '0':
            count += 1
    return count

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
            

def parse_args():
    parser = argparse.ArgumentParser(description='Checkers runner configuration')
    parser.add_argument('--mode', type=int, default=0, choices=[0, 1, 2, 3],
                        help=('0: human vs minimax  '
                              '1: minimax vs minimax  '
                              '2: human vs learn-bot  '
                              '3: minimax vs learn-bot'))
    parser.add_argument('--depth',  type=int, default=10,
                        help='Minimax depth in mode 0 (-1 = random)')
    parser.add_argument('--depth1', type=int, default=6,
                        help='Minimax depth for player 1 in mode 1 (-1 = random)')
    parser.add_argument('--depth2', type=int, default=10,
                        help='Minimax depth for player 2 in mode 1 (-1 = random)')
    parser.add_argument('--bot-delay', type=int, default=0,
                        help='Delay between bot moves in ms (modes 1, 3)')
    parser.add_argument('--difficulty', type=int, default=5,
                        metavar='1-10',
                        help='Learn-bot difficulty 1 (easiest) … 10 (hardest) for modes 2 & 3')
    parser.add_argument('--color', type=int, default=0, choices=[0, 1],
                        help='Human piece color in modes 0/2: 0=white, 1=black')
    parser.add_argument('--bot-color', type=int, default=0, choices=[0, 1],
                        help='Minimax color in mode 3: 0=white (turn 1), 1=black (turn -1)')
    parser.add_argument('--train', action='store_true',
                        help='Enable online TD-Leaf learning for the learn-bot during mode 3')
    parser.add_argument('--train-games', type=int, default=100,
                        help='Run N self-play training games before entering mode 3 (use with --train)')
    parser.add_argument('--curriculum', type=str, default=None,
                        help='Curriculum phases (comma-separated depths): 0=self, -1=random, 1-10=minimax depth. '
                             'E.g., "0,0,2,2,2,2,2,4,4,6" divides --train-games equally among phases.')
    parser.add_argument('--games', type=int, default=1,
                        help='Number of games to play in mode 3 (with --train, learns across all games)')
    parser.add_argument('--no-endgame-boost', action='store_true',
                        help='Disable minimax endgame depth boost (search exact depth, not adaptive)')
    return parser.parse_args()


def random_bot_play(bstr, turn):
    temp_board = bd.Board(bstr)
    candidates = []
    for i in range(8):
        for j in range(8):
            for d in ['L', 'R', '-L', '-R']:
                if temp_board.moveAllowed(i, j, d, turn):
                    temp_board.move(i, j, d, turn)
                    candidates.append(temp_board.getString())
                    temp_board.editBoard(bstr)
    if not candidates:
        return bstr
    return random.choice(candidates)


def bot_play_with_depth(bstr, depth, turn, no_endgame_boost=False):
    if depth == -1:
        return random_bot_play(bstr, turn)
    return bp.botPlay(bstr, depth, turn, 0, True, no_endgame_boost)


def main():
    args = parse_args()
    MODE       = args.mode
    DEPTH      = args.depth
    DEPTH1     = args.depth1
    DEPTH2     = args.depth2
    BOT_DELAY  = args.bot_delay
    DIFFICULTY = max(1, min(10, args.difficulty))
    # Human color: 1 = white, -1 = black
    HUMAN_TURN = 1 if args.color == 0 else -1
    # Minimax color in mode 3: 1 = white, -1 = black
    MINIMAX_TURN_M3 = 1 if args.bot_color == 0 else -1
    DO_TRAIN   = args.train
    TRAIN_GAMES = args.train_games
    CURRICULUM = args.curriculum
    NUM_GAMES   = args.games
    NO_ENDGAME_BOOST = args.no_endgame_boost

    # Mode = 0: human vs minimax bot
    # Mode = 1: minimax vs minimax
    # Mode = 2: human vs learn-bot   (--color selects human side)
    # Mode = 3: minimax vs learn-bot (--bot-color selects minimax side,
    #            --train enables online TD-Leaf learning,
    #            --train-games N pre-trains for N self-play games first)

    # ── optional pre-training before mode 3 ──────────────────────────────
    if MODE == 3 and DO_TRAIN and TRAIN_GAMES > 0:
        if CURRICULUM is not None:
            # Curriculum learning mode
            curriculum_phases = [int(d) for d in CURRICULUM.split(',')]
            print(f'[LearnBot] Curriculum training: {curriculum_phases} over {TRAIN_GAMES} games …')
            
            # Create opponent move callback
            def opponent_move_fn(bstr, turn, depth, no_endgame_boost):
                """Generate opponent move using random or minimax at given depth."""
                if depth == -1:
                    return random_bot_play(bstr, turn)
                else:
                    return bp.botPlay(bstr, depth, turn, 0, True, no_endgame_boost)
            
            lb.train_curriculum(num_games=TRAIN_GAMES, 
                              opponent_depths=curriculum_phases,
                              no_endgame_boost=NO_ENDGAME_BOOST,
                              opponent_move_fn=opponent_move_fn)
        else:
            # Standard self-play training
            print(f'[LearnBot] Pre-training for {TRAIN_GAMES} self-play games …')
            lb.train_selfplay(num_games=TRAIN_GAMES)

    pygame.init()
    run = True
    game_over = False
    clock = pygame.time.Clock()
    x = -1
    y = -1
    x2 = -1
    y2 = -1
    direction = ''
    turn = 1
    board = bd.Board(customPos)
    pygame.display.set_caption('Checkers')
    pygame.display.set_icon(pygame.image.load('icon.png'))
    drawBoard(board.getString())
    drawPieces(board.getString())
    pygame.display.update()

    # ─────────────────────────────────────────────────────────────────────
    # Shared human input handler used in modes 0 and 2
    # ─────────────────────────────────────────────────────────────────────
    def handle_human_input():
        """
        Process one frame of human mouse input.
        Returns True if a valid move was made (turn should flip),
        False otherwise, or None if the window was closed.
        """
        nonlocal x, y, x2, y2, direction, run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if x == -1 and y == -1:
                    x = pos[0] // SQUARE_SIZE
                    y = pos[1] // SQUARE_SIZE
                    print('From:', x, y)
                    drawBoard(board.getString())
                    pygame.draw.rect(SCREEN, RED,
                                     (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    for d in ['L', 'R', '-L', '-R']:
                        if board.moveAllowed(y, x, d, turn):
                            if d == 'L':
                                pygame.draw.rect(SCREEN, WHITERED,
                                    ((x - 1) * SQUARE_SIZE, (y - 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            elif d == 'R':
                                pygame.draw.rect(SCREEN, WHITERED,
                                    ((x + 1) * SQUARE_SIZE, (y - 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            elif d == '-L':
                                pygame.draw.rect(SCREEN, WHITERED,
                                    ((x - 1) * SQUARE_SIZE, (y + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            elif d == '-R':
                                pygame.draw.rect(SCREEN, WHITERED,
                                    ((x + 1) * SQUARE_SIZE, (y + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    drawPieces(board.getString())
                    pygame.display.update()
                else:
                    x2 = pos[0] // SQUARE_SIZE
                    y2 = pos[1] // SQUARE_SIZE
                    direction = ''
                    if   x2 > x and y2 > y: direction = '-R'
                    elif x2 > x and y2 < y: direction = 'R'
                    elif x2 < x and y2 > y: direction = '-L'
                    elif x2 < x and y2 < y: direction = 'L'
                    moved = False
                    if x != -1 and y != -1 and x2 != -1 and y2 != -1:
                        if board.move(y, x, direction, turn):
                            print(x, y, direction)
                            moved = True
                        else:
                            print('Invalid move', x, y, direction)
                    x = y = -1
                    direction = ''
                    print('To:', x2, y2)
                    SCREEN.fill(WHITE)
                    drawBoard(board.getString())
                    drawPieces(board.getString())
                    pygame.display.update()
                    if moved:
                        return True
        return False

    # ─────────────────────────────────────────────────────────────────────
    if MODE == 0:
        # Human vs minimax.  --color 0 = human is white, 1 = human is black.
        while run:
            clock.tick(60)
            if turn == HUMAN_TURN and not board.endGame(turn):
                SCREEN.fill(WHITE)
                result = handle_human_input()
                if result is True:
                    turn = -turn
                    SCREEN.fill(WHITE)
                    drawBoard(board.getString())
                    drawPieces(board.getString())
                    pygame.display.update()
            elif turn != HUMAN_TURN and not board.endGame(turn):
                side = 'White' if turn == 1 else 'Black'
                print(f"Minimax ({side})'s turn")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                timeStart = time.time()
                curPos = board.getString()
                suggestedPos = bot_play_with_depth(curPos, DEPTH, turn, NO_ENDGAME_BOOST)
                timeEnd = time.time()
                print('Time to evaluate:', timeEnd - timeStart)
                print('Number of evaluations:', evalCalls)
                print('=============================')
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
            elif board.endGame(turn):
                result = board.utility(turn)
                print('White wins' if result == 1 else 'Black wins')
                run = False
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    # ─────────────────────────────────────────────────────────────────────
    if MODE == 1:
        run = True
        while run:
            clock.tick(60)
            pygame.time.delay(BOT_DELAY)

            if turn == 1 and not board.endGame(turn):
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
                print("White's turn")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                timeStart = time.time()
                suggestedPos = bot_play_with_depth(board.getString(), DEPTH1, turn, NO_ENDGAME_BOOST)
                print('Time to evaluate:', time.time() - timeStart)
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
            elif turn == -1 and not board.endGame(turn):
                print("Black's turn")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                timeStart = time.time()
                suggestedPos = bot_play_with_depth(board.getString(), DEPTH2, turn, NO_ENDGAME_BOOST)
                print('Time to evaluate:', time.time() - timeStart)
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
            if board.endGame(turn):
                result = board.utility(turn)
                print('White wins' if result == 1 else 'Black wins')
                run = False
                game_over = True

    # ─────────────────────────────────────────────────────────────────────
    if MODE == 2:
        # Human vs learn-bot.  --color 0 = human is white, 1 = human is black.
        # The learn-bot always learns online via TD-Leaf(λ) — no pre-training needed.
        lb.online_new_game()
        run = True
        prev_bstr = board.getString()
        while run:
            clock.tick(60)
            if turn == HUMAN_TURN and not board.endGame(turn):
                SCREEN.fill(WHITE)
                result = handle_human_input()
                if result is True:
                    # TD update: human just moved, so the learnbot side
                    # gets a signal from the new board state.
                    leaf_v_next = lb.learnbot_leaf_value(
                        board.getString(), DIFFICULTY, -HUMAN_TURN)
                    lb.online_step(prev_bstr, -HUMAN_TURN, leaf_v_next)
                    prev_bstr = board.getString()
                    turn = -turn
                    SCREEN.fill(WHITE)
                    drawBoard(board.getString())
                    drawPieces(board.getString())
                    pygame.display.update()
            elif turn != HUMAN_TURN and not board.endGame(turn):
                side = 'White' if turn == 1 else 'Black'
                print(f'[LearnBot] ({side}) thinking …  difficulty={DIFFICULTY}')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                timeStart = time.time()
                curPos = board.getString()
                suggestedPos = lb.learnbot_play(curPos, DIFFICULTY, turn)
                print(f'[LearnBot] Time: {time.time() - timeStart:.2f}s')
                # TD update for the learnbot's own move
                leaf_v_next = lb.learnbot_leaf_value(
                    suggestedPos, DIFFICULTY, -turn)
                lb.online_step(curPos, turn, leaf_v_next)
                prev_bstr = suggestedPos
                board.editBoard(suggestedPos)
                turn = -turn
                SCREEN.fill(WHITE)
                drawBoard(board.getString())
                drawPieces(board.getString())
                pygame.display.update()
            elif board.endGame(turn):
                result = board.utility(turn)
                # Terminal update
                lb.online_step(board.getString(), -HUMAN_TURN, float(result))
                lb.save_weights()
                print('White wins' if result == 1 else 'Black wins')
                run = False
                game_over = True

    # ─────────────────────────────────────────────────────────────────────
    if MODE == 3:
        # Minimax vs learn-bot.
        # --bot-color 0 → minimax is white (turn 1), learnbot is black (-1)
        # --bot-color 1 → minimax is black (turn -1), learnbot is white (1)
        # --train       → enable online TD-Leaf updates for the learn-bot
        # --games N     → play N consecutive games (learning persists across games)
        LEARNBOT_TURN = -MINIMAX_TURN_M3
        m3_results = {'W': 0, 'B': 0, 'D': 0}

        for game_idx in range(NUM_GAMES):
            if NUM_GAMES > 1:
                print(f'\n=== Game {game_idx + 1}/{NUM_GAMES} ===')
            board.editBoard(customPos)
            turn = 1
            if DO_TRAIN:
                lb.online_new_game()
            run = True
            consecutive_quiet_moves = 0  # moves without capture/promotion
            total_moves = 0  # safety limit at 320 moves
            while run:
                clock.tick(60)
                pygame.time.delay(BOT_DELAY)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        game_over = True
                        NUM_GAMES = 0  # abort remaining games

                if not run:
                    break

                if not board.endGame(turn):
                    SCREEN.fill(WHITE)
                    drawBoard(board.getString())
                    drawPieces(board.getString())
                    pygame.display.update()

                    curPos = board.getString()
                    timeStart = time.time()

                    if turn == MINIMAX_TURN_M3:
                        side = 'White' if turn == 1 else 'Black'
                        print(f'[Minimax]   ({side}) thinking …')
                        suggestedPos = bot_play_with_depth(curPos, DEPTH, turn, NO_ENDGAME_BOOST)
                        print(f'[Minimax]   Time: {time.time() - timeStart:.2f}s')
                    else:
                        side = 'White' if turn == 1 else 'Black'
                        print(f'[LearnBot] ({side}) thinking …  difficulty={DIFFICULTY}')
                        suggestedPos = lb.learnbot_play(curPos, DIFFICULTY, turn)
                        print(f'[LearnBot]  Time: {time.time() - timeStart:.2f}s')
                        if DO_TRAIN:
                            leaf_v_next = lb.learnbot_leaf_value(suggestedPos, DIFFICULTY, -turn)
                            lb.online_step(curPos, turn, leaf_v_next)

                    # Track consecutive quiet moves (no capture/promotion)
                    if move_had_capture_or_promotion(curPos, suggestedPos):
                        consecutive_quiet_moves = 0
                    else:
                        consecutive_quiet_moves += 1
                        if consecutive_quiet_moves >= 100:
                            # Draw by 100 consecutive moves without capture/promotion
                            result = 0
                            if DO_TRAIN:
                                lb.online_step(suggestedPos, -turn, float(result))
                                lb.save_weights()
                            m3_results['D'] += 1
                            print(f'Draw (100 moves without capture/promotion)  |  W={m3_results["W"]}  B={m3_results["B"]}  D={m3_results["D"]}')
                            run = False
                            if game_idx == NUM_GAMES - 1:
                                game_over = True
                            break

                    board.editBoard(suggestedPos)
                    turn = -turn
                    total_moves += 1
                    
                    # Safety limit: draw if 320 moves reached
                    if total_moves >= 320:
                        result = 0
                        if DO_TRAIN:
                            lb.online_step(suggestedPos, -turn, float(result))
                            lb.save_weights()
                        m3_results['D'] += 1
                        print(f'Draw (320-move limit)  |  W={m3_results["W"]}  B={m3_results["B"]}  D={m3_results["D"]}')
                        run = False
                        if game_idx == NUM_GAMES - 1:
                            game_over = True
                        break
                    
                    SCREEN.fill(WHITE)
                    drawBoard(board.getString())
                    drawPieces(board.getString())
                    pygame.display.update()
                else:
                    result = board.utility(turn)
                    if DO_TRAIN:
                        lb.online_step(board.getString(), LEARNBOT_TURN, float(result))
                        lb.save_weights()
                    winner = 'White wins' if result == 1 else ('Black wins' if result == -1 else 'Draw')
                    if result == 1:   m3_results['W'] += 1
                    elif result == -1: m3_results['B'] += 1
                    else:              m3_results['D'] += 1
                    print(f'{winner}  |  W={m3_results["W"]}  B={m3_results["B"]}  D={m3_results["D"]}')
                    run = False
                    if game_idx == NUM_GAMES - 1:
                        game_over = True

        if NUM_GAMES > 1:
            print(f'\n=== Final: W={m3_results["W"]}  B={m3_results["B"]}  D={m3_results["D"]} ===')
        if not game_over:
            game_over = True

    # ─────────────────────────────────────────────────────────────────────
    # Freeze: keep window open until user closes it
    if game_over:
        freeze = True
        while freeze:
            SCREEN.fill(WHITE)
            drawBoard(board.getString())
            drawPieces(board.getString())
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    freeze = False

    pygame.quit()


if __name__ == '__main__':
    main()
