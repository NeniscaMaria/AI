import numpy as np

class Algorithm:
    def __init__(self,iterations,minimum,maximum,individualSize):
        self._iterations = iterations
        self._min=minimum
        self._max=maximum
        self._individualSize = individualSize #individual = 2*n permutations
        
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
    
    def _fitness(self, individual):
        """
        Determine the fitness of an individual. Lower is better.(min problem)
        individual: the individual to evaluate
        we add 1 for each mistake
        """
        fitness=0
        matrix = self.formSolution(individual)
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
    
    def _generatePopulation(self,size):
        """
        Create a number of individuals (i.e. a population).
        """
        return [ self._individual(self._individualSize) for x in range(size) ]
    
    def _individual(self,length):
        '''
        Create a member of the population - an individual
         An individual is a list of all possible permutations of numbers from self._min to self._max
    
        vmin: the minimum possible value 
        vmax: the maximum possible value 
        '''
        listElements=range(self._min,self._max+1)
        individual = []
        while len(individual)<self._individualSize:
            permutation = tuple(np.random.permutation(listElements).tolist())
            if permutation not in individual:
                individual.append(permutation)
        return individual