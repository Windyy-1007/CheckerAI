# Checker-AI - By Windyy1007

## Introduction
Checkers is known as a solved game. If two players play perfectly, it will always end up in a draw. This is an engine that can gives accurate reponse for an checker position in a certain of moves ahead, made by a first year university student.

## Method
Current best method is pure Alpha - Beta Tuning Minimax Algorithm. Other method has ben tried such as original Minimax algorithm or Alpha - Beta Tuning Minimax Algorithm with position parameters. But these two methods are either too slow or too inaccurate. The pure minimax Algorithm evaluate simply by deviding its number of pieces with its oppoment's. It also cuts off the branches that are guaranteed to be too good for oppoment.

## How to use

### Running the Game
Run `runner.py` from the command line with the desired parameters:
```
python runner.py [--mode MODE] [--depth DEPTH] [--depth1 DEPTH1] [--depth2 DEPTH2] [--bot-delay BOT_DELAY]
```

### Parameters
- **--mode**: Game mode (default: 0)
  - `0`: Human vs AI Bot
  - `1`: AI Bot vs AI Bot
- **--depth**: Search depth for bot in mode 0 (default: 10)
  - Higher values = stronger but slower
  - `-1`: Random bot
  - `6`: ~1.5 seconds per move
  - `8`: ~15 seconds per move
  - `10`: ~2 minutes per move (best for solving puzzles)
- **--depth1**: Search depth for player 1 in mode 1 (default: 6)
- **--depth2**: Search depth for player 2 in mode 1 (default: 10)
- **--bot-delay**: Delay between bot moves in mode 1, in milliseconds (default: 0)

### Examples
```
# Play against bot with depth 8
python runner.py --mode 0 --depth 8

# Watch two bots play with delay
python runner.py --mode 1 --depth1 6 --depth2 8 --bot-delay 1000

# Easy mode against random bot
python runner.py --mode 0 --depth -1
```

### Changing the AI Model (Advanced)
The current best model is `bp` (bot.py), which uses Alpha-Beta Pruning with move ordering. It's already the default in runner.py.

Alternative models (not recommended):
- `bv2` (botV2.py): Alpha-Beta with position evaluation heuristics (slower, less optimized)
- `v1` (minimaxV1.py): Original Minimax without pruning (much slower, same output as bp)

To switch models, edit the imports and modify the `bot_play_with_depth()` function in runner.py to use the desired model.

## Citation information
Nguyen Huu Nam Phong - First year student at HCMUT, Vietnam (2023)
Team Asignment Introduction of AI - Modifications and updates (2026)
