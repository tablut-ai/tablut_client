from math import inf
from time import time
from search.cache import LRUCache, HistoryHeuristic
from heuristic.eval_obj import HeuristicObj
from game.game_obj import GameObj
from multiprocessing import Manager
from pathos.multiprocessing import ProcessingPool as Pool, cpu_count 
from pathos.core import getpid

class Search:

    def __init__(self, color, timeout = 59.5, depth=4): 
        self.TIMEOUT = timeout
        self.DEPTH = depth

        manager = Manager()

        self.tt = LRUCache()
        self.hh = HistoryHeuristic()

        self.game = GameObj(color)
        self.heuristic = HeuristicObj()
        self.eval_fn = self.heuristic.evaluation_fn
        
        self.inq = manager.Queue()
        self.outq = manager.Queue()
        for i in range(cpu_count()):
            Pool().apipe(self.process_search, depth, color)

    def start(self, state):
        started = time()
        #self.fd = open(str(self.started)+".data", "w")

        α = -inf
        β = inf
        pawns, hash_ = self.game.compute_state(state)

        # YBWC
        moves = self.game.actions(state, self.game.color, pawns)
        moves.sort(key = self.order_moves)
        first_move = moves.pop(0)
        self.inq.put((state, hash_, pawns, first_move, α, β, started))

        α = self.outq.get(block=True)[0]
        best = [α, first_move]

        for move in moves:
            self.inq.put((state, hash_, pawns, move, α, β, started))
        
        for i in range(len(moves)):
            recvd = self.outq.get(block=True)
            if best[0] < recvd[0]:
                best = recvd

        #self.fd.close()
        print("\n\n\n", best)
        return best[1]

    def process_search(self, depth, color):
        while True: 
            state, hash_, pawns, move, α, β, started = self.inq.get(block=True)
            print(move, len(self.tt.od), "=========", getpid())
            try:
                next_state, next_hash, next_pawns, terminal = self.game.update_state(state, hash_, pawns, move, color)
                child_value = -self.negamax(next_state, depth-1, -β, -α, -color, next_pawns, next_hash, terminal, started)
                self.outq.put((child_value, move))
            except Exception as e:
                print(e) 

    def negamax(self, state, depth, α, β, color, pawns, hash_, terminal, started):
        alphaOrig = α
        from_tt = self.tt.get(hash_) 
        if from_tt != None and from_tt["depth"] >= depth:
            if from_tt["flag"] == 0:
                return from_tt["val"]
            elif from_tt["flag"] == -1:
                α = max(α, from_tt["val"])
            elif from_tt["flag"] == 1:
                β = min(β, from_tt["val"])
            if α >= β:
                return from_tt["val"]

        if terminal or depth == 0:
            return self.eval_fn(state, color, terminal, pawns) - depth

        moves = self.game.actions(state, color, pawns)
        moves.sort(key = self.order_moves)

        best_value = -inf
        best_move = None
        for child_move in moves:
            #self.fd.write("  "*(self.depth-depth) + str(child_move)+"{\n")
            if time() - started >= self.TIMEOUT:
                print("timeout")
                if best_value == -inf:
                    return best_value * self.game.color * color # should be always the minimum
                break

            next_state, next_hash, next_pawns, terminal = self.game.update_state(state, hash_, pawns, child_move, color)
            child_value = -self.negamax(next_state, depth-1, -β, -α, -color, next_pawns, next_hash, terminal, started)

            if child_value >= best_value:
                best_value = child_value
                best_move = child_move

            α = max(child_value, α)
            if α >= β:
                #self.fd.write("  "*(self.depth-depth+1) + "cutoff;\n")
                break
            #self.fd.write("  "*(self.depth-depth) + "}\n")
        
        if best_value >= β:
            self.set_tt(hash_, best_value, depth, best_move, -1)
        elif best_value <= alphaOrig:
            self.set_tt(hash_, best_value, depth, best_move, 1)
        else:
            self.set_tt(hash_, best_value, depth, best_move, 0)

        if color == self.game.color and best_move != None:
            self.hh[best_move] = 2**depth
        
        return best_value

    def set_tt(self, state, val, depth, move, flag):
        entry = {
            "val" : val,
            "depth" : depth,
            "move" : move,
            "flag" : flag
        }
        self.tt[state] = entry

    def order_moves(self, move):
        stored = self.hh.get(move)
        if stored == None:
            # throne-from distance + throne-to distance
            return (4-move[0][0])*(4-move[0][0]) + (4-move[0][1]) * (4-move[0][1]) + (4-move[1][0])*(4-move[1][0]) + (4-move[1][1]) * (4-move[1][1])
        return stored        