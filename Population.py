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
        self.solve = create_list()
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
    J =  Population(26,7)

    for i in range(0,1000,1):
        for item in J.population:
            item.local_search()
            print item.fitness



