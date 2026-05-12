# TD-Leaf(λ) with Neural Network Evaluation for Checkers

**Abstract** — We present LearnBot, a self-learning checkers agent that combines alpha-beta tree search with a small multilayer perceptron (MLP) trained via the TD-Leaf(λ) algorithm. The agent acquires positional knowledge entirely through self-play, without hand-crafted heuristics. We describe the board representation, network architecture, update rule, search integration, and curriculum training schedule. Experimental results from automated self-play confirm that the agent progressively improves through experience.

---

## 1. Introduction

The game of checkers (English draughts) is a two-player, zero-sum, perfect-information board game played on an 8×8 grid. Despite being solved optimally by Chinook [1], checkers remains a canonical testbed for reinforcement learning research because its branching factor and game length are representative of a wide class of sequential decision problems.

Classical game-playing agents rely on manually engineered evaluation functions, which are costly to design and brittle outside the scenarios the designer anticipated. A more principled alternative is to learn the evaluation function from experience via temporal-difference (TD) learning [2].

TD-Leaf(λ), introduced by Baxter et al. [3] for chess, extends plain TD learning to tree-search agents. Rather than applying TD updates to the root position, it applies them to the *leaf* node reached by the search. This single change dramatically stabilises training because the search corrects systematic errors in the raw network output before they propagate through the update.

This paper documents the design and implementation of LearnBot, which realises TD-Leaf(λ) on top of a minimax alpha-beta search using a small MLP as the value function.

---

## 2. Problem Formulation

### 2.1 Game State

A board position is represented as a string $s \in \Sigma^{64}$, where each character $s_i \in \{{\tt 0, w, W, b, B}\}$ encodes one of the 64 squares. The alphabet has the semantics:

| Symbol | Meaning          |
|--------|------------------|
| `0`    | Empty square     |
| `w`    | White man        |
| `W`    | White king       |
| `b`    | Black man        |
| `B`    | Black king       |

The turn indicator $\tau \in \{+1, -1\}$ encodes the side to move (+1 = white, −1 = black).

### 2.2 Objective

We seek a parameterised value function $V_\theta : \mathcal{S} \times \{+1,-1\} \to [-1, 1]$ such that $V_\theta(s, \tau) \approx \mathbb{E}[\text{outcome} \mid s, \tau]$, where the outcome is $+1$ (white wins), $-1$ (black wins), or $0$ (draw).

---

## 3. Board Encoding

The raw board string is converted into a 65-dimensional real-valued feature vector $\mathbf{x} \in \mathbb{R}^{65}$:

$$x_i = \begin{cases}
0.0   & s_i = {\tt 0} \\
+0.5  & s_i = {\tt w} \\
+1.0  & s_i = {\tt W} \\
-0.5  & s_i = {\tt b} \\
-1.0  & s_i = {\tt B}
\end{cases}, \quad i = 1,\ldots,64$$

$$x_{65} = 0.5\,\tau$$

The sign convention makes white's advantage positive and black's advantage negative, which is consistent with the minimax orientation of the search. Kings are given twice the weight of men, reflecting their greater mobility. The turn feature $x_{65}$ provides the network with information about tempo.

---

## 4. Neural Network Architecture

The value function is realised by a three-layer MLP with $\tanh$ activations:

$$\mathbf{a}^{(1)} = \tanh\!\left(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}\right), \quad \mathbf{a}^{(1)} \in \mathbb{R}^{128}$$

$$\mathbf{a}^{(2)} = \tanh\!\left(\mathbf{W}^{(2)}\mathbf{a}^{(1)} + \mathbf{b}^{(2)}\right), \quad \mathbf{a}^{(2)} \in \mathbb{R}^{64}$$

$$V_\theta(\mathbf{x}) = \tanh\!\left(\mathbf{W}^{(3)}\mathbf{a}^{(2)} + \mathbf{b}^{(3)}\right) \in [-1, 1]$$

**Architecture summary:**

| Layer | Input dim | Output dim | Activation |
|-------|-----------|------------|------------|
| 1     | 65        | 128        | tanh       |
| 2     | 128       | 64         | tanh       |
| 3     | 64        | 1          | tanh       |

