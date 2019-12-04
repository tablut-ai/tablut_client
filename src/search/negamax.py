from math import inf
from time import time
from search.cache import LRUCache, HistoryHeuristic
from heuristic.eval_obj import HeuristicObj
from game.game_obj import GameObj
from os import getpid
from multiprocessing import Process, Queue, Pipe, cpu_count
from select import select

class Search:

    def __init__(self, color, weights, timeout = 59.5, depth=3): 
        self.TIMEOUT = timeout
        self.DEPTH = depth

        self.game = GameObj(color)
        self.heuristic = HeuristicObj(weights)
        self.eval_fn = self.heuristic.evaluation_fn

        self.tt = LRUCache()
        self.hh = HistoryHeuristic()

        self.cache_pipes = []
        self.jobs_queue = Queue()
        self.moves_queue = Queue()
        
        num_worker = 1 #cpu_count()
        for i in range(num_worker):
            search_pipe, cache_pipe = Pipe(True)
            self.cache_pipes.append(cache_pipe)
            Process(target=self.search_worker, args=[self.jobs_queue, self.moves_queue, search_pipe, depth, color]).start()
            search_pipe.close() # are used by search workers

        Process(target=self.cache_worker, args=[self.cache_pipes]).start()
        for p in self.cache_pipes: p.close()
        
    def cache_worker(self, pipes):
        try:
            readers = list(map(lambda p: p.fileno(), pipes))
            while True:
                ready, _, __ = select(readers, [], [])
                for r in ready:
                    pipe = pipes[readers.index(r)]
                    req = pipe.recv()
                    if len(req) == 1:
                        pipe.send(self.tt.get(req[0]))
                    else: #2
                        self.tt[req[0]] = req[1]
        except Exception as e: print(e)

    def search_worker(self, inq, outq, cache_pipe, depth, color):
        print("[search worker ", getpid(), "] started.")
        while True: 
            try:
                state, hash_, pawns, move, α, β, started = inq.get(block=True)
                print("[search worker ", getpid(), "] processing move: ", move)
                next_state, next_hash, next_pawns, terminal = self.game.update_state(state, hash_, pawns, move, color)
                child_value = -self.negamax(next_state, depth-1, -β, -α, -color, next_pawns, next_hash, terminal, started, cache_pipe)
                outq.put((child_value, move))
            except Exception as e: print(e) 
        
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
        self.jobs_queue.put((state, hash_, pawns, first_move, α, β, started))

        α = self.moves_queue.get(block=True)[0]
        best = [α, first_move]

        for move in moves:
            self.jobs_queue.put((state, hash_, pawns, move, α, β, started))
        
        for i in range(len(moves)):
            recvd = self.moves_queue.get(block=True)
            if best[0] < recvd[0]:
                best = recvd

        #self.fd.close()
        print("\n\n\n", best)
        return best[1]

    def negamax(self, state, depth, α, β, color, pawns, hash_, terminal, started, cache_pipe):
        alphaOrig = α
        from_tt = self.get_tt(cache_pipe, hash_)
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
            child_value = -self.negamax(next_state, depth-1, -β, -α, -color, next_pawns, next_hash, terminal, started, cache_pipe)

            if child_value >= best_value:
                best_value = child_value
                best_move = child_move

            α = max(child_value, α)
            if α >= β:
                #self.fd.write("  "*(self.depth-depth+1) + "cutoff;\n")
                break
            #self.fd.write("  "*(self.depth-depth) + "}\n")
        
        if best_value >= β:
            self.set_tt(cache_pipe, hash_, best_value, depth, best_move, -1)
        elif best_value <= alphaOrig:
            self.set_tt(cache_pipe, hash_, best_value, depth, best_move, 1)
        else:
            self.set_tt(cache_pipe, hash_, best_value, depth, best_move, 0)

        if color == self.game.color and best_move != None:
            self.hh[best_move] = 2**depth
        
        return best_value

    def get_tt(self, cachep, hash_):
        return self.tt.get(hash_)
        """
        t = time()
        cachep.send([hash_])
        val = cachep.recv() 
        print("get_tt time: ", (time()-t)*1e6," us", val)
        return val
        """

    def set_tt(self, cachep, hash_, val, depth, move, flag):
        entry = {
            "val" : val,
            "depth" : depth,
            "move" : move,
            "flag" : flag
        }
        cachep.send([hash_, entry])
        self.tt[hash_] = entry

    def order_moves(self, move):
        stored = self.hh.get(move)
        if stored == None:
            # throne-from distance + throne-to distance
            return (4-move[0][0])*(4-move[0][0]) + (4-move[0][1]) * (4-move[0][1]) + (4-move[1][0])*(4-move[1][0]) + (4-move[1][1]) * (4-move[1][1])
        return stored        