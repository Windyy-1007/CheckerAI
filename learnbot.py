"""
learnbot.py  —  TD-Leaf(λ) learning bot for checkers
======================================================
Strategy: TD-Leaf(λ)
  - A small MLP (65→128→64→1, tanh) maps board positions to a value in [-1, 1].
  - During play the bot uses alpha-beta search with the MLP as leaf evaluator.
  - After each move the leaf values are used to compute a TD error and
    update the network weights with eligibility traces (λ).
  - The "leaf" variant is more stable than plain TD because the α-β search
    already corrects systematic errors in the raw network output.

Difficulty 1-10 controls search depth and noise level:
  1  → depth 1, high noise  (very easy)
  5  → depth 3, low noise   (medium)
  10 → depth 6, no noise    (strong)

Weights are persisted to `learnbot_weights.npz`.
"""

import numpy as np
import board as bd
import math
import os
import random

WEIGHTS_FILE = 'learnbot_weights.npz'

# ──────────────────────────────────────────────
# Board encoding
# ──────────────────────────────────────────────
_PIECE_VAL = {'0': 0.0, 'w': 0.5, 'W': 1.0, 'b': -0.5, 'B': -1.0}

def encode_board(bstr: str, turn: int) -> np.ndarray:
    """Return a 65-d float32 feature vector (64 squares + turn indicator)."""
    feats = np.array([_PIECE_VAL.get(c, 0.0) for c in bstr[:64]], dtype=np.float32)
    return np.append(feats, float(turn) * 0.5)


# ──────────────────────────────────────────────
# Neural network
# ──────────────────────────────────────────────
INPUT_DIM = 65
H1 = 128
H2 = 64


class NeuralNet:
    """Tiny MLP: 65 → 128 → 64 → 1 with tanh activations."""

    def __init__(self):
        rng = np.random.default_rng(0)
        l1 = math.sqrt(6.0 / (INPUT_DIM + H1))
        l2 = math.sqrt(6.0 / (H1 + H2))
        l3 = math.sqrt(6.0 / (H2 + 1))
        self.W1 = rng.uniform(-l1, l1, (INPUT_DIM, H1)).astype(np.float32)
        self.b1 = np.zeros(H1, dtype=np.float32)
        self.W2 = rng.uniform(-l2, l2, (H1, H2)).astype(np.float32)
        self.b2 = np.zeros(H2, dtype=np.float32)
        self.W3 = rng.uniform(-l3, l3, (H2, 1)).astype(np.float32)
        self.b3 = np.zeros(1, dtype=np.float32)

    # ------------------------------------------------------------------
    def forward(self, x: np.ndarray):
        """Returns (scalar value, cache)."""
        a1 = np.tanh(x @ self.W1 + self.b1)
        a2 = np.tanh(a1 @ self.W2 + self.b2)
        v  = np.tanh(a2 @ self.W3 + self.b3)
        return float(v[0]), (x, a1, a2, float(v[0]))

    def grad(self, cache):
        """Gradient of output w.r.t. all parameters (∇V for TD update)."""
        x, a1, a2, v = cache
        g3 = 1.0 - v * v                               # d tanh / dz at output
        g2 = (g3 * self.W3.ravel()) * (1.0 - a2 * a2)
        g1 = (g2 @ self.W2.T)       * (1.0 - a1 * a1)
        return (np.outer(x,  g1), g1,
                np.outer(a1, g2), g2,
                np.outer(a2, [g3]), np.array([g3]))

    def evaluate(self, bstr: str, turn: int = 1) -> float:
        x = encode_board(bstr, turn)
        v, _ = self.forward(x)
        return v

    # ------------------------------------------------------------------
    def save(self, path: str = WEIGHTS_FILE):
        np.savez(path,
                 W1=self.W1, b1=self.b1,
                 W2=self.W2, b2=self.b2,
                 W3=self.W3, b3=self.b3)
        print(f'[LearnBot] Weights saved → {path}')

    def load(self, path: str = WEIGHTS_FILE) -> bool:
        if not os.path.exists(path):
            return False
        d = np.load(path)
        self.W1, self.b1 = d['W1'], d['b1']
        self.W2, self.b2 = d['W2'], d['b2']
        self.W3, self.b3 = d['W3'], d['b3']
        print(f'[LearnBot] Weights loaded ← {path}')
        return True


