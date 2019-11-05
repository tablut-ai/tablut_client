from aima.search import Problem, Node, breadth_first_graph_search

class Tablut:

    def next_move(state):
        if state["turn"] == "WHITE":            
            move = {"from": "d5", "to": "d6"}
        if state["turn"] == "BLACK":           
            move = {"from": "a4", "to": "b4"}
        return move
    
    def is_valid_move(state, move):
        pass
