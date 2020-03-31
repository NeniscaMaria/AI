from Controller import Controller
from Problem import Problem
from Matrix import Matrix
import numpy as np

class UI:
    def __init__(self):
        try:
            n=int(input("Input the size of the board (implicit n=4)"))
        except :
            print("Invalid number. Size set to implict: 4.")
            n=4
        matrix = np.zeros((n,n),dtype=int).tolist()
        self.__initialState = Matrix(n,matrix)
        self.__problem = Problem(self.__initialState)
        self.__controller = Controller(self.__problem)
        
    def mainMenu(self):
        print("Please choose an option from below:")
        print("0.Exit")
        print("1.Solve with DFS")
        print("2.Solve with greedy")
    
    
    def runBFS(self):
        solution = self.__controller.DFS(self.__problem.getRoot())
        if solution==[]:
            print("No solution found")
        else:
            for s in solution:
                print(str(s))
        
    def runGBFS(self):
        solution = self.__controller.Greedy(self.__problem.getRoot())
        if solution==[]:
            print("No solution found")
        else:
            print(str(solution))
        
    def run(self):
        self.mainMenu()
        finished=False
        while not finished:
            try:
                choice=int(input(">>"))
                if choice==0:
                    finished=True
                elif choice==1:
                    self.runBFS()
                elif choice==2:
                    self.runGBFS()
            except ValueError:
                print("Invalid choice. Please choose one of 0,1 or 2")
        