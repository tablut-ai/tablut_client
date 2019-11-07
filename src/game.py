from aima.adversarial_search import alphabeta_cutoff_search
from evaluation_functions import evaluation_fn

class TablutGame:

    def __init__(self):
        self.c=0

    # invoked by the game loop
    def next_move(self, state):
        '''
        depth = 4 
        move = alphabeta_cutoff_search(state, self, depth, cutoff_test=None, eval_fn=evaluation_fn)
        return self.parse_move(move)
        '''
        if state["turn"] == "WHITE" and self.c == 0:
            self.c+=1
            return self.parse_move({
                "from": [4, 5],
                "to": [5, 5]
            })
        if state["turn"] == "BLACK" and self.c == 0:
            self.c+=1
            return self.parse_move({
                "from": [0, 5],
                "to": [0, 7]
            })
        if state["turn"] == "WHITE" and self.c == 1:
            self.c+=1
            self.check_move(state, {
                "from": [5, 5],
                "to": [0, 5]
            })
            return self.parse_move({
                "from": [5, 5],
                "to": [0, 5]
            })


        print("=====================================")

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        p = state["board"][move["from"][0]][move["from"][1]]
        state["board"][move["from"][0]][move["from"][1]] = "O"
        state["board"][move["to"][0]][move["to"][1]] = p
        raise state

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        return state["turn"]

    def parse_move(self, move):
        return {
            "from": chr(97 + move["from"][1]) + str(move["from"][0]+1),
            "to": chr(97 + move["to"][1]) + str(move["to"][0]+1)
        }

    def check_move(self, state, move):

        from_row = move["from"][0]
        from_column = move["from"][1]
        to_row = move["to"][0] 
        to_column = move["to"][1] 

        #----------------------Diagonal move-----------------------------
        if from_row != to_row and from_column != to_column :
            print("Diagonale")
            return False

        #------------------------Throne----------------------------------
        if move["to"] == [4,4] :
            print("Trono")
            return False

        #-------------------------Citadels---------------------------------
        citadels = [[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]]

        if state["turn"]== "WHITE" :
            if move["to"] in citadels:
                print("Bianco in Accampamento")
                return False

        if state["turn"]== "BLACK" :
            if not (move["from"] in citadels) and move["to"] in citadels :
                print("Nero uscito che torna in accampamento")
                return False
        
        #----------------------Other Pawns---------------------------------
        
        if state["board"] [to_row] [to_column] != "O" :
            print("Posizione di arrivo occupata")
            return False

        if state["turn"]== "WHITE" :
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if (state["board"][i][to_column] != "O") and (state["board"][i][to_column] in citadels):
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if (state["board"][i][to_column]) != "O" and (state["board"][i][to_column] in citadels):
                            print("Altra pedina lungo la traiettoria")
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if (state["board"][to_row][i] != "O") and (state["board"][to_row][i] in citadels):
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column):
                        if (state["board"][to_row] [i] != "O") and (state["board"][to_row][i] in citadels):
                            print("Altra pedina lungo la traiettoria")
                            return False 

        if state["turn"]== "BLACK" and move["from"] in citadels:
                    #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if state["board"][i][to_column] != "O" :
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if state["board"][i][to_column] != "O" :
                            print("Altra pedina lungo la traiettoria")
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if state["board"][to_row][i] != "O" :
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column):
                        if state["board"][to_row][i] != "O" :
                            print("Altra pedina lungo la traiettoria")
                            return False 

        return True