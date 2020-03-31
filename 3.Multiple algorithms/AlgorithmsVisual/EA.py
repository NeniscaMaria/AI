import numpy as np
from Problem import Algorithm
class EA(Algorithm):
    def __init__(self,mutation,crossover,popSize,gens,minimum,maximum, individualSize):
        Algorithm.__init__(self,gens,minimum,maximum,individualSize)
        self.__mutationProbability=mutation
        self.__crossoverProbability=crossover
        self.__populationSize=popSize
        self.__population = self._generatePopulation(self.__populationSize)
    
    def __mutate(self, individual): 
        '''
        individual:the individual to be mutated
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
        
        child1=[0]*self._individualSize
        child2=[0]*self._individualSize
        
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
        
        return [child1,child2]
            
    def __iteration(self):
        '''
        an iteration
        '''
        crossover = False
        while not crossover:
            i1=np.random.randint(0,len(self.__population)-1)
            i2=np.random.randint(0,len(self.__population)-1)
            #select parents
            if (i1!=i2):
                if self.__crossoverProbability > np.random.random():
                    crossover = True
                    #combine parents
                    parent1=self.__population[i1]
                    parent2=self.__population[i2]
                    children=self.__crossover(parent1,parent2)
                    
                    #mutate offsprings
                    child1=self.__mutate(children[0])
                    child2=self.__mutate(children[1])
                    
                    #select individuals for the next generation
                    fitnessList=[parent1,parent2,child1,child2]
                    fitnessList.sort(reverse=True,key=self._fitness)
                    self.__population[i1]=fitnessList[0]
                    self.__population[i2]=fitnessList[1]
                    
    def runValidation(self):
        for i in range(self._iterations):
            self.__iteration()
        fitnessAndIndividual = [ (self._fitness(x), x) for x in self.__population]
        sortedFitnessAndIndividual =  sorted(fitnessAndIndividual)
        bestIndividual = sortedFitnessAndIndividual[0]
        bestFitness = bestIndividual[0]
        return bestFitness
            
    def run(self,i):
        #function that runs forms a new generation
        self.__iteration()
        graded = [ (self._fitness(x), x) for x in self.__population]
        graded =  sorted(graded)
        result=graded[0]
        #fitnessOptim=result[0]
        individualOptim=result[1]
        return individualOptim
            

                
                
                


    

    



