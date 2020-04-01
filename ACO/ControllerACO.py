# -*- coding: utf-8 -*-

class Controller:
    def __init__(self,problem,noEpoch,noAnts,alpha,beta,rho,q0,pheromoneMatrix):
        self.__problem = problem
        self.__noEpoch = noEpoch
        self.__noAnts = noAnts
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho
        self.__q0 = q0
        
        self.__population = []#problem._generatePopulation(noAnts) 
        self.__pheromoneMatrix = pheromoneMatrix
        
    def iteration(self):
        #initialize population:
        self.__population = self.__problem.generatePopulation(self.__noAnts)
        
        for i in range(self.__problem.getSize()):
            for ant in self.__population:
                ant.update(self.__pheromoneMatrix, self.__q0,self.__alpha,self.__beta)
                
        #local change of pheromone trail      
        t = [1.0 / (self.__population[i].evaluate()+1) for i in range(self.__noAnts)]
        
        for i in range(self.__problem.getSize()):
            for j in range(self.__problem.getSize()):
                self.__pheromoneMatrix[i][j] = (1-self.__rho)*self.__pheromoneMatrix[i][j]
        
        for i in range(self.__noAnts):
            for j in range(self.__problem.getSize()-1):
                x = self.__problem.getPosition(self.__population[i].getIndividual()[j])
                y = self.__problem.getPosition(self.__population[i].getIndividual()[j+1])
                self.__pheromoneMatrix[x][y] = self.__pheromoneMatrix[i][j] + t[i]
                
        fitness = [[self.__population[i].evaluate(),i] for i in range(self.__noAnts)]
        fitness = min(fitness)
        return self.__population[fitness[1]]
    
    def run(self):
        solution=None
        bestAnt = None
        for i in range(self.__noEpoch):
            print(i,"/",self.__noEpoch)
            solution = self.iteration()
            if bestAnt == None:
                bestAnt = solution
            if solution.evaluate()<bestAnt.evaluate():
                bestAnt = solution
        return solution
        
        