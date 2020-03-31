# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
import time
import numpy as np
from EA import EA
class AlgorithmValidation(QRunnable):
    def __init__(self):
        super(AlgorithmValidation,self).__init__()
        self.signals = ValidationSignals()
        
    def run(self):
        i = 0
        listOfFitnesses = []
        for i in range(30):
            #show progres
            self.signals.progress.emit(i)
            
            #generate paramteres
            probabilityMutation = np.random.random()
            probabilityCrossover = np.random.random()
            numberOfGenerations = 1000
            populationSize = 40
            sizeSymbolSet = np.random.randint(5,10)
            
            #run algorithm
            algorithmEA = EA(probabilityMutation, probabilityCrossover, populationSize, numberOfGenerations, 
                              0, sizeSymbolSet-1, sizeSymbolSet*2)
            
            listOfFitnesses.append(algorithmEA.runValidation())
        self.signals.finished.emit(listOfFitnesses)
        
   
        
    
class ValidationSignals(QObject):
    '''
    Defines the signals available from a RunningAlgorithm thread.

    Supported signals are:

    finished
        'list' the list of fitnesses
    
    progress
        `int` indicating progress

    '''
    finished = pyqtSignal(list)
    progress = pyqtSignal(int)