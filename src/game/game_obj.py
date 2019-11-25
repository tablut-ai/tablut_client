class GameObj:

    def __init__(self, color):
        self.color = color

        self.citadels = [[0,3], [0,4], [0,5], [1,4], 
                         [8,3], [8,4], [8,5], [7,4], 
                         [3,8], [4,8], [5,8], [4,7], 
                         [3,0], [4,0], [5,0], [4,1]]

        self.safe_citadels = [[0,3], [0,4], [0,5], 
                              [8,3], [8,4], [8,5], 
                              [3,8], [4,8], [5,8], 
                              [3,0], [4,0], [5,0]]
        
        self.throne = [4,4]

        self.escapes = [[0,1],[0,2],[0,6],[0,7], 
                        [8,1],[8,2],[8,6],[8,7],
                        [1,0],[2,0],[6,0],[7,0],
                        [1,8],[2,8],[6,8],[7,8]]

    def actions(self, state, color):
        moves = []
        for col in range(9):
            for row in range(9):
                if state[row][col] * color > 0:
                    mcol = col - 1
                    while mcol >= 0:
                        if [row, mcol] == self.throne:
                            break
                        if ([row, mcol] in self.citadels and
                            (color == 1 or [row, col] not in self.citadels)):
                            break
                        if state[row][mcol] != 0:
                            break
                        moves.append([[row, col], [row, mcol]])
                        mcol -= 1
                    mcol = col +1
                    while mcol < 9:
                        if [row, mcol] == self.throne:
                            break
                        if ([row, mcol] in self.citadels and
                            (color == 1 or [row, col] not in self.citadels)):
                            break
                        if state[row][mcol] != 0:
                            break
                        moves.append([[row, col], [row, mcol]])
                        mcol += 1

                    mrow = row - 1
                    while mrow >= 0:
                        if [mrow, col] == self.throne:
                            break
                        if ([mrow, col] in self.citadels and
                            (color == 1 or [row, col] not in self.citadels)):
                            break
                        if state[mrow][col] != 0:
                            break
                        moves.append([[row, col], [mrow, col]])
                        mrow -= 1
                    mrow = row +1
                    while mrow < 9:
                        if [mrow, col] == self.throne:
                            break
                        if ([mrow, col] in self.citadels and
                            (color == 1 or [row, col] not in self.citadels)):
                            break
                        if state[mrow][col] != 0:
                            break
                        moves.append([[row, col], [mrow, col]])
                        mrow += 1
        return moves

    def result(self, state, move, color):
        """Updates the state according to the last move for tree generation"""
        state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
        state[move[0][0]][move[0][1]] = 0

        if color == 1:
            state = self._white_capture_black(state, move)
        else:
            state = self._black_capture_white(state, move)

        return state

    def terminal_test(self, state, color):
        if color == 1:
            return self._capture_king(state)
        else :
            return self._king_escape(state) 


    def _white_capture_black(self, state, move):

        my_row = move[1][0]
        my_column =  move[1][1]

        #Capture Down
        if (my_row < 7 
            and state[my_row + 1][my_column] == -1 
            and not [my_row + 1, my_column] in self.safe_citadels
            and ( state[my_row + 2][my_column] == 1 
                or [my_row + 2, my_column] in self.citadels
                or [my_row + 2, my_column] == self.throne)): 
            
            state[my_row + 1][my_column] = 0
            return state

        #Capture Up
        if (my_row > 1 
            and state[my_row - 1][my_column] == -1
            and not [my_row - 1, my_column] in self.safe_citadels 
            and ( state[my_row - 2][my_column] == 1 
                or [my_row - 2, my_column] in self.citadels
                or [my_row - 2, my_column] == self.throne)):
            
            state[my_row - 1][my_column] = 0
            return state

        #Capture Left
        if (my_column > 1 
            and state[my_row][my_column - 1] == -1 
            and not [my_row, my_column - 1] in self.safe_citadels
            and ( state[my_row][my_column - 2]  == 1 
                or [my_row, my_column - 2] in self.citadels
                or [my_row, my_column - 2] == self.throne)):
            
            state[my_row][my_column - 1]  = 0
            return state
        
        #Capture Right
        if (my_column < 7 
            and state[my_row][my_column + 1] == -1 
            and not [my_row, my_column + 1] in self.safe_citadels
            and ( state[my_row][my_column + 2]  == 1 
                or [my_row, my_column + 2] in self.citadels
                or [my_row, my_column + 2] == self.throne)):
            
            state[my_row][my_column + 1]  = 0
            return state

        return state

    def _black_capture_white(self, state, move):

        my_row = move[1][0]
        my_column =  move[1][1]

        #Capture Down
        if (my_row < 7 
            and state[my_row + 1][my_column] == 1 
            and ( state[my_row + 2][my_column] == -1 
                or [my_row + 2, my_column] in self.citadels
                or [my_row + 2, my_column] == self.throne)): 
            
            state[my_row + 1][my_column] = 0
            return state

        #Capture Up
        if (my_row > 1 
            and state[my_row - 1][my_column] == 1 
            and ( state[my_row - 2][my_column] == -1 
                or [my_row - 2, my_column] in self.citadels
                or [my_row - 2, my_column] == self.throne)):
            
            state[my_row - 1][my_column] = 0
            return state

        #Capture Left
        if (my_column > 1 
            and state[my_row][my_column - 1] == 1 
            and ( state[my_row][my_column - 2]  == -1 
                or [my_row, my_column - 2] in self.citadels
                or [my_row, my_column - 2] == self.throne)):
            
            state[my_row][my_column - 1]  = 0
            return state
        
        #Capture Right
        if (my_column < 7 
            and state[my_row][my_column + 1] == 1 
            and ( state[my_row][my_column + 2]  == -1 
                or [my_row, my_column + 2] in self.citadels
                or [my_row, my_column + 2] == self.throne)):
            
            state[my_row][my_column + 1]  = 0
            return state

        return state

    def _capture_king(self, state):
        #King on the throne
        if (    state[4][4] == 2 
            and state[4][5] == -1   
            and state[4][3] == -1 
            and state[3][4] == -1
            and state[5][4] == -1):
            return True

        #King on the right of the throne
        if (    state[4][5] == 2 
            and state[3][5] == -1 
            and state[5][5] == -1 
            and state[4][6] == -1):
            return True
            
        #King on the left of the throne
        if (    state[4][3] == 2 
            and state[3][3] == -1 
            and state[5][3] == -1 
            and state[4][2] == -1):
            return True
        
        #King above the throne
        if (    state[3][4] == 2             
            and state[3][2] == -1 
            and state[3][5] == -1 
            and state[2][4] == -1):
            return True

        #King below the throne
        if (    state[5][4] == 2             
            and state[5][5] == -1 
            and state[5][3] == -1 
            and state[6][4] == -1):
            return True
                
        if state[4][4] != 2:
            for i in range(9):
                for j in range(9):
                    if state[i][j] == 2:
                        k_row = i
                        k_column = j
                        
                        #Vertical capture
                        if (k_row < 8 and k_row > 0
                            and ( state[k_row + 1][ k_column] == -1 or [k_row + 1,k_column] in self.citadels or [k_row + 1,k_column] == self.throne)  
                            and (state[k_row - 1][ k_column] == -1 or [k_row - 1, k_column] in self.citadels or [k_row - 1,k_column] == self.throne )):
                            return True

                        #Horizontal capture
                        if (k_column < 8 and k_column > 0
                            and ( state[k_row][ k_column + 1] == -1 or [k_row, k_column + 1] in self.citadels or [k_row,k_column + 1]  == self.throne)  
                            and (state[k_row][ k_column - 1] == -1 or [k_row, k_column - 1]  in self.citadels or [k_row, k_column - 1]  == self.throne )):
                            return True
                    
        return False

    def _king_escape(self, state):
        for escape in self.escapes:
            if state[escape[0]][escape[1]] == 2:
                return True
        return False
    