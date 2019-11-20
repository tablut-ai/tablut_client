class GameObj:

    def __init__(self):

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

    def actions(self, state, turn):
        moves = []
        for col in range(9):
            for row in range(9):
                if state[row][col] * turn > 0:
                    mcol = col - 1
                    while mcol >= 0:
                        if [row, mcol] == self.throne:
                            break
                        if ([row, mcol] in self.citadels and
                            (turn == 1 or [row, col] not in self.citadels)):
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
                            (turn == 1 or [row, col] not in self.citadels)):
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
                            (turn == 1 or [row, col] not in self.citadels)):
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
                            (turn == 1 or [row, col] not in self.citadels)):
                            break
                        if state[mrow][col] != 0:
                            break
                        moves.append([[row, col], [mrow, col]])
                        mrow += 1
        return moves

    def result(self, state, move, turn):
        """Updates the state according to the last move for tree generation"""
        state [move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
        state [move[0][0]][move[0][1]] = 0

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

    def _capture_king(self, state, move):

        my_row = move[1][0]
        my_column =  move[1][1]

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
                
        #Capture Down
        if (    my_row < 7 
            and state[my_row + 1][ my_column] == 2 
            and ( state[my_row + 2][ my_column] == -1 or [my_row + 2,my_column] in self.citadels)):
            return True

        #Capture Up
        if (my_row > 1 
            and state[my_row - 1][ my_column] == 2 
            and (state[my_row - 2][ my_column] == -1 or [my_row - 2, my_column] in self.citadels)):
            return True

        #Capture Left
        if (my_column > 1 
            and state[my_row][ my_column - 1] == 1 
            and (state[my_row][ my_column - 2 ] == -1 or [my_row, my_column - 2] in self.citadels)):
            return True
        
        #Capture Right
        if (my_column < 7 
            and state[my_row][ my_column + 1] == 1 
            and (state[my_row][ my_column + 2 ] == -1 or [my_row, my_column + 2] in self.citadels)):
            return True
        
        return False

    def _king_escape(self, state, move):

        row = move[1][0]
        column =  move[1][1]
        if state[row][ column] == 2 and move[1] in self.escapes:
            return True
        
        return False
    