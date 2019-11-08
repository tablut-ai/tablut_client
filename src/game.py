from aima.adversarial_search import alphabeta_cutoff_search
from evaluation_functions import evaluation_fn
import numpy as np

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


    def white_moves_set(self, state, turn):
        """
        Return a Nx4 numpy array of allowable moves for the WHITE player in the current state.
        Each move in the array is written as [from_row, from_column, to_row, to_column]
        """
        moves = []
        for row in range(9):
            for col in range(9):
                if state[row, col] > 0 :
                    for new_col in range(8, col, -1):
                        if self.check_moves(state,[row, col, row, new_col], turn):
                            moves.append([row, col, row, new_col])
                    for new_col in range(0, col):
                        if self.check_moves(state,[row, col, row, new_col], turn):
                            moves.append([row, col, row, new_col])
                    for new_row in range(8, row, -1):                        
                        if self.check_moves(state, [row, col, new_row, col], turn):
                            moves.append([row, col, new_row, col])
                    for new_row in range(0, row):
                        if self.check_moves(state, [row, col, new_row, col], turn):
                            moves.append([row, col, new_row, col])

        return np.array(moves)


    def black_moves_set(self, state, turn):
        """
        Return a Nx4 numpy array of allowable moves for the WHITE player in the current state.
        Each move in the array is written as [from_row, from_column, to_row, to_column]
        """
        moves = []
        for row in range(9):
            for col in range(9):
                if state[row,col] == -1 :
                    for new_col in range(8, col, -1):
                        if self.check_moves(state,[row, col, row, new_col], turn):
                            moves.append([row, col, row, new_col])
                    for new_col in range(0, col):
                        if self.check_moves(state,[row, col, row, new_col], turn):
                            moves.append([row, col, row, new_col])
                    for new_row in range(8, row, -1):                        
                        if self.check_moves(state, [row, col, new_row, col], turn):
                            moves.append([row, col, new_row, col])
                    for new_row in range(0, row):
                        if self.check_moves(state, [row, col, new_row, col], turn):
                            moves.append([row, col, new_row, col])

        return np.array(moves)


    def actions(self, state, turn):
        """
        Return the set of allowable moves for the current player represented by a 1x4 numpy array:
        [from_row, from_column, to_row, to_column]
        """    
        if turn == "WHITE": 
            return white_moves_set(self, state, turn)
        if turn == "BLACK":
            return black_moves_set(self, state, turn)  


    def result(self, state, move):
        """Updates the state according to the last move"""
        p = state[move[0], move[1]]
        state [move[0], move[1]] = 0
        state [move[2]], move[3]] = p
        raise state

    def terminal_test(self, state):
        """Returns True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state, turn):
        return turn

    def parse_move(self, move):
        return {
            "from": chr(97 + move[1]) + str(move[0]+1),
            "to": chr(97 + move[3]) + str(move[2]+1)
        }

    def check_move(self, state, move, turn):

        from_row = move[0]
        from_column = move[1]
        to_row = move[2] 
        to_column = move[3] 

        #----------------------Diagonal move-----------------------------
        if from_row != to_row and from_column != to_column :
            print("Diagonale")
            return False

        #------------------------Throne----------------------------------
        if move[2:] == [4,4] :
            print("Trono")
            return False

        #------------------------Occupied position----------------------------------
        if state[to_row, to_column] != 0 :
            print("Posizione di arrivo occupata")
            return False

        #-------------------------Citadels---------------------------------
        citadels = np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]])

        if turn == "WHITE" :
            if (((move[2:] == citadels).all(axis=(1))).any()):
                print("Bianco in Accampamento")
                return False

        if turn == "BLACK" :
            if not (((move[0:2] == citadels).all(axis=(1))).any())  and (((move[2:] == citadels).all(axis=(1))).any()) :
                print("Nero uscito che torna in accampamento")
                return False
        
        #----------------------Blocked trajectory---------------------------------

        if turn == "WHITE" or (turn == "BLACK" and not (((move[0:2] == citadels).all(axis=(1))).any()):
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if (state [i, to_column] != 0) or (((state [i, to_column] == citadels).all(axis=(1))).any()):
                            print("Altra pedina o accampamento lungo la traiettoria")
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if (state[i, to_column] != 0) or (((state [i, to_column] == citadels).all(axis=(1))).any()):
                            print("Altra pedina o accampamento lungo la traiettoria")
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if (state [to_row, i] != 0) or (((state [to_row, i] == citadels).all(axis=(1))).any()):
                            print("Altra pedina o accampamento lungo la traiettoria")
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column):
                        if (state [to_row, i] != 0) or (((state [to_row, i] == citadels).all(axis=(1))).any()):
                            print("Altra pedina lungo o accampamento la traiettoria")
                            return False 

        if turn == "BLACK" and (((move[0:2] == citadels).all(axis=(1))).any()):
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if state [i, to_column] != 0 :
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if state [i, to_column] != 0 :
                            print("Altra pedina lungo la traiettoria")
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if state [to_row, i] != 0 :
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column):
                        if state [to_row, i] != 0 :
                            print("Altra pedina lungo la traiettoria")
                            return False 

        return True