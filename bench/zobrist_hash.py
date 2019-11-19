import sys, os, timeit, cProfile
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

def main():
    setup = "\
from random import randrange \n\
import numpy as np \n\
from search.zobrist_hash import ZobristHash \n\
zh = ZobristHash() \n\
state = [ \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0,-1], \n\
    [-1, -1, 1, 1, 2, 1, 1, -1, -1], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0, -1], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0]] \n"

    fn = "print(zh.compute(state))"

    print("====== Benchmark zorbist hash =====")
    print(avg_time(fn, setup, 1))

    print("====== All benchmark completed! =====")

def avg_time(stm, setup, n):
    return str(timeit.timeit(stm, setup=setup, number=n) / n * 1e6) + " us"

if __name__ == '__main__': main()