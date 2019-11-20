from math import inf
from copy import deepcopy
from search.cache import LRUCache

class Search:
    def __init__(self):
        self.tt = LRUCache()

    def start(self, game, state, turn, heuristic):
        depth=2
        if turn == 1:
            return self.alphabeta_cutoff_search(game, state, turn, depth, eval_fn = heuristic.white_MAX_evaluation_fn)
        else:
            return self.alphabeta_cutoff_search(game, state, turn, depth, eval_fn = heuristic.black_MAX_evaluation_fn)

    def set_tt(self, state, val, depth, flag):
        entry = {}
        entry["val"] = val
        entry["depth"] = depth
        entry["flag"] = flag
        self.tt[state] = entry

    def alphabeta_cutoff_search(self, game, state, turn, d=4, cutoff_test=None, eval_fn=None, timeout = 1000):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""
        maximizer = turn
        minimizer = - turn
        # Functions used by alphabeta

        def max_value(state, game, alpha, beta, depth, maximizer, minimizer, move):
            from_tt = self.tt.get(state) 
            if from_tt != None and from_tt["depth"] >= depth:
                if from_tt["flag"] == 0: #exact
                    return from_tt["val"]
                elif from_tt["flag"] == -1: #lowerbound
                    alpha = max(alpha, from_tt["val"])
                elif from_tt["flag"] == 1: #upperbound
                    beta = min(beta, from_tt["val"])
                if alpha >= beta:
                    return from_tt["val"]

            terminal = 0
            if game.terminal_test(state, minimizer, move):
                terminal = inf
                return eval_fn(game, state, minimizer, terminal)
        
            if game.terminal_test(state, maximizer, move):
                terminal = -inf
                return eval_fn(game, state, minimizer, terminal)

            if cutoff_test(100, depth):
                return eval_fn(game, state, minimizer, terminal)

            v = -inf
            for a in game.actions(state, maximizer):
                v = max(v, min_value(game.result(deepcopy(state), a, maximizer),  game,
                                    alpha, beta, depth + 1, maximizer, minimizer, move))
                if v >= beta:
                    self.set_tt(state, v, depth, -1)
                    return v
                alpha = max(alpha, v)

            self.set_tt(state, v, depth, 0)
            return v

        def min_value(state, game, alpha, beta, depth, maximizer, minimizer, move):
            from_tt = self.tt.get(state) 
            if from_tt != None and from_tt["depth"] >= depth:
                if from_tt["flag"] == 0: #exact
                    return from_tt["val"]
                elif from_tt["flag"] == -1: #lowerbound
                    alpha = max(alpha, from_tt["val"])
                elif from_tt["flag"] == 1: #upperbound
                    beta = min(beta, from_tt["val"])
                if alpha >= beta:  ## IDK
                    return from_tt["val"]
        
            terminal = 0
            if game.terminal_test(state, maximizer, move):
                terminal = inf
                return eval_fn(game, state, maximizer, terminal)

            if game.terminal_test(state, minimizer, move):
                terminal = -inf
                return eval_fn(game, state, maximizer, terminal)

            if cutoff_test(100, depth):
                return eval_fn(game, state, maximizer, terminal)

            v = inf
            for a in game.actions(state, minimizer):
                v = min(v, max_value(game.result(deepcopy(state), a, minimizer), game,
                                    alpha, beta, depth + 1, maximizer, minimizer, move))
                if v <= alpha:
                    self.set_tt(state, v, depth, 1)
                    return v
                beta = min(beta, v)

            self.set_tt(state, v, depth, 0)
            return v

        # Body of alphabeta_cutoff_search starts here:
        # The default test cuts off at depth d or at timeout
        cutoff_test = (cutoff_test or (lambda time, depth: depth > d or time > timeout))
        eval_fn = eval_fn 
        best_score = -inf
        beta = inf
        best_action = None

        for a in game.actions(state, maximizer):
            v = min_value(game.result(deepcopy(state),a, maximizer), game, best_score, beta, 1, maximizer, minimizer, a)
            print(v, a)
            if v > best_score:
                best_score = v
                best_action = a
        print("Best_Score", best_score, " of action ", best_action)
        return best_action

