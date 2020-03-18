import numpy as np
import math

class Problem:
    def __init__(self,mutation,crossover,popSize,gens,minimum,maximum, individualSize):
        self.__iterations = gens
        self.__mutationProbability=mutation
        self.__crossoverProbability=crossover
        self.__populationSize=popSize
        self.__min=minimum
        self.__max=maximum
        self.__individualSize = individualSize #individual = 2*n permutations
        self.__population = self.__generatePopulation()
        
    def __individual(self,length, vmin, vmax):
        '''
        Create a member of the population - an individual
         An individual is a list of all possible permutations of numbers from self.__min to self.__max
    
        vmin: the minimum possible value 
        vmax: the maximum possible value 
        '''
        listElements=range(self.__min,self.__max+1)
        individual = []
        while len(individual)<self.__individualSize:
            permutation = tuple(np.random.permutation(listElements).tolist())
            if permutation not in individual:
                individual.append(permutation)
        return individual
       
    def __generatePopulation(self):
        """
        Create a number of individuals (i.e. a population).
        """
        return [ self.__individual(self.__individualSize, self.__min, self.__max) for x in range(self.__populationSize) ]
    
    def __mutate(self, individual): 
        '''
        Performs a mutation on an individual with the probability of pM.
        If the event will take place, at a random position a new value will be
        generated in the interval [vmin, vmax]
    
        individual:the individual to be mutated
        pM: the probability the mutation to occure
        vmin: the minimum possible value 
        vmax: the maximum possible value
        
        randomly select 2 genes and swap them
        '''
        if self.__mutationProbability > np.random.random():
                pos1 = np.random.randint(0,len(individual)-1)
                pos2 = np.random.randint(0,len(individual)-1)
                individual[pos1],individual[pos2]=individual[pos2],individual[pos1]
        return individual
    
    def __crossover(self, parent1, parent2):
        '''
        crossover between 2 parents
        '''
        print("Parent 1: ",parent1)
        print("Parent 2: ", parent2)
        
        child1=[0]*self.__individualSize
        child2=[0]*self.__individualSize
        
        #making cut in parents
        pos1 = np.random.randint(0,len(parent1)-1)
        pos2 = np.random.randint(0,len(parent1)-1)
        if pos1>pos2:
            pos1,pos2 = pos2,pos1
            
        for i in range (pos1,pos2+1):
            child1[i]=parent1[i]
            child2[i]=parent2[i]
        
        pos2+=1
        nextPosInParent=pos2
        nextPosInChild=pos2
        while nextPosInParent<len(parent2) and child1.count(0)!=0:
            nextGene = parent2[nextPosInParent]
            if nextGene not in child1:
                child1[nextPosInChild] = nextGene
                nextPosInChild+=1
                if nextPosInChild==len(parent2):
                    nextPosInChild=0
            nextPosInParent+=1
            if nextPosInParent==len(parent2):
                nextPosInParent=0
            
                
        print("Child 1: ",child1)
                
        nextPosInParent=pos2
        nextPosInChild=pos2
        while nextPosInParent<len(parent1) and child2.count(0)!=0:
            nextGene = parent1[nextPosInParent]
            if nextGene not in child2:
                child2[nextPosInChild] = nextGene
                nextPosInChild+=1
                if nextPosInChild==len(parent1):
                    nextPosInChild=0
            nextPosInParent+=1 
            if nextPosInParent==len(parent1):
                nextPosInParent=0
                
        print("Child2: ",child2)
        
        return [child1,child2]
    
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
        
    
    def __fitness(self, individual):
        """
        Determine the fitness of an individual. Lower is better.(min problem)
        For this problem we have the Rastrigin function
        
        individual: the individual to evaluate
        we add 1 for each mistake
        if fitness=0 => perfect solution
        """
        fitness=0
        matrix = self.formSolution(individual)
        #check the columns
        matrixSize = len(matrix)
        for column in range(matrixSize):
            firstPosition=[]
            secondPosition=[]
            for row in range(matrixSize):
                element=matrix[row][column]
                firstPosition.append(element[0])
                secondPosition.append(element[1])
            for number in range (self.__min,self.__max+1):
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
            
    def __iteration(self):
        '''
        an iteration
        '''
        i1=np.random.randint(0,len(self.__population)-1)
        i2=np.random.randint(0,len(self.__population)-1)
        #select parents
        #sort pop based on fitness function
        #combine the 2 best parents
        if (i1!=i2):
            #combine parents
            parent1=self.__population[i1]
            parent2=self.__population[i2]
            children=self.__crossover(parent1,parent2)
            
            #mutate offsprings
            child1=self.__mutate(children[0])
            child2=self.__mutate(children[1])
            
            #select individuals for the next generation
            fitnessList=[parent1,parent2,child1,child2]
            fitnessList.sort(reverse=True,key=self.__fitness)
            self.__population[i1]=fitnessList[0]
            self.__population[i2]=fitnessList[1]
    
    def run(self):
        print("Initial population:")
        for el in self.__population:
            print(el)
        for i in range(self.__iterations):
            self.__iteration()
    
        #print the best individual
        graded = [ (self.__fitness(x), x) for x in self.__population]
        graded =  sorted(graded)
        result=graded[0]
        #fitnessOptim=result[0]
        individualOptim=result[1]
        print('Result: The best solution after ',self.__iterations,' iterations is:')
        solution = self.formSolution(individualOptim)
        for row in solution:
            print(row)
        return individualOptim
            
            
if __name__ == "__main__":
    problem = Problem(0.8,0.8,3,10,1,3,6)
    problem.run()
                
                
                


    

    



