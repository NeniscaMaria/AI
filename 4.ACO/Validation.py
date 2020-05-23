# -*- coding: utf-8 -*-
from ACO import ACO
from ControllerACO import Controller
import random

class Validation:
    def __init__(self):
        pass
    
    def run(self):
        i = 0
        listOfFitnesses = []
        for i in range(30):
            #show progres
            print("Validation ",i,'/',30)
            minimum = 0
            maximum = random.randint(21,30)
            individualSize = (maximum)*2
            
            problem = ACO(minimum,maximum-1,individualSize)
            
            noEpoch = 30
            noAnts = 40
            alpha = random.random()+random.randint(0, 3)
            beta = random.random()+random.randint(0, 3)
            rho = random.random()
            q0 = random.random()
            pheromoneMatrix = [[1 for i in range(individualSize)]for j in range (individualSize)]
            
            controller = Controller(problem, noEpoch, noAnts, alpha, beta, rho, q0, pheromoneMatrix)
            fitness = controller.run()[1] 
            listOfFitnesses.append(fitness)
        return listOfFitnesses