import numpy as np
from Item import item
import random
from create_list import *
import sys
from collections import Counter, defaultdict

def duplicates(lst):
    cnt= Counter(lst)
    return [key for key in cnt.keys() if cnt[key]> 1]

def indices(lst, items= None):
    items, ind= set(lst) if items is None else items, defaultdict(list)
    for i, v in enumerate(lst):
        if v in items: ind[v].append(i)
    return ind

def sort_matrix2(matrix):
    col_label_list = set(range(0,len(matrix[0])))
    rows_left = set(range(0,len(matrix)))
    new_row_list = []
    for c in col_label_list:
        rows_with_nonzero = [r for r in rows_left if matrix[r][c] != 0 ]
        if rows_with_nonzero != []:
            pivot = rows_with_nonzero[0]
            rows_left.remove(pivot)
            new_row_list.append(matrix[pivot])
            for r in rows_with_nonzero[1:]:
                multiplier = matrix[r][c]/matrix[pivot][c]
                matrix[r]=[i - j*multiplier for i, j in zip(matrix[r], matrix[pivot])]

    return np.array(new_row_list)

class Chromosome():

    def __init__(self, multiplications):
        self.multiplications = multiplications
        self.options = create_list()
        self.solution = create_sols()
        self.Chromosome = np.random.choice(self.options, multiplications)
        val = np.array(self.Chromosome[0].result)
        for i in range(1,multiplications,1):
            val = np.concatenate((val, self.Chromosome[i].result), axis = 1)
        self.value = val
        self.fitness = 0
        self.determine_fitness()


    def update_value(self):
        val = np.array(self.Chromosome[0].result)
        for i in range(1, self.multiplications, 1):
            val = np.concatenate((val, self.Chromosome[i].result), axis=1)
        self.value = val
        self.determine_fitness()

    def determine_fitness(self):
        #self.partition = np.concatenate((self.value, self.solution), axis=1)

        solution = self.solution
        a = np.dot(self.value, self.value.T)
        b = np.linalg.pinv(a)
        c = np.dot(self.value.T, b)
        d = np.dot(self.value.T, solution)
        e = np.dot(c.T, d)
        f = np.subtract(e, solution)
        g = np.dot(f, f.T)
        h = np.trace(g)
        i = 1 / (1 + h)
        self.fitness = i
        if self.fitness == 1:
            print self.Chromosome
            print "YAAAAAAY"
            sys.exit()

    def find_X(self):
        X = sort_matrix2(np.concatenate((self.value,self.solution),axis=1))
        X = X[0:self.multiplications,self.multiplications:]
        return X

    def check_X(self, X):
        search_index = []
        for row in range(0,len(X)):
            if X[row].any() == 0:
                search_index.append(row)

            Z , ind = np.unique(X,return_index=True,axis =0)
            try:
                search_index.append(random.sample(set(np.arange(self.multiplications)) - set(ind)))
            except:
                search_index.append(random.choice(np.arange(self.multiplications)))



        return search_index

    def local_search(self):
        X = self.find_X()
        print X
        index = self.check_X(X)
        print index
        choice = np.random.choice(index)
        print choice
        old_fitness = self.fitness
        old_item = self.Chromosome[choice]

        print len(self.solution)
        for i in range(0,len(self.options),1):
            self.Chromosome[choice] = self.options[i]
            self.update_value()
            if self.fitness > old_fitness:
                old_item = self.Chromosome[choice]
                old_fitness = self.fitness
                break
        self.Chromosome[choice]= old_item
        self.fitness = old_fitness



if __name__ == "__main__":
    for i in range(0,100,1):
        new_Chrom = Chromosome(7)
        print new_Chrom.value
        print new_Chrom.fitness
        print new_Chrom.find_X()
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

        for i in range(0,40,1):
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            new_Chrom.local_search()
            print new_Chrom.value
            print new_Chrom.fitness




