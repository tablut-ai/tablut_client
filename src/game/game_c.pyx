import numpy as np
cimport cython

def cresult(move):
    return _cresult(move)

cdef long [:,::1] state = np.array([
    [0, 0, 0, 4, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0], 
    [0, 0, 0, 0, 1, 0, 0, 0, 0], 
    [4, 0, 0, 0, 1, 0, 0, 0, 4], 
    [4, 4, 1, 1, 2, 1, 1, 4, 4], 
    [4, 0, 0, 0, 1, 4, 0, 0, 4], 
    [0, 0, 0, 0, 1, 0, 0, 0, 0], 
    [0, 0, 0, 0, 4, 0, 0, 0, 0], 
    [0, 0, 0, 4, 4, 4, 0, 0, 0]])

@cython.boundscheck(False)
@cython.wraparound(False) 
cdef void _cresult(long[:] move):
    cdef long p = state[move[0], move[1]]
    state[move[0], move[1]] = 0
    state[move[2], move[3]] = p