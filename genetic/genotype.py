from random import randint, randrange, uniform, seed

class Genotype:
    def __init__(self, N = 100, n_offsprings = 2, n_genes = 11, mutation_prob = 1, 
                    genes_dict ={   0 : "escape_w " ,
                                    1 : "citadel_w" ,
                                    2 : "throne_w",
                                    3 : "near_white_w",
                                    4 : "adjacent_white_w",
                                    5 : "near_black_w" ,
                                    6 : "adjacent_black_w" ,
                                    7 : "material_w" ,
                                    8 : "king_pos_w" ,
                                    9 : "white_w" ,
                                    10 :"black_w" },

                    genes_bounds = {"escape_w" : (10,100),
                                "citadel_w" : (-20,10),
                                "throne_w" : (-20,10),
                                "near_white_w" : (-20,10),
                                "adjacent_white_w" : (-20,10),
                                "near_black_w" : (-20,10),
                                "adjacent_black_w" : (-20,10),
                                "material_w" : (1,10),
                                "king_pos_w" : (1,10),
                                "white_w" : (1,11),
                                "black_w" : (1,11)
                    }):

        self.N = N
        self.population = list()
        self.n_offsprings = n_offsprings
        self.n_genes = n_genes
        self.genes_bounds = genes_bounds
        self.mutation_prob = mutation_prob
        self.genes_dict = genes_dict


    def initialize_population(self):
        for i in range(self.N):
            escape_w = randrange(self.genes_bounds["escape_w"][0], self.genes_bounds["escape_w"][1])
            citadel_w = randrange(self.genes_bounds["citadel_w"][0], self.genes_bounds["citadel_w"][1])
            throne_w = randrange(self.genes_bounds["throne_w"][0], self.genes_bounds["throne_w"][1])
            near_white_w = randrange(self.genes_bounds["near_white_w"][0], self.genes_bounds["near_white_w"][1])
            adjacent_white_w = randrange(self.genes_bounds["adjacent_white_w"][0], self.genes_bounds["adjacent_white_w"][1])
            near_black_w = randrange(self.genes_bounds["near_black_w"][0], self.genes_bounds["near_black_w"][1])
            adjacent_black_w = randrange(self.genes_bounds["adjacent_black_w"][0], self.genes_bounds["adjacent_black_w"][1])
            material_w = randrange(self.genes_bounds["material_w"][0], self.genes_bounds["material_w"][1])
            king_pos_w = randrange(self.genes_bounds["king_pos_w"][0], self.genes_bounds["king_pos_w"][1])
            white_w = 0.1 * randrange(self.genes_bounds["white_w"][0], self.genes_bounds["white_w"][1])
            black_w = 0.1 * randrange(self.genes_bounds["black_w"][0], self.genes_bounds["black_w"][1])

            agent = [escape_w, 
                    citadel_w, 
                    throne_w, 
                    near_white_w, 
                    adjacent_white_w,
                    near_black_w,
                    adjacent_black_w,
                    material_w,
                    king_pos_w,
                    white_w,
                    black_w]

            self.population.append(agent)


    def two_point_cross_over(self, parent_1, parent_2):
        #p1 = randrange(self.n_genes)
        #p2 = randrange(self.n_genes)
        p1, p2 = 3,7

        offspring_1 = parent_1[:p1] + parent_2[p1:p2] + parent_1[p2:]
        offspring_2 = parent_2[:p1] + parent_1[p1:p2] + parent_2[p2:]

        self.non_uniform_mutation(offspring_1)
        self.non_uniform_mutation(offspring_2)

        return offspring_1, offspring_2


    def non_uniform_mutation(self, offspring):
            #la mutation_prob va fatta calare via via che si va avanti con le generazioni, 
            # per avvicinarci sempre più ai pesi ottimali
        if uniform(0,1) <= self.mutation_prob:
            gene_number = randrange(0, self.n_genes)
            mutated_gene = self.genes_dict[gene_number]
            print(mutated_gene)
            offspring[gene_number] = randrange(self.genes_bounds[mutated_gene][0], self.genes_bounds[mutated_gene][1])

    def fitness_fn(self):
        pass
        #Mi serve fight.py per contare il numero di vittorie
    
    def new_population(self):
        #da decidere il metodo di ripopoamento che più si addice 
        pass