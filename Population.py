import numpy as np
import random
from create_list import *
from Chromosome import *
from store_unique import *
from test3by3 import *



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
        self.solve, self.options = create_list2(2,2,False)
        self.sols = create_sols2(True)#twobytwo
        print "lists generated:/n"
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
    def re_innitialize(self):
        self.population = []
        for i in range(0, self.size,1):
            x = Chromosome(multiplications, self.solve ,self.sols)
            for j in range(0, i+1, 1):
                if j == i:
                    self.population.append(x)
                    break
                elif x.fitness < self.population[j].fitness:
                    self.population.insert(j,x)
                    break



if __name__ == "__main__":
    re_innit = False
    for number in range(0,10,1):
        multi = 7
        if re_innit == False:
            J =  Population(40,multi)
        if re_innit == True:
            J.re_innitialize()
        re_innit = False
        i = 0
        while not re_innit and i < 6000:
            for Chrom in J.population:
                Chrom.local_search()
                print Chrom.fitness
                if Chrom.stop == True:
                    tester = np.array(Chrom.encode_answer())
                    print tester
                    check = check_and_write(tester, '2by2_complete.h5',multi)
                    if check:
                        with open("2by2_complete.txt","a+") as f:
                            X = Chrom.find_X()
                            string = "A=\n %s \n  X = \n %s \n C= \n %s \n" % (Chrom.value, X ,np.dot(Chrom.value,X))
                            print string
                            f.write(string)
                            f.close()
                        #print "YAAAAAAY"
                        re_innit = True
                        break
                    else:
                        continue
            i = i + 1
            print i



