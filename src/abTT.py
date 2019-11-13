LOWERBOUND, EXACT, UPPERBOUND = -1,0,1
inf = float('infinity')

def abTT(state, depth, game, best_action, alpha, beta, best_score, tt=None):

    if tt != None:

        assert best_action in game.actions(state)
        tt.store(game=state, depth=depth, value = best_score ,
                 move= best_action,
                 flag = UPPERBOUND if (best_action <= alpha) else (
                        LOWERBOUND if (best_score >= beta) else EXACT))