**Total parameters:** $65 \times 128 + 128 + 128 \times 64 + 64 + 64 \times 1 + 1 = 16{,}833$

**Weight initialisation:** Glorot uniform [4] for each weight matrix:

$$W^{(l)}_{ij} \sim \mathcal{U}\!\left(-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}},\; +\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right)$$

Biases are initialised to zero. All weights are stored in `float32`.

---

## 5. Alpha-Beta Search

At inference time, the agent selects a move by running **negamax alpha-beta** search to depth $d$, using $V_\theta$ as the leaf evaluator.

### 5.1 Algorithm

```
function alphabeta(s, d, α, β, τ):
    if terminal(s, τ):   return utility(s, τ)
    if d = 0:            return V_θ(s, τ)
    if τ = +1:
        v* ← −∞
        for each successor s' of s under τ:
            v ← alphabeta(s', d−1, α, β, −τ)
            v* ← max(v*, v)
            α  ← max(α, v*)
            if β ≤ α: break          // β-cut
        return v*
    else: (symmetric min-node case)
```

The function returns both the best leaf value and the board string of the best immediate successor, the latter being the move the agent actually plays.

### 5.2 Terminal Conditions

A position is terminal if (a) one side has no pieces remaining, or (b) the side to move has no legal moves. The utility is $+1$ if white wins, $-1$ if black wins, and $0$ for a draw.

### 5.3 Stochastic Exploration (Difficulty Scaling)

During evaluation mode a Gaussian noise term $\epsilon \sim \mathcal{N}(0, \sigma^2)$ is added to each leaf score. The standard deviation $\sigma$ and search depth $d$ are jointly controlled by a difficulty parameter $k \in \{1,\ldots,10\}$:

| $k$ | $d$ | $\sigma$ |
|-----|-----|----------|
| 1   | 1   | 0.80     |
| 2   | 1   | 0.50     |
| 3   | 2   | 0.35     |
| 4   | 2   | 0.18     |
| 5   | 3   | 0.12     |
| 6   | 3   | 0.06     |
| 7   | 4   | 0.04     |
| 8   | 4   | 0.01     |
| 9   | 5   | 0.005    |
| 10  | 6   | 0.00     |

---

## 6. TD-Leaf(λ) Learning

### 6.1 Background: TD Learning

In temporal-difference learning, the weight update at time $t$ is:

$$\Delta\theta_t = \alpha \cdot \delta_t \cdot \nabla_\theta V_\theta(s_t)$$

where the TD error is $\delta_t = V_\theta(s_{t+1}) - V_\theta(s_t)$.

Plain TD applied to a tree-search agent is unstable because $V_\theta(s_t)$ is the *root* evaluation, which can fluctuate due to the search's horizon effect.

### 6.2 The Leaf Substitution

TD-Leaf(λ) [3] replaces root values with **leaf values** obtained by search:

$$v^*_t = \text{alphabeta}(s_t,\; d,\; -\infty,\; +\infty,\; \tau_t)$$

The TD error becomes:

$$\delta_t = v^*_{t+1} - v^*_t$$

Because $v^*_t$ is the evaluation of a deeply searched position, it is a much more stable estimate of the true value than the raw network output at the root. This is the key insight: the search acts as a *variance reducer* for the TD target.

### 6.3 Eligibility Traces

To propagate credit over multiple time steps, **accumulating eligibility traces** $\mathbf{e}_t$ are maintained for every parameter tensor $\theta_k$:

$$\mathbf{e}_t^{(k)} = \lambda \cdot \mathbf{e}_{t-1}^{(k)} + \nabla_\theta V_\theta(s_t)\Big|_{\theta_k}$$

where $\lambda \in [0, 1]$ is the trace decay. The weight update at each step is:

$$\theta_k \leftarrow \theta_k + \alpha \cdot \delta_t \cdot \mathbf{e}_t^{(k)}$$

Traces are initialised to zero at the start of each game and never carried across games.

### 6.4 Gradient Computation

The gradient $\nabla_\theta V_\theta(s_t)$ is computed analytically via backpropagation through the MLP. Let $v = V_\theta(\mathbf{x})$. Defining the output delta:

$$g_3 = 1 - v^2$$

