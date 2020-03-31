# -*- coding: utf-8 -*-

import random

class Controller:
    def __init__(self,problem):
        self.__problem=problem
        
    def orderStates(self):
        pass
    
    def DFS(self, root):
        q = [root]
        solution=[]
        while len(q) > 0 :
            currentState = q.pop(0)
            if currentState.checkOnes():
                solution.append(currentState)
            q = q + self.__problem.expand(currentState)
        return solution
    
    def Greedy(self, start):
        self.__problem.setFinalConfig(self.DFS(start)[0])
        found = False
        visited = []
        toVisit = [start] # FIFO sorted list (priority queue)
        while toVisit!=[] and not found:
            if toVisit == []:
                return False
            node = toVisit.pop()
            if node == self.__problem.getFinal():
                return node
            aux = []
            for child in self.__problem.expand(node):
                if child not in visited:
                    aux.append(child)
            #sorting the priority queue according to the heuristic
            aux = [ [x, self.__problem.heuristic(x)] for x in aux]
            aux.sort(key=lambda x:x[1])
            aux = [x[0] for x in aux]
            toVisit = aux[:] + toVisit 
        return found
    
    def greedy2(self,root):
        found = False
        sol = []
        while not found:
            if sol!=[]:
                if sol.checkOnes():
                    found=True
                e=self.__problem.expand(sol)
                i=random.randint(0, len(e)-1)
                sol=e[i]
            else:
                e=self.__problem.expand(root)
                i=random.randint(0, len(e)-1)
                sol=e[i]
        return sol