# ──────────────────────────────────────────────
# TD-Leaf(λ) trainer
# ──────────────────────────────────────────────
class TDLeafTrainer:
    """
    TD-Leaf(λ) update rule.

    At each time-step we have:
      v_t   = value at leaf of α-β search from position s_t
      v_t1  = value at leaf of α-β search from position s_{t+1}
      δ_t   = v_t1 − v_t          (TD error)

    Weight update:
      w ← w + α · δ_t · Σ_{τ≤t} λ^{t−τ} · ∇V(s_τ)
          = w + α · δ_t · e_t

    where e_t is the eligibility trace.
    """

    def __init__(self, net: NeuralNet, alpha: float = 0.0004, lam: float = 0.7):
        self.net   = net
        self.alpha = alpha
        self.lam   = lam
        self._reset()

    def _reset(self):
        n = self.net
        self.eW1 = np.zeros_like(n.W1)
        self.eb1 = np.zeros_like(n.b1)
        self.eW2 = np.zeros_like(n.W2)
        self.eb2 = np.zeros_like(n.b2)
        self.eW3 = np.zeros_like(n.W3)
        self.eb3 = np.zeros_like(n.b3)

    def new_game(self):
        self._reset()

    def step(self, bstr_t: str, turn_t: int, leaf_v_next: float):
        """Single TD-Leaf step using the current position's leaf value."""
        x = encode_board(bstr_t, turn_t)
        v_t, cache = self.net.forward(x)
        delta = leaf_v_next - v_t

        dW1, db1, dW2, db2, dW3, db3 = self.net.grad(cache)

        # Update eligibility traces: e ← λ·e + ∇V(s_t)
        self.eW1 = self.lam * self.eW1 + dW1
        self.eb1 = self.lam * self.eb1 + db1
        self.eW2 = self.lam * self.eW2 + dW2
        self.eb2 = self.lam * self.eb2 + db2
        self.eW3 = self.lam * self.eW3 + dW3
        self.eb3 = self.lam * self.eb3 + db3

        # w ← w + α · δ · e
        lr = self.alpha * delta
        self.net.W1 += lr * self.eW1; self.net.b1 += lr * self.eb1
        self.net.W2 += lr * self.eW2; self.net.b2 += lr * self.eb2
        self.net.W3 += lr * self.eW3; self.net.b3 += lr * self.eb3


# ──────────────────────────────────────────────
# Move generation & alpha-beta
# ──────────────────────────────────────────────
def _get_moves(bstr: str, turn: int) -> list:
    board = bd.Board(bstr)
    moves = []
    for i in range(8):
        for j in range(8):
            for d in ('L', 'R', '-L', '-R'):
                if board.moveAllowed(i, j, d, turn):
                    board.move(i, j, d, turn)
                    moves.append(board.getString())
                    board.editBoard(bstr)
    return moves


def _alphabeta(bstr: str, depth: int, alpha: float, beta: float,
               turn: int, net: NeuralNet, noise: float = 0.0):
    """Returns (leaf_value, best_next_bstr)."""
    board = bd.Board(bstr)
    if board.endGame(turn):
        return float(board.utility(turn)), bstr
    if depth == 0:
        return net.evaluate(bstr, turn), bstr

    moves = _get_moves(bstr, turn)
    if not moves:
        return float(board.utility(turn)), bstr

    best = moves[0]
    if turn == 1:
        best_val = -math.inf
        for m in moves:
            v, _ = _alphabeta(m, depth - 1, alpha, beta, -1, net)
            if noise > 0:
                v += random.gauss(0.0, noise)
            if v > best_val:
                best_val, best = v, m
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best
    else:
        best_val = math.inf
        for m in moves:
            v, _ = _alphabeta(m, depth - 1, alpha, beta, 1, net)
            if noise > 0:
                v += random.gauss(0.0, noise)
            if v < best_val:
                best_val, best = v, m
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best


# ──────────────────────────────────────────────
# Difficulty configuration  (depth, noise)
# ──────────────────────────────────────────────
_DIFF = {
    1:  (1, 0.80),
    2:  (1, 0.50),
    3:  (2, 0.35),
    4:  (2, 0.18),
    5:  (3, 0.12),
    6:  (3, 0.06),
    7:  (4, 0.04),
    8:  (4, 0.01),
    9:  (5, 0.005),
    10: (6, 0.00),
}


# ──────────────────────────────────────────────
# Singleton model + public API
# ──────────────────────────────────────────────
_net = NeuralNet()
_loaded = _net.load()
if not _loaded:
    print('[LearnBot] No saved weights found – using random init.')
    print('[LearnBot] Run with --mode 3 --train to build a model.')

# Persistent online trainer used during live games
_online_trainer = TDLeafTrainer(_net, alpha=0.0002, lam=0.6)


def learnbot_play(bstr: str, difficulty: int, turn: int) -> str:
    """Return the best next board string according to the learned policy."""
    depth, noise = _DIFF.get(max(1, min(10, difficulty)), (3, 0.1))
    print(f'[LearnBot] depth={depth}  noise={noise:.3f}')
    _, best = _alphabeta(bstr, depth, -math.inf, math.inf, turn, _net, noise=noise)
    return best


