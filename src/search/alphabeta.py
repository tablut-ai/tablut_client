import numpy as np
from math import inf

def start_search(game, state, turn, eval_fn):
    depth=2
    return alphabeta_cutoff_search(game, state, turn, depth, eval_fn)

def alphabeta_cutoff_search(game, state, turn, max_depth, eval_fn):

    def max_value(game, state, turn, move, alpha, beta, depth):
        terminal = game.terminal_test(state, turn, move)
        if depth > max_depth or terminal != 0:
            return eval_fn(state, turn) + terminal
        v = -inf
        for a in game.actions(state, turn):
            v = max(v, min_value(game, game.result(np.copy(state), a, turn), turn, move,
                            alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(game, state, turn, move, alpha, beta, depth):
        terminal = game.terminal_test(state, turn, move)
        if depth > max_depth or terminal != 0:
            return eval_fn(state, turn) + terminal
        v = inf
        for a in game.actions(state, turn):
            v = min(v, max_value(game, game.result(np.copy(state), a, turn), turn, move,
                            alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -inf
    beta = inf
    best_action = None
    for a in game.actions(state, turn):
        v = min_value(game, game.result(np.copy(state), a, turn), turn, a, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

