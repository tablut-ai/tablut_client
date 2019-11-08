import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from game import TablutGame

def main():
    game = TablutGame()
    state = {'board': [
        ['O', 'O', 'O', 'B', 'B', 'B', 'O', 'O', 'O'], 
        ['O', 'O', 'O', 'O', 'B', 'O', 'O', 'O', 'O'], 
        ['O', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'], 
        ['B', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'B'], 
        ['B', 'B', 'W', 'W', 'K', 'W', 'W', 'B', 'B'], 
        ['B', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'B'], 
        ['O', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'], 
        ['O', 'O', 'O', 'O', 'B', 'O', 'O', 'O', 'O'], 
        ['O', 'O', 'O', 'B', 'B', 'B', 'O', 'O', 'O']
        ], 'turn': 'WHITE'
    }

    assert move(game, state, {"from": [4, 5], "to": [5, 5]})
    state["turn"] = "BLACK"
    assert move(game, state, {"from": [0, 5], "to": [0, 7]})
    state["turn"] = "WHITE"
    assert False == move(game, state, {"from": [0, 5], "to": [0, 7]})

    print("====== Test completed! =====")


def move(game, state, move):
    valid = game.check_move(state, move)
    if valid:
        p = state["board"][move["from"][0]][move["from"][1]]
        state["board"][move["from"][0]][move["from"][1]] = "O"
        state["board"][move["to"][0]][move["to"][1]] = p
        return True
    return False

if __name__ == '__main__': main()