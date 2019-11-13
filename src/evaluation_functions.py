#====================EVALUATION FUNCTIONS=============================================

def evaluation_fn(game, state, turn, material_w=1, free_w=1, escapes_w=1):
    Pawns = Board_Reader(state)
    val = material_w * Material(Pawns) + free_w * Free_Sides(state, Pawns) + escapes_w * Reachable_Escapes(state, Pawns)
    return turn * val

def Board_Reader(state):
    """
    Board_Reader(state) returns a dictionary containing the number of W and B knights and the king position
    in the current state.
    """
 
    Pawns = {"B" : 0, "W": 0, "K": 0} 
    for i in range(9):
        for j in range(9):
            if state[i,j] == -1:
                Pawns["B"] += 1
            if state[i,j] == 1:
                Pawns["W"] += 1
            if state[i,j] == 2:
                Pawns["K"] = (i,j)
    
    return Pawns



def Material(Pawns):
    """
    (Number of white knights - Number of black knights) in the current state.
    """

    return Pawns["W"] - Pawns["B"]



def Free_Sides(state, Pawns):
    """
    Number of king's free sides in the current state
    """
    sides = 0
    K_row = Pawns["K"][0]
    K_column = Pawns["K"][1]
    
    try:
        if state[K_row, K_column + 1] == "O":
            sides += 1
    except:
        pass
    try:
        if state[K_row, K_column - 1] == "O":
            sides += 1
    except:
        pass
    try:
        if state[K_row + 1, K_column] == "O":
            sides += 1
    except:
        pass
    try:
        if state[K_row - 1, K_column] == "O":
            sides += 1
    except:
        pass

    return sides



def Reachable_Escapes(state, Pawns):
    """
    Number of escape squares reachable in 1 move by the king in the current state.
    """
    escapes = 0
    K_row = Pawns["K"][0]
    K_column = Pawns["K"][1]

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