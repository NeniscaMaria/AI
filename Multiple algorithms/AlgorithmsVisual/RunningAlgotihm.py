# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
import time


class RunningAlgorithm(QRunnable):
    def __init__(self,problem,iterations):
        super(RunningAlgorithm,self).__init__()
        self.__problem = problem
        self.__iterations = iterations
        self.signals = AlgorithmSignals()
        self.__stop = False
    
    def stop(self):
        self.__stop=True
        
    def run(self):
        i=0
        while i<self.__iterations and not self.__stop:
            print(i)
            bestIndividual = self.__problem.run(i)
            print(bestIndividual)
            self.signals.progress.emit(bestIndividual)
            time.sleep(0.5)
            i+=1
        self.signals.finished.emit()
    
class AlgorithmSignals(QObject):
    '''
    Defines the signals available from a RunningAlgorithm thread.

    Supported signals are:

    finished
        No data
    
    progress
        `list` indicating best individual up until now 

    '''
    finished = pyqtSignal()
    progress = pyqtSignal(list)