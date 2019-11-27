from math import inf
from time import time
from search.cache import LRUCache, HistoryHeuristic
from heuristic.eval_obj import HeuristicObj
from game.game_obj import GameObj

class Search:

    def __init__(self, color, timeout = 59.5): 
        self.tt = LRUCache()
        self.hh = HistoryHeuristic()

        self.game = GameObj(color)
        self.heuristic = HeuristicObj()
        self.eval_fn = self.heuristic.evaluation_fn

        self.started = 0
        self.TIMEOUT = timeout

    def start(self, state):
        self.depth = 3
        α = -inf
        β = inf
        self.started = time()
        pawns, hash_ = self.game.compute_state(state)
        move = self.negamax(state, self.depth, α, β, self.game.color, pawns, hash_, False)
        return move

    def negamax(self, state, depth, α, β, color, pawns, hash_, terminal):
        alphaOrig = α
        from_tt = self.tt.get(hash_) 
        if from_tt != None and from_tt["depth"] >= depth:
            if from_tt["flag"] == 0:
                return from_tt["move"] if depth == self.depth else from_tt["val"]
            elif from_tt["flag"] == -1:
                α = max(α, from_tt["val"])
            elif from_tt["flag"] == 1:
                β = min(β, from_tt["val"])
            if α >= β:
                return from_tt["move"] if depth == self.depth else from_tt["val"]

        if terminal or depth == 0:
            return None if depth == self.depth else self.eval_fn(state, color, terminal, pawns) - depth

        moves = self.game.actions(state, color, pawns)
        moves.sort(key = self.orderMoves)
        
        best_value = -inf
        best_move = None
        for child_move in moves:
            if time() - self.started >= self.TIMEOUT:
                print("timed out")
                break

            next_state, next_hash, next_pawns, terminal = self.game.update_state(state, hash_, pawns, child_move, color)
            child_value = -self.negamax(next_state, depth-1, -β, -α, -color, next_pawns, next_hash, terminal)

            if child_value >= best_value:
                best_value = child_value
                best_move = child_move

            if α < child_value:
                α = child_value
                if depth == self.depth:
                    best_move = child_move
                if α >= β:
                    break
        
        if best_value >= β:
            self.set_tt(hash_, best_value, depth, best_move, -1)
        elif best_value <= alphaOrig:
            self.set_tt(hash_, best_value, depth, best_move, 1)
        else:
            self.set_tt(hash_, best_value, depth, best_move, 0)

        if color == self.game.color and best_move != None:
            self.hh[best_move] = 2**depth
        
        return best_move if depth == self.depth else best_value

    def set_tt(self, state, val, depth, move, flag):
        entry = {
            "val" : val,
            "depth" : depth,
            "move" : move,
            "flag" : flag
        }
        self.tt[state] = entry

    def orderMoves(self, move):
        return self.hh.get(move)