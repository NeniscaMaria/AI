# -*- coding: utf-8 -*-
from NeuralNetwork import NeuralNetwork
import random
import numpy as np
import matplotlib as mpl
def linear(x):
    return x
class UI:
    def __init__(self):
        self.__data, self.__output = self.__readData()
        self.__trainingData, self.__testingData, self.__trainingOutput, self.__testingOutput = self.__split()
        #parameters of liniar function
        self.__b0 = 0
        self.__b1 = 0
        self.__b2 = 0
        self.__b3 = 0
        self.__b4 = 0
        self.__b5 = 0
        
    def __readData(self):
        data = []
        output = []
        try:
            with open("data.txt",'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line != "":
                        words = line.strip().split(" ")
                        if(words[-1]==''):
                            words.remove('')
                        if len(words) == 6:
                            a1=float(words[0].strip())
                            a2=float(words[1].strip())
                            a3=float(words[2].strip())
                            a4=float(words[3].strip())
                            a5=float(words[4].strip())
                            r = float(words[5].strip())
                            data.append([a1,a2,a3,a4,a5,1])      
                            output.append([r])
        except FileNotFoundError:
            print("Inexistent file : "+self.__filename)
        return np.array(data),np.array(output)
    
    def __split(self):
        train_data = self.__data[:int((len(self.__data)+1)*.70)] #Remaining 70% to training set
        test_data = self.__data[int(len(self.__data)*.30+1):] #Splits 30% data to test set
        
        train_out = self.__output[:int((len(self.__data)+1)*.70)] #Remaining 70% to training set
        test_out = self.__output[int(len(self.__data)*.30+1):] #Splits 30% data to test set
        
        return train_data, test_data, train_out, test_out
    def __test(self):
        #returns average error and maximum error in test data set
        maximum = 0
        sumSquares = 0
        for i in range(len(self.__testingData)):
            #1 difference between actual value of y (y1) and predicted value of y(y2)
            y1 = self.__testingOutput[i][0]
            data = self.__testingData[i]
            y2 = self.__b0 + self.__b1*data[0] + self.__b2*data[1] + self.__b3*data[2] + self.__b4*data[3] + self.__b5*data[4]
            difference = y1-y2
            if difference>maximum:
                maximum = difference
            #2 square de difference (y1-y2)^2
            square = difference**2
            sumSquares+=square
        
        #3 find the mean of squares for every value
        mean = sumSquares/len(self.__testingData)
        return mean,maximum
    
    def run(self):
        nn = NeuralNetwork(self.__trainingData,self.__trainingOutput,1)
        l_rate = 0.0001 #should be a bery small number if we want more iterations
        nn.loss=[]
        while len(nn.loss)==0 or nn.loss[-1]>0.0004 :
            nn.feedforward()
            nn.backprop(l_rate)
        
        #get parameters
        r=nn.weights2[0]
        self.__b0 = r
        self.__b1 = nn.weights1[0]*r
        self.__b2 = nn.weights1[1]*r 
        self.__b3 = nn.weights1[2]*r 
        self.__b4 = nn.weights1[3]*r 
        self.__b5 = nn.weights1[4]*r
        
        print("f(x) = ",self.__b0," + ",self.__b1,"*x1 + ",self.__b2,"*x2 + ",
              self.__b3,"*x3 + ",self.__b4,"*x4 + ",self.__b5,"*x5")
        print('Maximum error: ',self.__test()[1])
        print("Average error: ",self.__test()[0])
    

def main():
    ui = UI()
    ui.run()
    
main()