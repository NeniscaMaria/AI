# -*- coding: utf-8 -*-
from ACO import ACO
from ControllerACO import Controller
from Validation import Validation
from matplotlib import pyplot as plt
import numpy as np

def printMenu():
    print("0.Exit")
    print("1.Run ACO.")
    print("2.Run validation")
    
def runValidation():
    validation = Validation()
    data = validation.run()
    #prepare data
    arr = np.array(data)
    m = np.mean(arr, axis=0)
    std = np.std(arr, axis=0)
    means = []
    stddev = []
    for i in range(30):
        means.append(m)
        stddev.append(std)
        
    
    plt.plot(data, 'r-')
    plt.plot(range(30), means, 'b:')
    plt.plot(range(30), stddev, 'g--') #green dashed line
    plt.show()

def main():
    finished = False
    while not finished:
        try:
            printMenu()
            choice = int(input(">>"))
            if choice==0:
                finished = True
            elif choice == 1:
                minimum = 0
                maximum = int(input("How many numbers do you wish to permute? "))
                individualSize = (maximum)*2
            
                problem = ACO(minimum,maximum-1,individualSize)
                
                noEpoch = int(input("Number of eras: "))
                noAnts = int(input("Number of ants: "))
                if(noAnts>individualSize):
                    raise ValueError("Number of ants must be at most 2*number of numbers you wish to permute.")
                alpha = float(input("Trail importance(alpha): "))
                beta = float(input("Visibility importance(beta): "))
                rho = float(input("Pheromone degradation(0<=rho<=1): "))
                if rho<0 or rho>1:
                    raise ValueError("Rho must be >=0 and <=1")
                q0 = float(input("Random proportional rule(0<=q0<=1): "))
                if q0<0 or q0>1:
                    raise ValueError("q0 must be >=0 and <=1")
                pheromoneMatrix = [[1 for i in range(individualSize)]for j in range (individualSize)]
                
                controller = Controller(problem, noEpoch, noAnts, alpha, beta, rho, q0, pheromoneMatrix)
                solution = controller.run()[0] 
                print("Solution:")
                for row in solution.formSolution(solution.getIndividual()):
                    print(row)
            elif choice == 2:
                runValidation()                
            else:
                print("Invalid choice. Please try again.")   
        except ValueError as ve:
            print(ve)
            
main()