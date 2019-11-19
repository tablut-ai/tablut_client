
class HeuristicNumpy:

    def __init__(self):
        self.pawns = {"B" : 0, "W": 0, "K": 0} 

    def update(self, state):
        self.pawns["B"] = 0
        self.pawns["W"] = 0
        self.pawns["K"] = 0

        for i in range(9):
            for j in range(9):
                if state[i,j] == -1:
                    self.pawns["B"] += 1
                if state[i,j] == 1:
                    self.pawns["W"] += 1
                if state[i,j] == 2:
                    self.pawns["K"] = (i,j)

    def eval_fn(self, state, turn, material_w=1, free_w=3, escapes_w=3):
        return turn * (
            material_w * self.material() + 
            free_w * self.free_sides(state) + 
            escapes_w * self.free_escapes(state))


    def material(self):
        """
        (Number of white knights - Number of black knights) in the current state.
        """
        return self.pawns["W"] - self.pawns["B"]

    def free_sides(self, state):
        """
        Number of king's free sides in the current state
        """
        sides = 0
        K_row = self.pawns["K"][0]
        K_column = self.pawns["K"][1]
        
        try:
            if state[K_row, K_column + 1] == 0:
                sides += 1
        except:
            pass
        try:
            if state[K_row, K_column - 1] == 0:
                sides += 1
        except:
            pass
        try:
            if state[K_row + 1, K_column] == 0:
                sides += 1
        except:
            pass
        try:
            if state[K_row - 1, K_column] == 0:
                sides += 1
        except:
            pass

        return sides


    def free_escapes(self, state):
        """
        Number of escape squares reachable in 1 move by the king in the current state.
        """
        escapes = 0
        K_row = self.pawns["K"][0]
        K_column = self.pawns["K"][1]

        if K_row in [1,2,6,7]: 
            if len([state[K_row, j]  for j in range(0, K_column) if state[K_row, j] != 0]) == 0:
                escapes += 1
            if len([state[K_row, j]  for j in range(K_column + 1, 9) if state[K_row, j] != 0]) == 0:
                escapes += 1
        
        if K_column in [1,2,6,7]: 
            if len([state[i, K_column] for i in range(0, K_row) if state[i, K_column] != 0]) == 0:
                escapes += 1
            if len([state[i, K_column] for i in range(K_row + 1, 9) if state[i, K_column] != 0]) == 0:
                escapes += 1
            
        return escapes