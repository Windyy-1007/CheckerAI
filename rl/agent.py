"""RL agent using a small neural network value function trained with TD-learning."""
import os
import pickle
import numpy as np
import sys

# Allow importing board from the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rl.features import extract_features

POLICY_DIR = os.path.join(os.path.dirname(__file__), 'policies')
DEFAULT_POLICY = os.path.join(POLICY_DIR, 'default.pkl')

# --------------- tiny numpy MLP ---------------

def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(np.float32)

def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    t = np.tanh(x)
    return 1 - t * t


class NeuralNet:
    """2-hidden-layer MLP: input -> 64 -> 32 -> 1 (tanh output in [-1, 1])."""

    def __init__(self, input_size=32, h1=64, h2=32):
        scale1 = np.sqrt(2.0 / input_size)
        scale2 = np.sqrt(2.0 / h1)
        scale3 = np.sqrt(2.0 / h2)
        self.W1 = np.random.randn(input_size, h1).astype(np.float32) * scale1
        self.b1 = np.zeros(h1, dtype=np.float32)
        self.W2 = np.random.randn(h1, h2).astype(np.float32) * scale2
        self.b2 = np.zeros(h2, dtype=np.float32)
        self.W3 = np.random.randn(h2, 1).astype(np.float32) * scale3
        self.b3 = np.zeros(1, dtype=np.float32)

    def forward(self, x):
        """Return (value, cache) where cache stores intermediates for backprop."""
        z1 = x @ self.W1 + self.b1
        a1 = relu(z1)
        z2 = a1 @ self.W2 + self.b2
        a2 = relu(z2)
        z3 = a2 @ self.W3 + self.b3
        out = tanh(z3)
        cache = (x, z1, a1, z2, a2, z3)
        return out.item(), cache

    def backward(self, cache, grad_out):
        """Compute gradients w.r.t. all parameters."""
        x, z1, a1, z2, a2, z3 = cache
        # Reshape for consistent matrix ops
        x = x.reshape(1, -1)
        a1 = a1.reshape(1, -1)
        a2 = a2.reshape(1, -1)

        d3 = grad_out * tanh_deriv(z3).reshape(1, -1)  # (1,1)
        dW3 = a2.T @ d3
        db3 = d3.flatten()

        d2 = (d3 @ self.W3.T) * relu_deriv(z2).reshape(1, -1)
        dW2 = a1.T @ d2
        db2 = d2.flatten()

        d1 = (d2 @ self.W2.T) * relu_deriv(z1).reshape(1, -1)
        dW1 = x.T @ d1
        db1 = d1.flatten()

        return {'W1': dW1, 'b1': db1, 'W2': dW2, 'b2': db2, 'W3': dW3, 'b3': db3}

    def update(self, grads, lr):
        """SGD update."""
        self.W1 -= lr * grads['W1']
        self.b1 -= lr * grads['b1']
        self.W2 -= lr * grads['W2']
        self.b2 -= lr * grads['b2']
        self.W3 -= lr * grads['W3']
        self.b3 -= lr * grads['b3']

    def get_params(self):
        return {
            'W1': self.W1.copy(), 'b1': self.b1.copy(),
            'W2': self.W2.copy(), 'b2': self.b2.copy(),
            'W3': self.W3.copy(), 'b3': self.b3.copy(),
        }

    def set_params(self, params):
        self.W1 = params['W1'].copy()
        self.b1 = params['b1'].copy()
        self.W2 = params['W2'].copy()
        self.b2 = params['b2'].copy()
        self.W3 = params['W3'].copy()
        self.b3 = params['b3'].copy()


# --------------- RL Bot ---------------

class RLBot:
    """Reinforcement-learning checkers bot.

    Uses TD(0) learning with a neural-network value function.
    The value is from white's perspective: +1 = white wins, -1 = black wins.
    """

    def __init__(self, policy_path=None, lr=0.001, epsilon=0.1, gamma=0.99):
        self.net = NeuralNet()
        self.lr = lr
        self.epsilon = epsilon
        self.gamma = gamma
        if policy_path and os.path.exists(policy_path):
            self.load(policy_path)

    # ---------- evaluation ----------

    def evaluate(self, bstr):
        """Return value in [-1, 1] from white's perspective."""
        features = extract_features(bstr)
        val, _ = self.net.forward(features)
        return val

    # ---------- move generation ----------

    @staticmethod
    def _generate_successors(bstr, turn):
        """Return list of board strings reachable in one move."""
        import board as bd
        temp = bd.Board(bstr)
        successors = []
        for i in range(8):
            for j in range(8):
                for d in ['L', 'R', '-L', '-R']:
                    if temp.moveAllowed(i, j, d, turn):
                        temp.move(i, j, d, turn)
                        successors.append(temp.getString())
                        temp.editBoard(bstr)
        return successors

    def choose_move(self, bstr, turn):
        """Epsilon-greedy move selection. Returns the chosen successor board string."""
        successors = self._generate_successors(bstr, turn)
        if not successors:
            return bstr  # no moves

        # Epsilon-greedy
        if np.random.random() < self.epsilon:
            return successors[np.random.randint(len(successors))]

        best_val = None
        best_move = None
        for s in successors:
            v = self.evaluate(s)
            # White maximises, black minimises
            if best_val is None:
                best_val = v
                best_move = s
            elif turn == 1 and v > best_val:
                best_val = v
                best_move = s
            elif turn == -1 and v < best_val:
                best_val = v
                best_move = s
        return best_move

    def best_move(self, bstr, turn):
        """Greedy (no exploration) move selection for actual play."""
        successors = self._generate_successors(bstr, turn)
        if not successors:
            return bstr

        best_val = None
        best_move = None
        for s in successors:
            v = self.evaluate(s)
            if best_val is None:
                best_val = v
                best_move = s
            elif turn == 1 and v > best_val:
                best_val = v
                best_move = s
            elif turn == -1 and v < best_val:
                best_val = v
                best_move = s
        return best_move

    # ---------- training step ----------

    def td_update(self, bstr, next_bstr, reward, done):
        """Perform one TD(0) update: V(s) <- V(s) + lr * (reward + gamma*V(s') - V(s))."""
        features = extract_features(bstr)
        val, cache = self.net.forward(features)

        if done:
            target = reward
        else:
            next_val = self.evaluate(next_bstr)
            target = reward + self.gamma * next_val

        td_error = target - val
        grad_out = np.array([[td_error]], dtype=np.float32)
        grads = self.net.backward(cache, grad_out)
        self.net.update(grads, self.lr)
        return td_error

    # ---------- persistence ----------

    def save(self, path=None):
        if path is None:
            path = DEFAULT_POLICY
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.net.get_params(), f)

    def load(self, path=None):
        if path is None:
            path = DEFAULT_POLICY
        with open(path, 'rb') as f:
            params = pickle.load(f)
        self.net.set_params(params)


# ---------- convenience for runner.py ----------

def rl_bot_play(bstr, turn, policy_path=None):
    """Drop-in replacement matching bot.botPlay signature style.

    Returns the best successor board string.
    """
    if policy_path is None:
        policy_path = DEFAULT_POLICY
    bot = RLBot(policy_path=policy_path, epsilon=0.0)
    return bot.best_move(bstr, turn)
