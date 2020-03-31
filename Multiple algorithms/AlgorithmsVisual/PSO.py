# -*- coding: utf-8 -*-

from Problem import Algorithm
import itertools
import numpy as np
import random

class PSO(Algorithm):
    def __init__(self,noIter,noParticles,individualSize,vmin,vmax,w,c1,c2,neghbourhoodSize):
        Algorithm.__init__(self,noIter,vmin,vmax,individualSize)
        self.__noParticles = noParticles
        self.__w = w
        self.__c1 = c1
        self.__c2 = c2
        self.__neighbourhoodSize = neghbourhoodSize
        self.__population = [ Particle(individualSize, vmin, vmax) for x in range(self.__noParticles) ]
        self.__allPermutations = list(itertools.permutations(range(self._min,self._max+1)))
        self.__neighborhoods=self.__selectNeighbors()
        
    def __selectNeighbors(self):
        #generates a list of neighbours for each particle
        #generate it based on position
        if (self.__neighbourhoodSize>len(self.__population)):
            self.__neighbourhoodSize=len(self.__population)
            
        neighbors=[]
        if self.__neighbourhoodSize == len(self.__population):
            for i in range(len(self.__population)):
                listPoz=list(range(0,len(self.__population)))
                random.shuffle(listPoz)
                neighbors.append(listPoz)
            return neighbors
        
        for i in range(len(self.__population)):
            localNeighbor=[]
            for j in range(self.__neighbourhoodSize):
                x=np.random.randint(0, len(self.__population)-1)
                while (x in localNeighbor):
                    x=np.random.randint(0, len(self.__population)-1)
                localNeighbor.append(x)
            neighbors.append(localNeighbor)
        return neighbors
            
    def __iteration(self,i):
        w = self.__w/(i+1)
        bestNeighbors=[]
        #determine the best neighbor for each particle
        for i in range(len(self.__population)):
            bestNeighbors.append(self.__neighborhoods[i][0])
            for neighbour in self.__neighborhoods[i]:
                if (self.__population[bestNeighbors[i]].fit() < self.__population[neighbour].fit()):
                    bestNeighbors[i]=neighbour     
        
        #update the velocity for each particle                    
        for i in range(len(self.__population)):
            for j in range(len(self.__population[0].velocity)):
                newVelocity = tuple([w * x for x in self.__population[i].velocity[j]])
                
                a = tuple(np.subtract(self.__population[bestNeighbors[i]].position[j],self.__population[i].position[j]))
                b = tuple([self.__c1*np.random.random()* x for x in a])            
                newVelocity = tuple(map(lambda x,y:x+y, newVelocity,b))
                
                c = tuple(np.subtract(self.__population[i].bestposition[j],self.__population[i].position[j]))
                d = tuple([self.__c2*np.random.random()*x for x in c])
                newVelocity = tuple(map(lambda x,y:x+y, newVelocity,d))
                
                self.__population[i].velocity[j]=newVelocity
                
        #update the position for each particle
        for i in range(len(self.__population)):
            newposition=[]
            for j in range(len(self.__population[0].velocity)):
                a = list(map(lambda x,y:x+y,self.__population[i].position[j],self.__population[i].velocity[j]))
                for el in a:
                    if el<self._min or el>self._max: #if it goes out of the search space, we keep it in place
                        a = self.__population[i].position[j]
                        self.__population[i].velocity[j]=tuple(0 for i in range(self._individualSize//2))
                        break
                newposition.append(tuple(a))
            self.__population[i].position=newposition
        return self.__population

    def runValidation(self):
        for i in range(self._iterations):           
            print(i)
            self.__population = self.__iteration(i)
            best = 0
            for i in range(1, len(self.__population)):
                if (self.__population[i].fit()<self.__population[best].fit()):
                    best = i
        #get best fitness from population
        best = 0
        for i in range(1, len(self.__population)):
            if (self.__population[i].fit()<self.__population[best].fit()):
                best = i
                
        fitnessOptim=self.__population[best].fit()
        print(self.__population[best].formSolution())
        return fitnessOptim
    
    def run(self,i):
        self.__iteration(i)
        #return best individual
        best = 0
        for i in range(1, len(self.__population)):
            if (self.__population[i].fit() < self.__population[best].fit()):
                best = i
        return self.__population[best].position
    
     
class Particle:
    def __init__(self, l, vmin, vmax):
        self._min=vmin
        self._max=vmax
        self._position = self._individual(l,vmin,vmax)
        self.evaluate()
        self.velocity = [ tuple(0 for i in range(l//2)) for i in range(l)]
        self._fitness = self.fit()
        
        #the memory of that particle
        self._bestposition=self._position.copy()
        self._bestFitness=self._fitness
    
    def _individual(self,length,vmin,vmax):
        '''
        Create a member of the population - an individual
         An individual is a list of all possible permutations of numbers from self._min to self._max
    
        vmin: the minimum possible value 
        vmax: the maximum possible value 
        '''
        listElements=range(vmin,vmax+1)
        individual = []
        while len(individual)<length:
            permutation = tuple(np.random.permutation(listElements).tolist())
            if permutation not in individual:
                individual.append(permutation)
        return individual
    
    def formSolution(self):
        matrix=[]
        matrixSize = len(self._position[0])        
        row=[]
        for i in range(matrixSize):
            for j in range(matrixSize):
                row.append(((int(round(self._position[i][j])), int(round(self._position[i+matrixSize][j])))))
            matrix.append(row)
            row=[]            
        return matrix
    
    def fit(self):
        """
        Determine the fitness of a particle. Lower is better.(min problem)
        """
        fitness=0
        matrix = self.formSolution()
        #check the columns
        matrixSize = len(matrix)
        for row in range(matrixSize):
            firstPosition=[]
            secondPosition=[]
            for column in range(matrixSize):
                element=matrix[row][column]
                firstPosition.append(element[0])
                secondPosition.append(element[1])
            for number in range (self._min,self._max+1):
                if number not in firstPosition:
                    fitness+=1
                if number not in secondPosition:
                    fitness+=1 
        #check that cells don't repet themselves
        flatten = lambda l: [item for sublist in l for item in sublist]
        flatMatrix = flatten(matrix)
        for cell in flatMatrix:
            if flatMatrix.count(cell)!=1:
                fitness+=1
        return fitness

    def evaluate(self):
        """ evaluates the particle """
        self._fitness = self.fit()

    @property
    def position(self):
        """ getter for position """
        return self._position

    @property
    def fitness(self):
        """ getter for fitness """
        return self._fitness

    @property
    def bestposition(self):
        """ getter for best position """
        return self._bestposition

    @property
    def bestFitness(self):
        """getter for best fitness """
        return self._bestFitness
    
    @position.setter
    def position(self, newPosition):
        self._position=newPosition.copy()
        # automatic evaluation of particle's fitness
        self.evaluate()
        # automatic update of particle's memory
        if (self._fitness<self._bestFitness):
            self._bestposition = self._position
            self._bestFitness  = self._fitness
            
    def __str__(self):
        return str(self._position)+str(self.velocity)
            
if __name__ == "__main__":
    problem = PSO(100,20,6,0,2,1.0,1,2.5,2)
    problem.runValidation()
    