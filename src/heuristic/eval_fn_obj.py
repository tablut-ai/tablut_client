#Evaluation functions 

def evaluation_fn(game, material_w=1, free_w=1, escapes_w=1):
    Pawns = Board_Reader(state)
    val = material_w * Material(Pawns) + free_w * Free_Sides(state, Pawns) + escapes_w * Reachable_Escapes(state, Pawns)
    if game.turn == "white":
        return val
    return - val

def Board_Reader(state):
    """
    Board_Reader(state) returns a dictionary containing the number of W and B knights and the king position
    in the current state.
    """
    Pawns = {"B" : 0, "W": 0, "K": ()} 

    for i in range(10):
        for j in range(10):
            if state[i,j] == "B":
                Pawns["B"] += 1
            if state[i,j] == "W":
                Pawns["W"] += 1
            if state[i,j] == "K":
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
    K_pos = Pawns["K"]

    if state[K_pos[0], K_pos[1] + 1] == "O":
        sides += 1
    if state[K_pos[0], K_pos[1] - 1] == "O":
        sides += 1
    if state[K_pos[0] + 1, K_pos[1]] == "O":
        sides += 1
    if state[K_pos[0] - 1, K_pos[1]] == "O":
        sides += 1

    return sides



def Reachable_Escapes(state, Pawns):
    """
    Number of escape squares reachable in 1 move by the king in the current state.
    """
    escapes = 0
    K_pos = Pawns["K"]

    if K_pos[0] in [1,2,6,7]: 
        if len([state[K_pos[0], j]  for j in range(K_pos[1] - 1, 0, -1) if state[K_pos[0], j] != "O"]) == 0:
            escapes += 1
        if len([state[K_pos[0], j]  for j in range(K_pos[1] + 1, 8) if state[K_pos[0], j] != "O"]) == 0:
            escapes += 1
    
    if K_pos[1] in [1,2,6,7]: 
        if len([state[i, K_pos[1]] for i in range(K_pos[0] - 1, 0, -1) if state[i, K_pos[1]] != "O"]) == 0:
            escapes += 1
        if len([state[i, K_pos[1]] for i in range(K_pos[0] + 1, 8) if state[i, K_pos[1]] != "O"]) == 0:
            escapes += 1
        
    return escapes