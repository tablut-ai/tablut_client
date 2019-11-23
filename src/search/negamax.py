from math import inf
from copy import deepcopy
from search.cache import LRUCache, HistoryHeuristic
from heuristic.eval_obj import HeuristicObj
from game.game_obj import GameObj

class Search:

    def __init__(self, color):
        self.tt = LRUCache()
        self.hh = HistoryHeuristic()
        self.game = GameObj(color)
        self.heuristic = HeuristicObj()
        self.eval_fn = self.heuristic.evaluation_fn

    def start(self, state):
        self.depth = 2
        α = -inf
        β = inf
        move = self.negamax(state, self.depth, α, β, self.game.color)
        return move

    def set_tt(self, state, val, depth, flag):
        entry = {}
        entry["val"] = val
        entry["depth"] = depth
        entry["flag"] = flag
        self.tt[state] = entry

    def negamax(self, state, depth, α, β, color):

        alphaOrig = α

        
        from_tt = self.tt.get(state) 
        if from_tt != None and from_tt["depth"] >= depth:
            if from_tt["flag"] == 0:
                return from_tt["val"]
            elif from_tt["flag"] == -1:
                α = max(α, from_tt["val"])
            elif from_tt["flag"] == 1:
                β = min(β, from_tt["val"])
            if α >= β:
                return from_tt["val"]
        

        terminal = self.game.terminal_test(state, color)
        if terminal != 0:
            return terminal * (1e8)
        if depth == 0:
            return self.eval_fn(state, color)

        moves = self.game.actions(state)
        # moves = orderMoves(moves) 
        v = -inf
        for m in moves:
            next_state = self.game.result(deepcopy(state), m)
            child_v = self.negamax(next_state, depth-1, -β, -α, -color)

            if -child_v > v:
                v = -child_v
                best_move = m

            α = max(α, v)

            if α >= β:
                break
        
        if v >= β:
            self.set_tt(state, v, depth, -1)
        elif v <= alphaOrig:
            self.set_tt(state, v, depth, 1)
        else:
            self.set_tt(state, v, depth, 0)
        
        if depth == self.depth:
            return best_move

        return v

