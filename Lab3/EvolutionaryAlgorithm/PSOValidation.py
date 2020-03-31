# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
import time
import numpy as np
from PSO import PSO
import threading
class PSOValidation(QRunnable):
    def __init__(self):
        super(PSOValidation,self).__init__()
        self.signals = ValidationSignals()
        self.listOfFitnesses = []
        
    def __startProgram(self,i):
         
            
         noIterations = 100
         noParticles = 40
         
         sizeSymbolSet = np.random.randint(5,10)
         individualSize = 2*sizeSymbolSet
         vmin=0
         vmax=sizeSymbolSet-1
         w=np.random.random()*np.random.randint(1,4)
         c1=np.random.random()*np.random.randint(1,6)
         c2=np.random.random()*np.random.randint(1,6)
         
         neighbourhoodSize = np.random.randint(2,noParticles+1)      
         
         #run algorithm
         pso = PSO(noIterations,noParticles,individualSize,vmin,vmax,w,c1,c2,neighbourhoodSize)
         print("a")
         self.listOfFitnesses.append(pso.runValidation())
         
        
    def run(self):
        i = 0
        threads=[]
        for i in range(30):
            #show progres
            '''
            thread = threading.Thread(target=self.__startProgram,args=(i,))
            threads.append(thread)
            thread.start()
        i=0
        for t in threads:
            self.signals.progress.emit(i)
            print(i)
            i+=1
            t.join()
            '''
            self.signals.progress.emit(i)
            
            noIterations = 100
            noParticles = 40
            
            sizeSymbolSet = np.random.randint(5,10)
            individualSize = 2*sizeSymbolSet
            vmin=0
            vmax=sizeSymbolSet-1
            w=np.random.random()*np.random.randint(1,4)
            c1=np.random.random()*np.random.randint(1,6)
            c2=np.random.random()*np.random.randint(1,6)
            
            neighbourhoodSize = np.random.randint(2,noParticles+1)      
            
            #run algorithm
            pso = PSO(noIterations,noParticles,individualSize,vmin,vmax,w,c1,c2,neighbourhoodSize)
            print("a")
            self.listOfFitnesses.append(pso.runValidation())
        self.signals.finished.emit(self.listOfFitnesses)
        
   
        
    
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