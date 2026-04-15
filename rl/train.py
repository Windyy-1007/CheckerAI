"""Self-play training script for the RL checkers bot.

Usage:
    python -m rl.train                     # default 5000 games
    python -m rl.train --games 20000       # more games
    python -m rl.train --games 10000 --lr 0.0005 --epsilon 0.2
    python -m rl.train --resume            # continue training from saved policy
"""
import os
import sys
import argparse
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import board as bd
from rl.agent import RLBot, DEFAULT_POLICY

INITIAL_POS = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'
MAX_MOVES = 200  # per game, to avoid infinite loops


def play_one_game(bot, move_limit=MAX_MOVES):
    """Play a self-play game. Returns (result, move_count).

    result: 1 = white win, -1 = black win, 0 = draw (move limit).
    """
    game_board = bd.Board(INITIAL_POS)
    turn = 1
    history = []  # list of (bstr, turn)
    move_count = 0

    while move_count < move_limit:
        bstr = game_board.getString()

        if game_board.endGame(turn):
            result = game_board.utility(turn)
            break

        next_bstr = bot.choose_move(bstr, turn)
        history.append((bstr, turn, next_bstr))
        game_board.editBoard(next_bstr)
        turn = -turn
        move_count += 1
    else:
        result = 0  # draw by move limit

    # Backward TD updates through the game history
    for i, (bstr, t, next_bstr) in enumerate(history):
        is_last = (i == len(history) - 1)
        if is_last:
            # Terminal: reward is the game result (from white's perspective)
            reward = float(result)
            bot.td_update(bstr, next_bstr, reward, done=True)
        else:
            # Intermediate: small step reward to encourage progress
            reward = 0.0
            bot.td_update(bstr, next_bstr, reward, done=False)

    return result, move_count


def train(num_games=5000, lr=0.001, epsilon=0.15, gamma=0.99,
          save_every=500, resume=False, policy_path=None):
    if policy_path is None:
        policy_path = DEFAULT_POLICY

    bot = RLBot(
        policy_path=policy_path if resume else None,
        lr=lr,
        epsilon=epsilon,
        gamma=gamma,
    )

    stats = {'white_wins': 0, 'black_wins': 0, 'draws': 0}
    t0 = time.time()

    for game_num in range(1, num_games + 1):
        # Decay epsilon over training
        bot.epsilon = max(0.05, epsilon * (1 - game_num / num_games))

        result, moves = play_one_game(bot)

        if result == 1:
            stats['white_wins'] += 1
        elif result == -1:
            stats['black_wins'] += 1
        else:
            stats['draws'] += 1

        if game_num % 100 == 0:
            elapsed = time.time() - t0
            w = stats['white_wins']
            b = stats['black_wins']
            d = stats['draws']
            print(f"Game {game_num}/{num_games} | W:{w} B:{b} D:{d} | "
                  f"eps={bot.epsilon:.3f} | {elapsed:.1f}s")

        if game_num % save_every == 0:
            bot.save(policy_path)
            print(f"  -> Policy saved to {policy_path}")

    # Final save
    bot.save(policy_path)
    elapsed = time.time() - t0
    print(f"\nTraining complete: {num_games} games in {elapsed:.1f}s")
    print(f"Results: W={stats['white_wins']} B={stats['black_wins']} D={stats['draws']}")
    print(f"Policy saved to {policy_path}")


def main():
    parser = argparse.ArgumentParser(description='Train RL checkers bot via self-play')
    parser.add_argument('--games', type=int, default=5000, help='Number of self-play games')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--epsilon', type=float, default=0.15, help='Initial exploration rate')
    parser.add_argument('--gamma', type=float, default=0.99, help='Discount factor')
    parser.add_argument('--save-every', type=int, default=500, help='Save policy every N games')
    parser.add_argument('--resume', action='store_true', help='Resume training from existing policy')
    parser.add_argument('--policy', type=str, default=None, help='Policy file path')
    args = parser.parse_args()

    train(
        num_games=args.games,
        lr=args.lr,
        epsilon=args.epsilon,
        gamma=args.gamma,
        save_every=args.save_every,
        resume=args.resume,
        policy_path=args.policy,
    )


if __name__ == '__main__':
    main()
