# -*- coding: utf-8 -*-
from Ant import Ant
import numpy as np

class ACO():
    def __init__(self,minimum,maximum,individualSize):
        self.min=minimum
        self.max=maximum
        self._individualSize = individualSize #individual = 2*n permutations
        print(self._individualSize)
        self.__permutations = self.__generate2Npermutations()
        
    def getSize(self):
        return self._individualSize 
    
    def getPermutations(self):
        return self.__permutations
    
    def getPosition(self,permutation):
        for i in range(self._individualSize):
            if self.__permutations[i]==permutation:
                return i
        return -1
        
    def __generate2Npermutations(self):
        
        listElements=list(range(self.min,self.max+1))
        p = []
        while len(p)<self._individualSize:
            permutation = tuple(np.random.permutation(listElements).tolist())
            if permutation not in p:
                p.append(permutation)  
        return p

    def _individual(self,length):
        
        individual = self.__permutations[np.random.randint(0,length)]
        return Ant(self,individual)
    
    def generatePopulation(self,size):
        """
        Create a number of individuals (i.e. a population).
        """
        return [ self._individual(self._individualSize) for x in range(size) ]
    
    