from aima.adversarial_search import alphabeta_cutoff_search
from evaluation_functions import evaluation_fn
import numpy as np

class GameNumpy:

    def actions(self, state, turn):
        moves = []
        for row in range(9):
            for col in range(9):
                if (state[row, col] > 0 and turn == 1) or (state[row, col] == 0 and turn == -1)
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


    def result(self, state, move):
        """Updates the state according to the last move for tree generation"""
        print("MOSSA", move)

        state [move[1,0], move[1,1]] = state[move[0,0], move[0,1]]
        state [move[0,0], move[0,1]] = 0
    
        if turn == 1:
            state = self._white_capture_black(state, move)

        else:
            state = self._black_capture_white(state, move)

        return state
        

    def terminal_test(self, state, turn, move):
        """Return True if this is a final state for the game."""
        if turn == 1:
            return self._king_escape(state, move)
        else:
            return self._capture_king(state, move)


#============== CATTURA MULTIPLA???? ===============================
    def _black_capture_white(self, state, move):

        my_row = move[1,0]
        my_column =  move[1,1]
        citadels =  np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4], [3,8], [4,8], [5,8], [4,7], [3,0], [4,0], [5,0], [4,1]])
        throne = np.array([4,4]) 

        #Capture Down
        if (my_row < 7 
            and state[my_row + 1, my_column] == 1 
            and ( state[my_row + 2, my_column] == -1 
                or ((np.array([my_row + 2, my_column])  == citadels).all(axis=(1))).any()
                or np.array_equal(np.array([my_row + 2, my_column]), throne) )
            ) :
            
            print("Pedina bianca catturata in", my_row + 1, my_column)
            state[my_row + 1, my_column] = 0
            return state

        #Capture Up
        if (my_row > 1 
            and state[my_row - 1, my_column] == 1 
            and ( state[my_row - 2, my_column] == -1 
                or ((np.array([my_row - 2, my_column])  == citadels).all(axis=(1))).any() 
                or np.array_equal(np.array([my_row - 2, my_column]), throne) )
            ) :
            
            print("Pedina bianca catturata in", my_row - 1, my_column)
            state[my_row - 1, my_column] = 0
            return state

        #Capture Left
        if (my_column > 1 
            and state[my_row, my_column - 1] == 1 
            and ( state[my_row, my_column - 2]  == -1 
                or ((np.array([my_row, my_column - 2] )  == citadels).all(axis=(1))).any()
                or np.array_equal(np.array([my_row, my_column - 2] ), throne) )
            ) :
            
            print("Pedina bianca catturata in", my_row, my_column - 1)
            state[my_row, my_column - 1]  = 0
            return state
        
        #Capture Right
        if (my_column < 7 
            and state[my_row, my_column + 1] == 1 
            and ( state[my_row, my_column + 2]  == -1 
                or ((np.array([my_row, my_column + 2] )  == citadels).all(axis=(1))).any()
                or np.array_equal(np.array([my_row, my_column + 2] ), throne) )
            ) :
            
            print("Pedina bianca catturata in", my_row, my_column + 1)
            state[my_row, my_column + 1]  = 0
            return state
        return state
    
    def _white_capture_black(self, state, move):

        my_row = move[1,0]
        my_column =  move[1,1]
        citadels =  np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4], [3,8], [4,8], [5,8], [4,7], [3,0], [4,0], [5,0], [4,1]])
        throne = np.array([4,4]) 

        #Capture Down
        if (my_row < 7 
            and state[my_row + 1, my_column] == -1 
            and not ((np.array([my_row + 1, my_column])  == citadels).all(axis=(1))).any() #per evitare di mangiare pedine nere che sono ancora in accampamento
            and ( state[my_row + 2, my_column] == 1 
                or ((np.array([my_row + 2, my_column])  == citadels).all(axis=(1))).any()
                or np.array_equal(np.array([my_row + 2, my_column]), throne) )
            ) :
            
            print("1) Pedina nera catturata in", my_row + 1, my_column)
            state[my_row + 1, my_column] = 0
            return state

        #Capture Up
        if (my_row > 1 
            and state[my_row - 1, my_column] == -1 
            and not ((np.array([my_row - 1, my_column])  == citadels).all(axis=(1))).any()
            and ( state[my_row - 2, my_column] == 1 
                or ((np.array([my_row - 2, my_column])  == citadels).all(axis=(1))).any() 
                or np.array_equal(np.array([my_row - 2, my_column]), throne) )
            ) :
            
            print("2) Pedina nera catturata in", my_row - 1, my_column)
            state[my_row - 1, my_column] = 0
            return state

        #Capture Left
        if (my_column > 1 
            and state[my_row, my_column - 1] == -1 
            and not ((np.array([my_row, my_column - 1])  == citadels).all(axis=(1))).any()
            and ( state[my_row, my_column - 2]  == 1 
                or ((np.array([my_row, my_column - 2] )  == citadels).all(axis=(1))).any()
                or np.array_equal(np.array([my_row, my_column - 2] ), throne) )
            ) :
            
            print("3) Pedina nera catturata in", my_row, my_column - 1)
            state[my_row, my_column - 1]  = 0
            return state
        
        #Capture Right
        if (my_column < 7 
            and state[my_row, my_column + 1] == -1 
            and ( state[my_row, my_column + 2]  == 1 
                or ((np.array([my_row, my_column + 2] )  == citadels).all(axis=(1))).any()
                or np.array_equal(np.array([my_row, my_column + 2] ), throne) )
            ) :
            
            print("4) Pedina nera catturata in", my_row, my_column + 1)
            state[my_row, my_column + 1]  = 0
            return state

        return state   

    def _capture_king(self, state, move):

        my_row = move[1,0]
        my_column =  move[1,1]
        citadels =  np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4], [3,8], [4,8], [5,8], [4,7], [3,0], [4,0], [5,0], [4,1]])
        throne = np.array([4,4]) 
        next_throne = np.array([[4,3],[4,5],[3,4],[5,4]])

        #King on the throne
        if (    state[4,4] == 2 
            and state[4,5] == -1   
            and state[4,3] == -1 
            and state[3,4] == -1
            and state[5,4] == -1):
            print("RE MANGIATO SUL TRONO")
            return True

        #King on the right of the throne
        if (    state[4,5] == 2 
            and state[3,5] == -1 
            and state[5,5] == -1 
            and state[4,6] == -1):
            print("RE MANGIATO A DESTRA del TRONO")
            return True
            
        #King on the left of the throne
        if (    state[4,3] == 2 
            and state[3,3] == -1 
            and state[5,3] == -1 
            and state[4,2] == -1):
            print("RE MANGIATO A SINISTRA del TRONO")
            return True
        
        #King above the throne
        if (    state[3,4] == 2             
            and state[3,2] == -1 
            and state[3,5] == -1 
            and state[2,4] == -1):
            print("RE MANGIATO SOPRA il TRONO")
            return True

        #King below the throne
        if (    state[5,4] == 2             
            and state[5,5] == -1 
            and state[5,3] == -1 
            and state[6,4] == -1):
            print("RE MANGIATO SOTTO il TRONO")
            return True
                
        #Capture Down
        if (my_row < 7 
            and state[my_row + 1, my_column] == 2 
            and ( state[my_row + 2, my_column] == -1 
                or ((np.array([my_row + 2, my_column])  == citadels).all(axis=(1))).any())
            ) :
            
            print("Re catturato in", my_row + 1, my_column)
            return True

        #Capture Up
        if (my_row > 1 
            and state[my_row - 1, my_column] == 2 
            and ( state[my_row - 2, my_column] == -1 
                or ((np.array([my_row - 2, my_column])  == citadels).all(axis=(1))).any())
            ) :
            
            print("Re catturato in", my_row - 1, my_column)
            return True

        #Capture Left
        if (my_column > 1 
            and state[my_row, my_column - 1] == 1 
            and ( state[my_row, my_column - 2]  == -1 
                or ((np.array([my_row, my_column - 2] )  == citadels).all(axis=(1))).any())
            ) :
            
            print("Re catturato in", my_row, my_column - 1)
            return True
        
        #Capture Right
        if (my_column < 7 
            and state[my_row, my_column + 1] == 1 
            and ( state[my_row, my_column + 2]  == -1 
                or ((np.array([my_row, my_column + 2] )  == citadels).all(axis=(1))).any())
            ) :
            
            print("Re catturato in", my_row, my_column + 1)
            return True
        
        return False


    def _king_escape(self, state, move):

        row = move[1,0]
        column =  move[1,1]

        escapes = np.array([[0,1],[0,2],[0,6],[0,7], 
                            [8,1],[8,2],[8,6],[8,7],
                            [1,0],[2,0],[6,0],[7,0],
                            [1,8],[2,8],[6,8],[7,8]])

        print(state)
        if state[row, column] == 2 and ((move[1] == escapes).all(axis=(1))).any():
            print("RE FUGGITO")
            return True
        
        return False
        
    def _check_move(self, state, move, turn):

        from_row = move[0,0]
        from_column = move[0,1]
        to_row = move[1,0] 
        to_column = move[1,1] 
        
        #----------------------Diagonal move-----------------------------
        if from_row != to_row and from_column != to_column :
            return False

        #------------------------Throne----------------------------------
        throne = np.array([4,4])
        if np.array_equal(move[1], throne) :
            return False

        #------------------------Occupied position----------------------------------
        if state[to_row, to_column] != 0 :
            return False

        #-------------------------Citadels---------------------------------
        citadels = np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4], [3,8], [4,8], [5,8], [4,7], [3,0], [4,0], [5,0], [4,1]])

        if turn == 1 :
            if (((move[1] == citadels).all(axis=(1))).any()):
                return False

        if turn == -1 :
            if not (((move[0] == citadels).all(axis=(1))).any())  and (((move[1] == citadels).all(axis=(1))).any()) :
                return False
        
        #----------------------Blocked trajectory---------------------------------


        if turn == 1 or (turn == -1 and not (((move[0] == citadels).all(axis=(1))).any())):
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if (state [i, to_column] != 0) or ((( np.array([i, to_column]) == citadels).all(axis=(1))).any()) or np.array_equal(np.array([i, to_column]), throne):
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if (state[i, to_column] != 0) or (((np.array([i, to_column])== citadels).all(axis=(1))).any()) or np.array_equal(np.array([i, to_column]), throne):
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if (state [to_row, i] != 0) or (((np.array([to_row, i]) == citadels).all(axis=(1))).any()) or np.array_equal(np.array([to_row, i]), throne):
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column):
                        if (state [to_row, i] != 0) or (((np.array([to_row, i])  == citadels).all(axis=(1))).any()) or np.array_equal(np.array([to_row, i]), throne):
                            return False 

        if turn == -1 and (((move[0] == citadels).all(axis=(1))).any()):
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if state [i, to_column] != 0 or np.array_equal(np.array([i, to_column]), throne):
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if state [i, to_column] != 0 or np.array_equal(np.array([i, to_column]), throne):
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if state [to_row, i] != 0 or np.array_equal(np.array([to_row, i]), throne):

                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column) :
                        if state [to_row, i] != 0 or np.array_equal(np.array([to_row, i]), throne):
                            return False 
        
        return True