def learnbot_leaf_value(bstr: str, difficulty: int, turn: int) -> float:
    """Return the leaf value of the best move (used for online TD updates)."""
    depth, _ = _DIFF.get(max(1, min(10, difficulty)), (3, 0.1))
    v, _ = _alphabeta(bstr, depth, -math.inf, math.inf, turn, _net)
    return v


def online_new_game():
    """Reset eligibility traces at the start of a new game."""
    _online_trainer.new_game()


def online_step(bstr_t: str, turn_t: int, leaf_v_next: float):
    """One online TD-Leaf update step during a live game."""
    _online_trainer.step(bstr_t, turn_t, leaf_v_next)


def save_weights(path: str = WEIGHTS_FILE):
    _net.save(path)


# ──────────────────────────────────────────────
# Self-play training loop
# ──────────────────────────────────────────────
_INITIAL = '0b0b0b0bb0b0b0b00b0b0b0b0000000000000000w0w0w0w00w0w0w0ww0w0w0w0'

def train_selfplay(num_games: int = 200,
                   train_depth: int = 2,
                   alpha: float = 0.0005,
                   lam: float = 0.7,
                   save_path: str = WEIGHTS_FILE,
                   callback=None) -> dict:
    """
    Train the neural net via TD-Leaf(λ) self-play.

    Both sides use the current network at `train_depth`.
    After every move the leaf value of the next position is used as the
    TD target for the current position.  At game end the terminal reward
    is used as the final target.

    Draw is declared after 100 consecutive moves without capture or promotion.

    Returns a dict with win/loss/draw counts.
    """
    def move_has_capture_or_promo(b1: str, b2: str) -> bool:
        # Check capture: piece disappeared
        for i in range(64):
            if b1[i] in 'wbWB' and b2[i] == '0':
                return True
        # Check promotion: w→W or b→B
        for i in range(64):
            if (b1[i] == 'w' and b2[i] == 'W') or (b1[i] == 'b' and b2[i] == 'B'):
                return True
        return False

    trainer = TDLeafTrainer(_net, alpha=alpha, lam=lam)
    results = {'W': 0, 'B': 0, 'D': 0}

    for g in range(num_games):
        bstr  = _INITIAL
        board = bd.Board(bstr)
        turn  = 1
        trainer.new_game()
        consecutive_quiet = 0
        total_moves = 0

        while not board.endGame(turn) and total_moves < 320:
            leaf_v, next_bstr = _alphabeta(
                bstr, train_depth, -math.inf, math.inf, turn, _net)

            # TD-Leaf target: leaf value of search from next position
            leaf_v_next, _ = _alphabeta(
                next_bstr, train_depth, -math.inf, math.inf, -turn, _net)

            trainer.step(bstr, turn, leaf_v_next)

            # Track quiet moves (no capture/promotion)
            if move_has_capture_or_promo(bstr, next_bstr):
                consecutive_quiet = 0
            else:
                consecutive_quiet += 1

            bstr = next_bstr
            board.editBoard(bstr)
            turn  = -turn
            total_moves += 1

            # Draw by 100 consecutive quiet moves
            if consecutive_quiet >= 100:
                trainer.step(bstr, turn, 0.0)  # terminal draw
                result = 0
                results['D'] += 1
                break

        else:
            # Game ended by endGame() (no legal moves or all pieces captured) or 320-move limit
            if total_moves >= 320:
                trainer.step(bstr, turn, 0.0)  # draw by 320-move limit
                result = 0
                results['D'] += 1
            else:
                result = float(board.utility(turn))
                trainer.step(bstr, turn, result)

                if result > 0:
                    results['W'] += 1
                elif result < 0:
                    results['B'] += 1
                else:
                    results['D'] += 1

        if callback:
            callback(g + 1, num_games, results)

        if (g + 1) % 25 == 0:
            _net.save(save_path)
            print(f'[LearnBot] {g+1}/{num_games}  '
                  f'W={results["W"]}  B={results["B"]}  D={results["D"]}')

    _net.save(save_path)
    print('[LearnBot] Training complete.')
    return results


