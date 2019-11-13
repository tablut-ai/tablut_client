from collections import namedtuple
import random
import itertools
import copy
from math import inf
import numpy as np
from aima.utils import argmax, vector_add, MCT_Node, ucb

#================ALPHA BETA ALGORITHM=======================================
def alphabeta_cutoff_search(game, state, turn, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    player = turn
    # Functions used by alphabeta

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

#=================================================================================

