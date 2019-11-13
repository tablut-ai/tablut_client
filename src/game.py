from evaluation_functions import evaluation_fn
from AlphaBeta import alphabeta_cutoff_search
import numpy as np
from random import randint

class TablutGame:

    def __init__(self):
        self.c=0

    # invoked by the game loop
    def next_move(self, state, turn):
        '''
        depth = 4 
        move = alphabeta_cutoff_search(state, self, depth, cutoff_test=None, eval_fn=evaluation_fn)
        return self.parse_move(move)
        

        moves = self.actions(state, turn)
        print("\n\n\n\n\n==================NUMBER OF POSSIBLE MOVES:", moves.shape[0])
        move_id = randint(0,moves.shape[0]-1)
        print(move_id, moves[move_id])
        if turn == -1:
            self.black_capture_white(state, moves[move_id])
            self.capture_king(state, moves[move_id])
        else:
            self.white_capture_black(state, moves[move_id])
        return self.parse_move(moves[move_id])
        
        '''
        depth = 2
        move = alphabeta_cutoff_search(self, state, turn, d = depth, eval_fn = evaluation_fn)
        print(move)
        return self.parse_move(move)
       

    
    def white_moves_set(self, state, turn):
        """
        Return a Nx4 numpy array of allowable moves for the WHITE player in the current state.
        Each move in the array is written as [[from_row, from_column], [to_row, to_column]]
        """
        print("BOARD DI WHITE MOVES", state)
        moves = []
        for row in range(9):
            for col in range(9):
                if state[row,col] == 1 or state[row, col] == 2 :
                    for new_col in range(8, col, -1):
                        if self.silent_check_move(state, np.array([[row, col], [row, new_col]]), turn):
                            moves.append([[row, col], [row, new_col]])
                    for new_col in range(0, col):
                        if self.silent_check_move(state, np.array([[row, col], [row, new_col]]), turn):
                            moves.append([[row, col], [row, new_col]])
                    for new_row in range(8, row, -1):                        
                        if self.silent_check_move(state, np.array([[row, col], [new_row, col]]), turn):
                            moves.append([[row, col], [new_row, col]])
                    for new_row in range(0, row):
                        if self.silent_check_move(state, np.array([[row, col], [new_row, col]]), turn):
                            moves.append([[row, col], [new_row, col]])

        return np.array(moves)


    def black_moves_set(self, state, turn):
        """
        Return a Nx4 numpy array of allowable moves for the WHITE player in the current state.
        Each move in the array is written as [[from_row, from_column], [to_row, to_column]]
        """
        moves = []
        for row in range(9):
            for col in range(9):
                if state[row,col] == -1 :
                    for new_col in range(8, col, -1):
                        if self.silent_check_move(state, np.array([[row, col], [row, new_col]]), turn):
                            moves.append([[row, col], [row, new_col]])
                    for new_col in range(0, col):
                        if self.silent_check_move(state, np.array([[row, col], [row, new_col]]), turn):
                            moves.append([[row, col], [row, new_col]])
                    for new_row in range(8, row, -1):                        
                        if self.silent_check_move(state, np.array([[row, col], [new_row, col]]), turn):
                            moves.append([[row, col], [new_row, col]])
                    for new_row in range(0, row):
                        if self.silent_check_move(state, np.array([[row, col], [new_row, col]]), turn):
                            moves.append([[row, col], [new_row, col]])

        return np.array(moves)


    def actions(self, state, turn):
        """
        Return the set of allowable moves for the current player represented by a 2x2 numpy array:
        [[from_row, from_column], [to_row, to_column]]
        """    
        if turn == 1:
            return self.white_moves_set(state, turn)
        else:
            return self.black_moves_set(state, turn)
  
    def result(self, state, move):
        """Updates the state according to the last move"""
        p = state[move[0,0], move[0,1]]
        state [move[0,0], move[0,1]] = 0
        state [move[1,0], move[1,1]] = p

        raise state

    def tree_result(self, state, move, turn):
        """Updates the state according to the last move for tree generation"""
        print("MOSSA", move)

        p = state[move[0,0], move[0,1]]
        state [move[0,0], move[0,1]] = 0
        state [move[1,0], move[1,1]] = p
    
        if turn == 1:
            state = self.white_capture_black(state, move)

        else:
            state = self.black_capture_white(state, move)

        return state

    def tree_terminal_test(self, state, turn, move):
        """Return True if this is a final state for the game."""
        if turn == 1:
            return self.king_escape(state, move)
        else:
            return self.capture_king(state, move)

    def terminal_test(self, state):
        """Returns True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state, turn):
        return turn

    def parse_move(self, move):
        return {
            "from": chr(97 + move[0,1]) + str(move[0,0]+1),
            "to": chr(97 + move[1,1]) + str(move[1,0]+1)
        }

    def check_move(self, state, move, turn):

        from_row = move[0,0]
        from_column = move[0,1]
        to_row = move[1,0] 
        to_column = move[1,1] 
        

        #----------------------Diagonal move-----------------------------
        if from_row != to_row and from_column != to_column :
            print("Diagonale")
            return False

        #------------------------Throne----------------------------------
        throne = np.array([4,4])
        if np.array_equal(move[1], throne) :
            print("Trono")
            return False

        #------------------------Occupied position----------------------------------
        if state[to_row, to_column] != 0 :
            print("Posizione di arrivo occupata")
            return False

        #-------------------------Citadels---------------------------------
        citadels = np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]])

        if turn == 1 :
            if (((move[1] == citadels).all(axis=(1))).any()):
                print("Bianco in Accampamento")
                return False

        if turn == -1 :
            if not (((move[0] == citadels).all(axis=(1))).any())  and (((move[1] == citadels).all(axis=(1))).any()) :
                print("Nero uscito che torna in accampamento")
                return False
        
        #----------------------Blocked trajectory---------------------------------


        if turn == 1 or (turn == -1 and not (((move[0] == citadels).all(axis=(1))).any())):
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if (state [i, to_column] != 0) or ((( np.array([i, to_column]) == citadels).all(axis=(1))).any()) or np.array_equal(np.array([i, to_column]), throne):
                            print("Altra pedina o accampamento lungo la traiettoria")
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if (state[i, to_column] != 0) or (((np.array([i, to_column])== citadels).all(axis=(1))).any()) or np.array_equal(np.array([i, to_column]), throne):
                            print("Altra pedina o accampamento lungo la traiettoria")
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if (state [to_row, i] != 0) or (((np.array([to_row, i]) == citadels).all(axis=(1))).any()) or np.array_equal(np.array([to_row, i]), throne):
                            print("Altra pedina o accampamento lungo la traiettoria")
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column):
                        if (state [to_row, i] != 0) or (((np.array([to_row, i])  == citadels).all(axis=(1))).any()) or np.array_equal(np.array([to_row, i]), throne):
                            print("Altra pedina lungo o accampamento la traiettoria")
                            return False 

        if turn == -1 and (((move[0] == citadels).all(axis=(1))).any()):
            #Vertical move
            if from_column == to_column:
                if from_row < to_row:
                    for i in range(to_row, from_row, -1) :
                        if state [i, to_column] != 0 or np.array_equal(np.array([i, to_column]), throne):
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_row > to_row:
                    for i in range(to_row, from_row):
                        if state [i, to_column] != 0 or np.array_equal(np.array([i, to_column]), throne):
                            print("Altra pedina lungo la traiettoria")
                            return False                
            #Horizontal move
            if from_row == to_row:
                if from_column < to_column:
                    for i in range(to_column, from_column, -1) :
                        if state [to_row, i] != 0 or np.array_equal(np.array([to_row, i]), throne):
                            print("Altra pedina lungo la traiettoria")
                            return False
                if from_column > to_column:
                    for i in range(to_column, from_column) :
                        if state [to_row, i] != 0 or np.array_equal(np.array([to_row, i]), throne):
                            print("Altra pedina lungo la traiettoria")
                            return False 
        
        return True

    def silent_check_move(self, state, move, turn):

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


#============== CATTURA MULTIPLA???? ===============================
    def black_capture_white(self, state, move):

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
    
    def white_capture_black(self, state, move):

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

    def capture_king(self, state, move):

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


    def king_escape(self, state, move):

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




















