import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from search.negamax import Search
from game.game_obj import GameObj
from genotype import Genotype

def main():
    timeout = 59.5
    GA = Genotype(N = 2)
    GA.initialize_population()
    g1 = GA.population[0]
    g2 = GA.population[1]
    w = Search(1, timeout)
    b = Search(-1, timeout)
    start(w, b)

def start(w, b):
    wgame, bgame = GameObj(1), GameObj(-1)
    past_states = dict()
    state = [
        [ 0,  0,  0, -1, -1, -1,  0,  0,  0],
        [ 0,  0,  0,  0, -1,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  1,  0,  0,  0,  0],
        [-1,  0,  0,  0,  1,  0,  0,  0, -1], 
        [-1, -1,  1,  1,  0,  1,  1, -1, -1], 
        [-1,  0,  0,  0,  1,  0,  2,  0, -1], 
        [ 0,  0,  0,  0,  1,  0,  0,  0,  0], 
        [ 0,  0,  0,  0, -1,  0,  0,  0,  0], 
        [ 0,  0,  0, -1, -1, -1,  0,  0,  0]]
    color = 1
    pawns, hash_ = wgame.compute_state(state)

    print("==========        " + u'\u2694'+ u'\u2694'+ u'\u2694' + "   FIGHT   " + u'\u2694'+ u'\u2694'+ u'\u2694' + "        ==========")
    while True:
        move = w.start(state)
        state, hash_, pawns, terminal = wgame.update_state(state, hash_, pawns, move, color)
        print("========== WHITE MOVE: ", move, "\n")
        print_state(state)
        if terminal: # ww
            print("========== WHITE WIN ==========")
            break
        color = -color

        move = b.start(state)
        state, hash_, pawns, terminal = bgame.update_state(state, hash_, pawns, move, color)
        print("========== BLACK MOVE: ", move, "\n")
        print_state(state)
        if terminal: # bw
            print("========== BLACK WIN ==========")
            break
        color = -color

        try: 
            past_states[hash_]
            print("========== DRAW ==========") # draw
            break
        except: past_states[hash_] = 1

def print_state(state):
    for r in range(9):
        u = ""
        for i in range(9):
            c = state[r][i]
            if c == -1: 
                u+=u'\u2999'+u'\u25cb'+" "
            elif c == 1: 
                u+=u'\u2999'+u'\u25cf'+" "
            elif c == 2: 
                u+=u'\u2999'+u'\u2654'+" "
            else: 
                if r == 4 and i == 4: u+=u'\u2999'+"x "
                else: u+=u'\u2999'+"  "
        print(r," ", u+u'\u2999', "\n")
    print("    ", "  ".join(str(x) for x in range(9)))

if __name__ == '__main__': main()