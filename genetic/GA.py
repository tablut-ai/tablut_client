import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from search.negamax import Search
from game.game_obj import GameObj
from genotype import Genotype

def main():
    timeout = 59.5
    N = 4 
    tournament_size = 2
    number_of_generations = 3
    mutation_prob = 0.05 
    GA = Genotype(N = N, timeout = timeout, tourn_size = tournament_size, 
                    max_generation = number_of_generations, mutation_prob = mutation_prob)
                    
    white_weights, black_weights = GA.start()

if __name__ == '__main__': main()