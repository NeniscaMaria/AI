# -*- coding: utf-8 -*-
import numpy as np
import itertools
import copy
from Problem import Algorithm

class HillClimbing(Algorithm):
    def __init__(self,iterations,minimum,maximum,individualSize):
        Algorithm.__init__(self,iterations,minimum,maximum,individualSize)
        self.__allPermutations = list(itertools.permutations(range(self._min,self._max+1)))
        self.__individual = self.__initializeIndividual()
        
    def __generateAllPermutations(self,size):
        listElements=range(self._min,self._max+1)
        permutations = []
        while len(permutations)<size:
            permutation = tuple(np.random.permutation(listElements).tolist())
            if permutation not in permutations:
                permutations.append(permutation)
        return permutations
    
    def __initializeIndividual(self):
        population =  self._generatePopulation(self._individualSize)
        #select an individual from a population
        index = np.random.randint(0,len(population)-1)
        return population[index]
        
    
    def __getAllNeighbours(self):
        #function that generates all the neighrbours of self.__individual
        neighbours = []
        indexToChange = np.random.randint(0,self._individualSize-1)
        for permutation in self.__allPermutations:
            if permutation!=self.__individual[indexToChange]:
                newIndividual = copy.deepcopy(self.__individual)
                newIndividual[indexToChange]=permutation
                neighbours.append(newIndividual)
        return neighbours
    
    def __getBestNeighbour(self,neighbours):
        '''
        Parameters
        ----------
        neighbours : list of individuals
        Returns
        -------
        bestIndividual : tuple: (fitness,individual)

        '''
        #return the best neighbour form the
        #neighbourhood according to the fitness function
        fitnessAndIndividual = [ (self._fitness(x), x) for x in neighbours]
        sortedFitnessAndIndividual =  sorted(fitnessAndIndividual)
        bestIndividual = sortedFitnessAndIndividual[0]
        return bestIndividual
        
    def __iteration(self):
        '''
        an iteration
        '''
        neighbours = self.__getAllNeighbours()
        bestNeighbour = self.__getBestNeighbour(neighbours)
        if bestNeighbour[0] <= self._fitness(self.__individual):
           self.__individual = bestNeighbour[1]
        
    
    def run(self,i):
        #for i in range(self.__iterations):
        self.__iteration()
        return self.__individual
        
if __name__ == "__main__":
    problem = HillClimbing(10, 0, 3, 8)
    problem.run()