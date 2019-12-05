import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from search.negamax import Search

def fitness_fn(white_population, black_population, timeout):
    for w in white_population:
        for b in black_population:
            w_player = Search(1, timeout = timeout, weights =w[0])
            b_player = Search(-1, timeout = timeout, weights = b[0])

            result = fight(w_player, b_player)
            if result == 1:
                w[1] += 1
                b[1] -= 1
            if result == -1:
                w[1] -= 1
                b[1] += 1

def fight(w, b):
    past_states = dict()
    state = [
        [ 0,  0,  0, -1, -1, -1,  0,  0,  0],
        [ 0,  0,  0,  0, -1,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  1,  0,  0,  0,  0],
        [-1,  0,  0,  0,  1,  0,  0,  0, -1], 
        [-1, -1,  1,  1,  2,  1,  1, -1, -1], 
        [-1,  0,  0,  0,  1,  0,  0,  0, -1], 
        [ 0,  0,  0,  0,  1,  0,  0,  0,  0], 
        [ 0,  0,  0,  0, -1,  0,  0,  0,  0], 
        [ 0,  0,  0, -1, -1, -1,  0,  0,  0]]

    color = 1
    pawns, hash_ = w.game.compute_state(state)

    print("\n\n==========        " + u'\u2694'+ u'\u2694'+ u'\u2694' + "   FIGHT   " + u'\u2694'+ u'\u2694'+ u'\u2694' + "        ==========")
    print("White player weights:", w.heuristic.weights, "\n black player weights:", b.heuristic.weights)

    while True:
        move = w.start(state)
        state, hash_, pawns, terminal = w.game.update_state(state, hash_, pawns, move, color)
        print("========== WHITE MOVE: ", move, "\n")
        print_state(state)
        if terminal: # ww
            print("\n========== WHITE WIN ==========")
            return 1
        
        color = -color

        move = b.start(state)
        state, hash_, pawns, terminal = b.game.update_state(state, hash_, pawns, move, color)
        print("========== BLACK MOVE: ", move, "\n")
        print_state(state)
        if terminal: # bw
            print("\n========== BLACK WIN ==========")
            return -1

        color = -color

        try: 
            past_states[hash_]
            print("\n========== DRAW ==========") # draw
            return 0
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

if __name__ == "__main__": 
    timeout = float('infinity')
    w_player = Search( 1, timeout = timeout, weights = [10, -1, 1, 1, 1, -2, -4, 2, 5, 1, 1])
    b_player = Search(-1, timeout = timeout, weights = [10, -1, 1, 1, 1, -2, -4, 2, 5, 1, 1])

    fight(w_player, b_player)