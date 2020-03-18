# -*- coding: utf-8 -*-

from Matrix import Matrix
import copy

class Problem():
    def __init__(self,initial):
        self.__initialConfig = initial
        self.__finalConfig = None
        self.__initialState = copy.deepcopy(initial)
        self.__filename='finalState.txt'
        

    def expand(self, currentState):
        '''
        currentState = the board with a number of queens already put in place
        We want to add a new one
        We return a list with all possible positions that a new queen can be added 
        on that board
        '''
        myList = []
        currentConfig = currentState
        for row in range(currentConfig.getSize()):
            for newState in currentConfig.nextConfig(row):
                myList.append(newState)
        return myList
    
    def setFinalConfig(self,conf):
        self.__finalConfig=conf
    
    def getFinal(self):
        return self.__finalConfig
    
    def getRoot(self):
        return self.__initialState
    
    def heuristic(self,state):
        for i in range(0,self.__initialConfig.getSize()):
            for j in range (0,self.__initialConfig.getSize()):
                if state.getElement(i, j)!=self.__finalConfig.getElement(i, j):
                    return False
        return True
    