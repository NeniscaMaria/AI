# -*- coding: utf-8 -*-

from MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from EA import EA
from HillClimbing import HillClimbing
import threading
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtCore import *
from RunningAlgotihm import RunningAlgorithm
from AlgorithmValidations import AlgorithmValidation
from PSO import PSO
from PSOValidation import PSOValidation
from ACO import ACO
from ControllerACO import Controller
from Ant import Ant

class UI (Ui_MainWindow):
    def __init__(self):
        #setup
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.__mainWindow)
        self.__setupButtons()
        self.__mainWindow.setWindowTitle("EA")
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        
        #attributes
        self.__problem = None
        self.__continueRunningAlgorithm = False
        self.__symbolset1 = None
        self.__symbolset2 = None
        self.__runningAlgorithm = None
        
        # plot attributes
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,parent=None)
        self.threadPool=QThreadPool()
        self.layoutPlot.addWidget(self.toolbar)
        self.layoutPlot.addWidget(self.canvas)
        
    def __setupButtons(self):
        self.runButton.setToolTip('Click to run algorithm')
        self.runButton.clicked.connect(self.startEA)
        self.runHillButton.clicked.connect(self.startHillClimbing)
        self.pushButton_2.clicked.connect(self.startPSO)
        self.stopButton.clicked.connect(self.stopAlgorithm)
        self.validationButton.clicked.connect(self.__runValidations)
        self.pushButton.clicked.connect(self.__runValidationsPSO)
        
    def __showMessage(self, message):
        msgBox = QMessageBox()
        QMessageBox.question(msgBox, 'Information', message, QMessageBox.Ok)
        msgBox.show()
            
    def stopAlgorithm(self):
        if self.__runningAlgorithm:
            self.__runningAlgorithm.signals.finished.emit()
            self.__runningAlgorithm.stop()
            self.__showMessage("Algorithm has stopped")
        
    def __validateProbability(self, prob):
        if prob<=0 or prob>1:
            raise TypeError("One of the probabilities is invalid.")
            
    def __validateInteger(self, integer):
        if integer<=0:
            raise TypeError("Invalid generations number or population size. Please input a non-negative number.")
        
    def __validateSymbolSet(self, symbolSet, size):
        symbolSet = symbolSet.split(" ")
        if len(symbolSet)>size:
            raise TypeError("A symbol text contains to many elements. Please be careful not to add any spaces at the end of your list.")
        for symbol in symbolSet:
            if symbolSet.count(symbol)!=1:
                raise TypeError("There are repeting symbols in one of the sets.")
        return symbolSet
    
    def __runSolution(self,numberOfGenerations):
        self.__runningAlgorithm = RunningAlgorithm(self.__problem, numberOfGenerations)
        self.__runningAlgorithm.signals.finished.connect(lambda:self.solutionLabel.setText("Final solution:"))#self.solutionLabel.setStyleSheet("QLabel { color : green; }"))
        self.__runningAlgorithm.signals.progress.connect(self.__displaySolution)
        self.threadPool.start(self.__runningAlgorithm)
    
    def __displaySolution(self, individual):
        self.bestSolutionUntilNowTextEdit.clear()
        solution = self.__problem.formSolution(individual)
        solutionFormatted = ''
        for row in solution:
            rowString=''
            for element in row:
                rowString+=('| (')
                rowString+=(str(self.__symbolset1[int(round(element[0]))]))
                rowString+=(',')
                rowString+=(str(self.__symbolset2[int(round(element[1]))]))
                rowString+=(') | ')
            rowString+=('\n')
            for i in range (10*len(row)):
                rowString+=('-')
            rowString+=('\n')
            solutionFormatted+=(rowString)
            
        self.bestSolutionUntilNowTextEdit.insertPlainText(solutionFormatted)
        
    def __drawPlot(self, data):
        self.progressBar.setVisible(False)
        #prepare data
        arr = np.array(data)
        m = np.mean(arr, axis=0)
        std = np.std(arr, axis=0)
        means = []
        stddev = []
        for i in range(30):
            means.append(m)
            stddev.append(std)
            
        # create an axis
        ax = self.figure.add_subplot(111)
        
        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data, 'r-')
        ax.plot(range(30), means, 'b:')
        ax.plot(range(30), stddev, 'g--') #green dashed line

        # refresh canvas
        self.canvas.draw()
        self.loadingLabel.setText("")
    
    def __displayProgress(self,algorithmNumber):
        self.progressBar.setValue(int(algorithmNumber*100/29))
        self.loadingLabel.setText('Loading.... ')
        
    def __runValidations(self):
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(100)
        validation = AlgorithmValidation()
        validation.signals.finished.connect(self.__drawPlot)
        validation.signals.progress.connect(self.__displayProgress)
        self.threadPool.start(validation)
        
    def __runValidationsPSO(self):
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(100)
        validation = PSOValidation()
        validation.signals.finished.connect(self.__drawPlot)
        validation.signals.progress.connect(self.__displayProgress)
        self.threadPool.start(validation)
    
    def startEA(self):
        try:
            self.solutionLabel.setText("Best solution until now:")
            self.solutionLabel.setStyleSheet("QLabel { color : black; }")
            probabilityMutation = float(self.mutationTextEdit.toPlainText())
            probabilityCrossover = float(self.crossoverTextEdit.toPlainText())
            numberOfGenerations = int(self.numberOfGenerationsTextEdit.toPlainText())
            populationSize = int(self.populationSizeTextEdit.toPlainText())
            sizeSymbolSet = int(self.symbolSetSizeTextEdit.toPlainText())
            symbolset1 = self.symbolSet1TextEdit.toPlainText()
            symbolset2 = self.symbolSet2TextEdit.toPlainText()
            
            #validations
            self.__validateProbability(probabilityMutation)
            self.__validateProbability(probabilityCrossover)
            self.__validateInteger(numberOfGenerations)
            self.__validateInteger(populationSize)
            self.__validateInteger(sizeSymbolSet)
            self.__symbolset1 = self.__validateSymbolSet(symbolset1,sizeSymbolSet)
            self.__symbolset2 = self.__validateSymbolSet(symbolset2,sizeSymbolSet)
            
            self.__problem = EA(probabilityMutation, probabilityCrossover, populationSize, numberOfGenerations, 
                              0, sizeSymbolSet-1, sizeSymbolSet*2)
            self.__continueRunningAlgorithm = True
            self.__runSolution(numberOfGenerations)            
        except ValueError:
            self.__showMessage("Invalid input. Please try again.")
        except TypeError as te:
            self.__showMessage(te)
        
    def startHillClimbing(self):
        try:
            self.solutionLabel.setText("Best solution until now:")
            self.solutionLabel.setStyleSheet("QLabel { color : black; }")
            numberOfIterations = int(self.iterationsTextField.toPlainText())
            sizeSymbolSet = int(self.sizeSymbolSetHillTextEdit.toPlainText())
            symbolset1 = self.symbolSet1HillTextEdit.toPlainText()
            symbolset2 = self.symbolSet2HillTextEdit.toPlainText()
            
            #validations
            self.__validateInteger(numberOfIterations)
            self.__validateInteger(sizeSymbolSet)
            self.__symbolset1 = self.__validateSymbolSet(symbolset1,sizeSymbolSet)
            self.__symbolset2 = self.__validateSymbolSet(symbolset2,sizeSymbolSet)
            
            self.__problem = HillClimbing(numberOfIterations, 0, sizeSymbolSet-1, sizeSymbolSet*2)
            self.__continueRunningAlgorithm = True
            self.__runSolution(numberOfIterations) 
            
        except ValueError:
            self.__showMessage("Invalid input. Please try again.")
        except TypeError as te:
            self.__showMessage(str(te))
    
    def startPSO(self):
        try:
            self.solutionLabel.setText("Best solution until now:")
            self.solutionLabel.setStyleSheet("QLabel { color : black; }")
            noIterations = int(self.psoIterationsText.toPlainText())
            noParticles = int(self.psoParticlesText.toPlainText())
            neighbouthoodSize=int(self.psoNeighbourhoodSizeText.toPlainText())
            
            sizeSymbolSet = int(self.psoSizeSSymbolSet.toPlainText())
            individualSize = 2*sizeSymbolSet
            vmin=0
            vmax=sizeSymbolSet-1
            
            symbolset1 = self.psoSymbolSet1.toPlainText()
            symbolset2 = self.psoSymbolSet1.toPlainText()
            
            w=float(self.psoWText.toPlainText())
            c1=float(self.psoC1Text.toPlainText())
            c2=float(self.psoC2Text.toPlainText())
            
            #validations
            self.__validateInteger(noIterations)
            self.__validateInteger(noParticles)
            self.__validateInteger(sizeSymbolSet)
            self.__validateInteger(neighbouthoodSize)
            self.__symbolset1 = self.__validateSymbolSet(symbolset1,sizeSymbolSet)
            self.__symbolset2 = self.__validateSymbolSet(symbolset2,sizeSymbolSet)
            
            self.__problem = PSO(noIterations,noParticles,individualSize,vmin,vmax,w,c1,c2,neighbouthoodSize)
            self.__continueRunningAlgorithm = True
            self.__runSolution(noIterations)            
        except ValueError:
            self.__showMessage("Invalid input. Please try again.")
        except TypeError as te:
            self.__showMessage(te)
    
        
    def run(self):
        self.__mainWindow.show()
        sys.exit(self.__app.exec_())
        
        
if __name__ == "__main__":
    ui=UI()
    ui.run()
        