The layer-wise backpropagation gives:

$$\mathbf{g}_2 = (g_3 \cdot \mathbf{W}^{(3)\top}) \odot (1 - \mathbf{a}^{(2)} \odot \mathbf{a}^{(2)})$$

$$\mathbf{g}_1 = (\mathbf{g}_2 \cdot \mathbf{W}^{(2)\top}) \odot (1 - \mathbf{a}^{(1)} \odot \mathbf{a}^{(1)})$$

The parameter gradients are:

$$\nabla_{\mathbf{W}^{(1)}} V = \mathbf{x} \otimes \mathbf{g}_1, \quad \nabla_{\mathbf{b}^{(1)}} V = \mathbf{g}_1$$

$$\nabla_{\mathbf{W}^{(2)}} V = \mathbf{a}^{(1)} \otimes \mathbf{g}_2, \quad \nabla_{\mathbf{b}^{(2)}} V = \mathbf{g}_2$$

$$\nabla_{\mathbf{W}^{(3)}} V = \mathbf{a}^{(2)} \otimes g_3, \quad \nabla_{\mathbf{b}^{(3)}} V = g_3$$

where $\otimes$ denotes the outer product and $\odot$ element-wise multiplication.

### 6.5 Complete Update Rule (Per Step)

Given the current position $s_t$, the next leaf value $v^*_{t+1}$, and the current eligibility traces $\mathbf{e}$:

1. Forward pass: $v^*_t, \text{cache} \leftarrow \text{alphabeta}(s_t, d, \tau_t)$
2. Compute TD error: $\delta_t = v^*_{t+1} - v^*_t$
3. Compute gradient: $\nabla V \leftarrow \text{backprop}(\text{cache})$
4. Update traces: $\mathbf{e} \leftarrow \lambda \mathbf{e} + \nabla V$
5. Update weights: $\theta \leftarrow \theta + \alpha \cdot \delta_t \cdot \mathbf{e}$

### 6.6 Terminal Step

At game end, the terminal utility $r \in \{-1, 0, +1\}$ is used as the final TD target:

$$\theta \leftarrow \theta + \alpha \cdot (r - v^*_T) \cdot \mathbf{e}_T$$

---

## 7. Training Procedures

### 7.1 Self-Play Training

In the primary training mode, both sides are controlled by the same network at a fixed search depth $d_{\text{train}}$. The algorithm proceeds as follows:

```
for game g = 1 … N:
    reset traces; s ← s₀; τ ← +1; quiet ← 0
    while not terminal(s, τ) and moves ≤ 320:
        v*, s'   ← alphabeta(s,  d_train, τ)
        v*_next, ← alphabeta(s', d_train, −τ)
        TD-Leaf step(s, τ, v*_next)
        if move_has_capture_or_promotion(s, s'):
            quiet ← 0
        else:
            quiet ← quiet + 1
        s ← s'; τ ← −τ
        if quiet ≥ 100: declare draw; break
    TD-Leaf terminal step(s, τ, utility(s))
```

**Draw conditions:** (a) 100 consecutive moves without capture or promotion (analogous to the fifty-move rule in chess), or (b) the 320-move hard limit. In both cases the terminal target is $r = 0$.

### 7.2 Curriculum Training

To accelerate learning, a **curriculum** can be specified as an ordered list of opponent phases $\{d_1, d_2, \ldots, d_K\}$. The total budget of $N$ games is divided equally among phases. Available phase types:

| Phase code | Opponent                             |
|------------|--------------------------------------|
| `0`        | Self (TD-Leaf bot vs. itself)        |
| `-1`       | Random                               |
| `1`–`10`   | Minimax at depth $d$ (no learning)   |

Within each non-self phase the learning agent always plays as White. The TD update is still computed from the perspective of the learning agent, even when the opponent's moves are selected by an external policy.

**Rationale:** Starting against weaker opponents (random or shallow minimax) provides a dense reward signal during early training. Progressing to deeper opponents gradually raises the level of competition, avoiding premature convergence to simple strategies.

---

## 8. Online Learning During Play

