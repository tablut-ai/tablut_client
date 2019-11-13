from collections import namedtuple
import random
import itertools
import copy
from math import inf

def alphabeta_cutoff_search(state, turn, game, d=4, eval_fn=None):
    def max_value(state, game, alpha, beta, depth, turn, move):
        
        if cutoff_test(state, depth, move):
            return eval_fn(game, state, turn)
        v = -inf
        for a in game.actions(state, turn):
            v = max(v, min_value(game.tree_result(np.copy(state), a, turn),  game,
                                 alpha, beta, depth + 1, turn, move))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, game, alpha, beta, depth, turn, move):
        if cutoff_test(state, depth, move):
            return eval_fn(game, state, turn)
        v = inf
        for a in game.actions(state, turn):
            v = min(v, max_value(game.tree_result(np.copy(state), a, turn), game,
                                 alpha, beta, depth + 1, turn, move))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth, move: depth > d or
                                         game.tree_terminal_test(state, turn, move)))
    eval_fn = eval_fn 
    #or (lambda state: game.utility(state, turn))
    best_score = -inf
    beta = inf
    best_action = None
    for a in game.actions(state, turn):
        v = min_value(game.tree_result(np.copy(state), a, turn), game, best_score, beta, 1, turn, a)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action
    


















    def max_value(state, alpha, beta, depth):
        if depth > d or game.terminal_test(state):
            return eval_fn(state, turn)
        v = -inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if depth > d or game.terminal_test(state):
            return eval_fn(state, turn)
        v = inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -inf
    beta = inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

