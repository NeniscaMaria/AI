# -*- coding: utf-8 -*-
from random import *
class Ant:
    def __init__(self,problem,individual):
        self.__problem = problem
        self.__individual = [individual]
        self.__nextPoz = 1
        
    def getIndividual(self):
        return self.__individual
        
    def evaluate(self):
        """
        Determine the fitness of an individual. Lower is better.(min problem)
        individual: the individual to evaluate
        we add 1 for each mistake
        """
        fitness=0
        matrix = self.formSolution(self.__individual)
        #check the columns
        matrixSize = len(matrix)
        for row in range(matrixSize):
            firstPosition=[]
            secondPosition=[]
            for column in range(matrixSize):
                element=matrix[row][column]
                firstPosition.append(element[0])
                secondPosition.append(element[1])
            for number in range (self.__problem.min,self.__problem.max+1):
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
    
    def formSolution(self, individual):
        matrix=[]
        matrixSize = len(individual[0])
        row=[]
        for i in range(matrixSize):
            for j in range(matrixSize):
                row.append(((individual[i][j], individual[i+matrixSize][j])))
            matrix.append(row)
            row=[]
            
        return matrix
    
    def __distMove(self,move):
        if(self.__nextPoz == self.__problem.getSize()):
            return 0
        
        #compute manhattan distance
        distance = 0
        for i in range(len(move)):
            distance+=abs(move[i]-self.__individual[self.__nextPoz-1][i])
        return distance
    
    def __nextMoves(self,pheromoneMatrix,q0):
        #generate next moves
        moves=[]
        for el in self.__problem.getPermutations():
            if el not in self.__individual:
                moves.append(el)
        return moves
                            
    def update(self,pheromoneMatrix,q0,alpha,beta):
        #visibility list
        visibility = [0 for i in range(self.__problem.getSize())]
        
        nextMoves = self.__nextMoves(pheromoneMatrix,q0)
        if(len(nextMoves)==0): #no posibility of update
            return False
        
        #compute visibility
        for i in range(len(nextMoves)):
            visibility[i] = self.__distMove(nextMoves[i])
        
        #position of last added permutation in the list of permutations
        position = self.__problem.getPosition(self.__individual[-1])
        #compute product
        visibility =[(visibility[i]**beta)*(pheromoneMatrix[position][i]**alpha) for i in range(len(visibility))]
        
        if random()<q0:
            #we add the best permutation
            m = [[i,visibility[i]] for i in range(len(visibility))]
            m = max(m,key = lambda a:a[1])
            self.__individual.append(nextMoves[m[0]])
            self.__nextPoz+=1
        else:
            s = sum(visibility)
            if(s==0):
                return choice(nextMoves)
            visibility = [visibility[i]/s for i in range(len(visibility))]
            visibility = [sum(visibility[0:i+1]) for i in range(len(visibility))]
            r = random()
            i=0
            while(r>visibility[i]):
                i+=1
            self.__individual.append(nextMoves[i])
            self.__nextPoz += 1
        return True
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        