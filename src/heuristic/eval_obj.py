class HeuristicObj:
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

    def evaluation_fn(self, state, turn, terminal, pawns, material_w=2, king_pos_w=5, white_w = 1, black_w = 1):
        if terminal:
            return -1e8
            
        w = len(pawns[1])
        b = len(pawns[0])
        king_pos = pawns[2][0]

       
        val = (material_w * (white_w * w - black_w * b) + 
            king_pos_w * self.eval_king_pos(state, king_pos))

        return turn * val

    def eval_king_pos(self, state, king_pos,  
        escape_w =  10,
        citadel_w = -1,
        throne_w =  1,
        near_white_w =   -1,
        adjacent_white_w = 1,
        near_black_w =   -2,
        adjacent_black_w = -4):

        row = king_pos[0]
        col = king_pos[1]
        score = 0
        
        mcol = col - 1
        while mcol >= 0:
            if [row, mcol] == self.throne:
                score += throne_w
                break
            if state[row][mcol] == -1:
                if mcol == col - 1:
                    score += adjacent_black_w
                else:
                    score += near_black_w
                break
            if state[row][mcol] == 1:
                if mcol == col - 1:
                    score += adjacent_white_w
                else:
                    score += near_white_w
                break
            if [row, mcol] in self.citadels:
                score += citadel_w
                break
            if [row, mcol] in self.escapes:
                score += escape_w
                break
            mcol -= 1

        mcol = col + 1
        while mcol < 9:
            if [row, mcol] == self.throne:
                score += throne_w
                break
            if state[row][mcol] == -1:
                if mcol == col + 1:
                    score += adjacent_black_w
                else:
                    score += near_black_w
                break
            if state[row][mcol] == 1:
                if mcol == col + 1:
                    score += adjacent_white_w
                else:
                    score += near_white_w
                break
            if [row, mcol] in self.citadels:
                score += citadel_w
                break
            if [row, mcol] in self.escapes:
                score += escape_w
                break
            mcol += 1

        mrow = row - 1
        while mrow >= 0:
            if [row, mcol] == self.throne:
                score += throne_w
                break
            if state[row][mcol] == -1:
                if mrow == row - 1:
                    score += adjacent_black_w
                else:
                    score += near_black_w
                break
            if state[row][mcol] == 1:
                if mrow == row - 1:
                    score += adjacent_white_w
                else:
                    score += near_white_w
                break
            if [row, mcol] in self.citadels:
                score += citadel_w
                break
            if [row, mcol] in self.escapes:
                score += escape_w
                break
            mrow -= 1

        mrow = row + 1
        while mrow < 9:
            if [row, mcol] == self.throne:
                score += throne_w
                break
            if state[row][mcol] == -1:
                if mrow == row + 1:
                    score += adjacent_black_w
                else:
                    score += near_black_w
                break
            if state[row][mcol] == 1:
                if mrow == row + 1:
                    score += adjacent_white_w
                else:
                    score += near_white_w
                break
            if [row, mcol] in self.citadels:
                score += citadel_w
                break
            if [row, mcol] in self.escapes:
                score += escape_w
                break
            mrow += 1

        return score