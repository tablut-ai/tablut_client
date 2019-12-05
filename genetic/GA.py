import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from search.negamax import Search
from game.game_obj import GameObj
from genotype import Genotype

def main():
    GA = Genotype()
                    
    white_weights, black_weights = GA.start()

if __name__ == '__main__': main()