# Curriculum learning
# ──────────────────────────────────────────────
def train_curriculum(num_games: int = 1000,
                     opponent_depths: list = None,
                     alpha: float = 0.0005,
                     lam: float = 0.7,
                     save_path: str = WEIGHTS_FILE,
                     no_endgame_boost: bool = False,
                     opponent_move_fn=None,
                     callback=None) -> dict:
    """
    Train the neural net via TD-Leaf(λ) with curriculum learning.
    
    opponent_depths: list of opponent depths for each phase:
      - 0: train against itself (both sides use learn bot search)
      - -1: train against random
      - 1-10: train against minimax at that depth
    
    num_games: total training games, divided equally among phases
    opponent_move_fn: callback(bstr, turn, depth, no_endgame_boost) -> next_bstr
                     Used to get opponent moves for non-self phases
    
    Returns a dict with win/loss/draw counts.
    """
    if opponent_depths is None:
        opponent_depths = [0]
    
    def move_has_capture_or_promo(b1: str, b2: str) -> bool:
        for i in range(64):
            if b1[i] in 'wbWB' and b2[i] == '0':
                return True
        for i in range(64):
            if (b1[i] == 'w' and b2[i] == 'W') or (b1[i] == 'b' and b2[i] == 'B'):
                return True
        return False

    trainer = TDLeafTrainer(_net, alpha=alpha, lam=lam)
    results = {'W': 0, 'B': 0, 'D': 0}
    
    num_phases = len(opponent_depths)
    games_per_phase = num_games // num_phases
    remainder = num_games % num_phases
    
    total_trained = 0
    
    for phase_idx, opponent_depth in enumerate(opponent_depths):
        # Distribute remainder games to first phases
        phase_games = games_per_phase + (1 if phase_idx < remainder else 0)
        phase_start = total_trained
        total_trained += phase_games
        
        print(f'[LearnBot] Phase {phase_idx + 1}/{num_phases} (depth={opponent_depth}): '
              f'{phase_games} games (total: {phase_start + 1}-{total_trained})')
        
        for g in range(phase_games):
            bstr = _INITIAL
            board = bd.Board(bstr)
            turn = 1
            trainer.new_game()
            consecutive_quiet = 0
            total_moves = 0
            
            while not board.endGame(turn) and total_moves < 320:
                if opponent_depth == 0:
                    # Self-play: learn bot on both sides
                    leaf_v, next_bstr = _alphabeta(
                        bstr, 2, -math.inf, math.inf, turn, _net)
                    
                    leaf_v_next, _ = _alphabeta(
                        next_bstr, 2, -math.inf, math.inf, -turn, _net)
                    
                    trainer.step(bstr, turn, leaf_v_next)
                    bstr = next_bstr
                else:
                    # Learn bot makes a move (as side 1 / white)
                    if turn == 1:
                        leaf_v, next_bstr = _alphabeta(
                            bstr, 2, -math.inf, math.inf, turn, _net)
                        
                        leaf_v_next, _ = _alphabeta(
                            next_bstr, 2, -math.inf, math.inf, -turn, _net)
                        
                        trainer.step(bstr, turn, leaf_v_next)
                        bstr = next_bstr
                    else:
                        # Opponent makes a move
                        if opponent_move_fn is not None:
                            next_bstr = opponent_move_fn(bstr, turn, opponent_depth, no_endgame_boost)
                        else:
                            # Fallback: random move if no callback provided
                            import random as rnd
                            temp_board = bd.Board(bstr)
                            candidates = []
                            for i in range(8):
                                for j in range(8):
                                    for d in ['L', 'R', '-L', '-R']:
                                        if temp_board.moveAllowed(i, j, d, turn):
                                            temp_board.move(i, j, d, turn)
                                            candidates.append(temp_board.getString())
                                            temp_board.editBoard(bstr)
                            next_bstr = rnd.choice(candidates) if candidates else bstr
                        
                        # Still track learn bot's perspective for TD updates
                        leaf_v_next, _ = _alphabeta(
                            next_bstr, 2, -math.inf, math.inf, -turn, _net)
                        # Update based on next position from learn bot's search
                        trainer.step(bstr, 1, leaf_v_next)  # Always track white's perspective
                        bstr = next_bstr
                
                # Track quiet moves
                if not move_has_capture_or_promo(board.getString(), bstr):
                    consecutive_quiet += 1
                else:
                    consecutive_quiet = 0
                
                board.editBoard(bstr)
                turn = -turn
                total_moves += 1
                
                if consecutive_quiet >= 100:
                    trainer.step(bstr, turn, 0.0)
                    result = 0
                    results['D'] += 1
                    break
            else:
                if total_moves >= 320:
                    trainer.step(bstr, turn, 0.0)
                    result = 0
                    results['D'] += 1
                else:
                    result = float(board.utility(turn))
                    trainer.step(bstr, turn, result)
                    
                    if result > 0:
                        results['W'] += 1
                    elif result < 0:
                        results['B'] += 1
                    else:
                        results['D'] += 1
            
            # Progress report every 25 games per phase
            if (g + 1) % 25 == 0:
                _net.save(save_path)
                print(f'[LearnBot]   {g+1}/{phase_games} games  '
                      f'W={results["W"]}  B={results["B"]}  D={results["D"]}')
            
            if callback:
                callback(total_trained + 1, num_games, results)
    
    _net.save(save_path)
    print('[LearnBot] Curriculum training complete.')
    return results
