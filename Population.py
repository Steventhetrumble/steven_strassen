import numpy as np
import random
from create_list import *
from Chromosome import *



def weighted_random_choice(population):
    max = sum(chromosome.get_rank() for chromosome in population)
    pick = random.uniform(0, max)
    current = 0
    for chromosome in population:
        current += chromosome.get_rank()
        if current > pick:
            return chromosome


class Population():
    def __init__(self,size,multiplications):
        self.population = []
        self.multiplications = multiplications
        self.size = size
        self.solve, self.options = create_list()
        self.sols = create_sols()
        for i in range(0, self.size,1):
            x = Chromosome(multiplications, self.solve ,self.sols)
            for j in range(0, i+1, 1):
                if j == i:
                    self.population.append(x)
                    break
                elif x.fitness < self.population[j].fitness:
                    self.population.insert(j,x)
                    break
        #self.elite = self.population[self.size - 1]

    def update(self):
        for i in range(0, self.size,1):
            self.population[i].update_value()



if __name__ == "__main__":
    for number in range(0,10,1):
        J =  Population(40,7)
        re_innit = False
        i = 0
        while not re_innit and i < 60:
            for Chrom in J.population:
                Chrom.local_search()
                if Chrom.stop == True:
                    with open("strassen_save.txt","a+") as f:
                        X = Chrom.find_X()

                        string = "A=\n %s \n  X = \n %s \n C= \n %s \n" % (Chrom.value, X ,np.dot(Chrom.value,X))
                        print string
                        print Chrom.encode_answer()
                        f.write(string)
                        f.close()
                    #print "YAAAAAAY"
                    re_innit = True
                    break
            i = i + 1
            print i



