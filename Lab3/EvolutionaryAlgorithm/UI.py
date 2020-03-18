# -*- coding: utf-8 -*-

from MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from Problem import Problem

class UI (Ui_MainWindow):
    def __init__(self):
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__mainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.__mainWindow)
        self.__setupButtons()
        self.__mainWindow.setWindowTitle("EA")
        self.__problem = None
        
    def __setupButtons(self):
        self.runButton.setToolTip('Click to run algorithm')
        self.runButton.clicked.connect(self.startAlgorithm)
        
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
    
    def __displaySolution(self, individual, symbolSet1, symbolSet2):
        solution = self.__problem.formSolution(individual)
        solutionFormatted = ''
        for row in solution:
            rowString=''
            for element in row:
                rowString+=('| (')
                rowString+=(str(symbolSet1[element[0]]))
                rowString+=(',')
                rowString+=(str(symbolSet2[element[1]]))
                rowString+=(') | ')
            rowString+=('\n')
            for i in range (10*len(row)):
                rowString+=('-')
            rowString+=('\n')
            solutionFormatted+=(rowString)
            
        self.bestSolutionUntilNowTextEdit.insertPlainText(solutionFormatted)
        
    
    def startAlgorithm(self):
        try:
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
            symbolset1 = self.__validateSymbolSet(symbolset1,sizeSymbolSet)
            symbolset2 = self.__validateSymbolSet(symbolset2,sizeSymbolSet)
            print(probabilityMutation,probabilityCrossover,numberOfGenerations,populationSize,sizeSymbolSet,symbolset1, symbolset2)
            
            self.__problem = Problem(probabilityMutation, probabilityCrossover, populationSize, numberOfGenerations, 
                              0, sizeSymbolSet-1, sizeSymbolSet*2)
            
            bestIndividual = self.__problem.run()
            
            self.__displaySolution(bestIndividual,symbolset1,symbolset2)           
        except ValueError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Invalid input. Please try again.")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.show()
        except TypeError as te:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(te)
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.show()
        
        
        
    def run(self):
        self.__mainWindow.show()
        sys.exit(self.__app.exec_())
        
        
if __name__ == "__main__":
    ui=UI()
    ui.run()
        