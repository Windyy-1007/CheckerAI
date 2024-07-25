# Checker-AI - By Windyy1007

## Introduction
Checkers is known as a solved game. If two players play perfectly, it will always end up in a draw. This is an engine that can gives accurate reponse for an checker position in a certain of moves ahead, made by a first year university student.

## Method
Current best method is pure Alpha - Beta Tuning Minimax Algorithm. Other method has ben tried such as original Minimax algorithm or Alpha - Beta Tuning Minimax Algorithm with position parameters. But these two methods are either too slow or too inaccurate. The pure minimax Algorithm evaluate simply by deviding its number of pieces with its oppoment's. It also cuts off the branches that are guaranteed to be too good for oppoment.

## How to use
1. Open "runner.py" file.
2. At main function, change MODE, DEPTH and BOT_DELAY as your desire. Instructions for these parameters are noted in the source code.
3. If you wish to change the model to test out yourselves, you can change import model in the source code to other model. If you dont, please skip this step. bp import current model. bv2 import the AB Tuning with parameters model. v1 import original minimax engine, which will return the same output as bp, but much slower.
4. Run the file and play with the bot.

## Citation information
Nguyen Huu Nam Phong - First year student at HCMUT, Vietnam.