In addition to offline self-play training, LearnBot supports **online learning** during live games. After every move made in an interactive session, a single TD-Leaf step is executed using the leaf value of the opponent's best reply as the target. The learning rate used during online play ($\alpha_{\text{online}} = 0.0002$, $\lambda = 0.6$) is lower than during self-play to avoid destabilising previously learned knowledge. Weights are persisted to disk after each game.

---

## 9. Hyperparameters

| Parameter                    | Symbol         | Default value |
|------------------------------|----------------|---------------|
| Self-play learning rate      | $\alpha$       | $5 \times 10^{-4}$ |
| Online learning rate         | $\alpha_{\text{online}}$ | $2 \times 10^{-4}$ |
| Trace decay                  | $\lambda$      | 0.7 (offline), 0.6 (online) |
| Training depth               | $d_{\text{train}}$ | 2         |
| Checkpoint interval          | —              | every 25 games |
| Draw threshold (quiet moves) | —              | 100 moves     |
| Move limit per game          | —              | 320 moves     |

---

## 10. Convergence and Stability Considerations

**Fixed-point perspective.** The TD-Leaf update drives $V_\theta$ toward the fixed point where $v^*_t \approx v^*_{t+1}$ along the trajectory induced by the current policy. This fixed point corresponds to a consistent valuation of positions at search depth $d$.

**Non-stationarity.** Because the training data distribution changes as the policy improves, TD-Leaf for games is a non-stationary learning problem. The use of eligibility traces with $\lambda < 1$ limits the temporal horizon over which credit is assigned, which partially mitigates the instability arising from non-stationarity.

**Search as variance reduction.** The leaf substitution ensures that $v^*_t$ is the value of a position at least $d$ plies deep in the game tree. The alpha-beta search implicitly performs a one-step lookahead correction: if the network underestimates a position, the search will prefer moves that are good but undervalued, and the leaf values will be more accurate than the root evaluation. This is the mechanism by which TD-Leaf is more stable than plain TD(λ) for game-playing agents.

---

## 11. Comparison with Related Work

| Method              | Value function       | Search | Learning signal         |
|---------------------|----------------------|--------|-------------------------|
| TD-Gammon [2]       | MLP (backgammon)     | None   | TD(λ) on root           |
| KnightCap [3]       | Linear + MLP (chess) | α-β    | TD-Leaf(λ)              |
| AlphaGo Zero [5]    | ResNet (Go)          | MCTS   | Policy + value gradient |
| **LearnBot (ours)** | MLP 65→128→64→1      | α-β    | TD-Leaf(λ)              |

LearnBot is closest in spirit to KnightCap. The primary differences are (a) the simpler board encoding (no hand-crafted features), (b) the smaller network (16K vs. hundreds of thousands of parameters), and (c) the addition of a curriculum training schedule.

---

## 12. Conclusions

We have described LearnBot, a checkers agent that learns to play entirely from self-play experience using TD-Leaf(λ). The combination of a small MLP value function, alpha-beta tree search, and temporal-difference learning with eligibility traces produces an agent that improves progressively without any domain-specific knowledge beyond the rules of the game. The curriculum training schedule provides a practical mechanism for bootstrapping learning from weaker opponents.

Future work could investigate (a) convolutional network architectures that exploit the spatial structure of the board, (b) Monte Carlo Tree Search as an alternative to alpha-beta, and (c) population-based training to reduce sensitivity to hyperparameters.

---

## References

[1] Schaeffer, J., Burch, N., Bjornsson, Y., Kishimoto, A., Müller, M., Lake, R., Lu, P., & Sutphen, S. (2007). Checkers is solved. *Science*, 317(5844), 1518–1522.

[2] Tesauro, G. (1995). Temporal difference learning and TD-Gammon. *Communications of the ACM*, 38(3), 58–68.

[3] Baxter, J., Tridgell, A., & Weaver, L. (1998). Experiments in parameter learning using temporal differences. *ICCA Journal*, 21(2), 84–99.

[4] Glorot, X., & Bengio, Y. (2010). Understanding the difficulty of training deep feedforward neural networks. In *Proceedings of AISTATS*, 249–256.

[5] Silver, D., Schrittwieser, J., Simonyan, K., et al. (2017). Mastering the game of Go without human knowledge. *Nature*, 550, 354–359.
