import numpy as np
from Item import item
import random
from create_list import *
import sys
import math

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

    def __init__(self, multiplications, list ,sols):
        self.multiplications = multiplications
        self.options = list
        self.solution = sols
        self.Chromosome = np.random.choice(self.options, multiplications)
        val = np.array(self.Chromosome[0].result)
        for i in range(1,multiplications,1):
            val = np.concatenate((val, self.Chromosome[i].result), axis = 1)
        self.value = val
        self.fitness = 0
        self.determine_fitness()
        self.stop = False
        self.encode = []

    def back_sub(self,upper_triangle):
        for i in range(self.multiplications - 1, -1, -1):
            if upper_triangle[i][i] != 1:
                upper_triangle[i][:] = upper_triangle[i][:] / upper_triangle[i][i]
            if any(upper_triangle[:][i]) != 0:
                for j in range(0, i, 1):
                    upper_triangle[j] = upper_triangle[j] - upper_triangle[i] * upper_triangle[j][i]

        return upper_triangle[:self.multiplications, self.multiplications:]

    def encode_answer(self):
        for item in self.Chromosome:
            self.encode.append([item.row1,item.row2])
        return self.encode


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
            self.stop = True

    def find_X(self):
        X = sort_matrix2(np.concatenate((self.value,self.solution),axis=1))
        X = self.back_sub(X)
        #X = X[0:self.multiplications,self.multiplications:]
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
        #print X
        index = self.check_X(X)
        choice = np.random.choice(index)
        old_fitness = self.fitness
        old_item = self.Chromosome[choice]
        search_range = int(self.fitness * len(self.options))
        upper_range = len(self.options) - search_range
        start = int(random.random()*upper_range)
        end = start + search_range
        for i in range(start,end,1):
            self.Chromosome[choice] = self.options[i]
            self.update_value()
            if self.fitness >= old_fitness:
                old_item = self.Chromosome[choice]
                old_fitness = self.fitness
                if self.stop == True:
                    break
                #break
        self.Chromosome[choice]= old_item
        self.fitness = old_fitness



if __name__ == "__main__":
    for i in range(0,10000,1):
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




