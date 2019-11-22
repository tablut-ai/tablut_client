class HeuristicObj:

    def evaluation_fn(self, state, turn, material_w=1, free_w=8,  escapes_w=10):
        w = 0
        b = 0
        for i in range(9):
            for j in range(9):
                if state[i][j] == 2:
                    king_pos = [i, j]
                elif state[i][j] == 1:
                    w+=1
                elif state[i][j] == -1:
                    b+=1

        val = (material_w * (w - b) + 
            free_w * self.free_sides(state, king_pos) + 
            escapes_w * self.free_escapes(state, king_pos)) 
        return turn * val

    def free_sides(self, state, king_pos):
        """
        Number of king's free sides in the current state
        """
        sides = 0
        K_row = king_pos[0]
        K_column = king_pos[1]
        
        sides += 1 if state[K_row][K_column + 1] == 0 else 0
        sides += 1 if state[K_row][K_column - 1] == 0 else 0
        sides += 1 if state[K_row + 1][K_column] == 0 else 0
        sides += 1 if state[K_row - 1][K_column] == 0 else 0

        return sides

    def free_escapes(self, state, king_pos):
        """
        Number of escape squares reachable in 1 move by the king in the current state.
        """
        escapes = 0
        K_row = king_pos[0]
        K_column = king_pos[1]

        if K_row in [1,2,6,7]: 
            if len([state[K_row][j]  for j in range(0, K_column) if state[K_row][j] != 0]) == 0:
                escapes += 1
            if len([state[K_row][j]  for j in range(K_column + 1, 9) if state[K_row][j] != 0]) == 0:
                escapes += 1
        
        if K_column in [1,2,6,7]: 
            if len([state[i][K_column] for i in range(0, K_row) if state[i][K_column] != 0]) == 0:
                escapes += 1
            if len([state[i][K_column] for i in range(K_row + 1, 9) if state[i][K_column] != 0]) == 0:
                escapes += 1
            
        return escapes