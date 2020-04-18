# -*- coding: utf-8 -*-
from Data import Data
import random
class UI:
    def __init__(self):
        self.__data = self.__readData()
        self.__trainingData, self.__testingData = self.__split()
        #parameters of liniar function
        self.__b0 = 0
        self.__b1 = 0
        self.__b2 = 0
        self.__b3 = 0
        self.__b4 = 0
        self.__b5 = 0
        #learning rate should be some very small value
        self.__learningRate = 0.0001
        
    def __readData(self):
        data = []
        try:
            with open("bdate2.txt",'r') as f:
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
                            d = Data(a1,a2,a3,a4,a5,r)
                            data.append(d)                        
        except FileNotFoundError :
            print("Inexistent file : "+self.__filename)
        return data
    
    def __split(self):
        random.shuffle(self.__data)
        train_data = self.__data[:int((len(self.__data)+1)*.70)] #Remaining 70% to training set
        test_data = self.__data[int(len(self.__data)*.30+1):] #Splits 30% data to test set
        return train_data, test_data
    
    def __loss(self):
        #formula used:
        #E = (1/n)*(sum 0->n of (actualY-predictedY)^2)
        #predictedY = htheta(x) where htheta is the function we are looking for
        #mean squared error function
        sumSquares = 0
        for data in self.__trainingData:
            #1 difference between actual value of y (y1) and predicted value of y(y2)
            y1 = data.getResult()
            y2 = self.__b0 + self.__b1*data.getA1() + self.__b2*data.getA2() + self.__b3*data.getA3() + self.__b4*data.getA4() + self.__b5*data.getA5()
            difference = y1-y2
            #2 square de difference (y1-y2)^2
            square = difference**2
            sumSquares+=square
        
        #3 find the mean of squares for every value
        mean = sumSquares/len(self.__trainingData)
        return mean
    
    def __updateParameters(self):
        #derivative of loss function wrt to each variables
        #loss function: (1/n)*(sum 0->n of (actualY-predictedY)^2)
        #loss function: (1/n)*(sum 0->n of (result-htheta(x))^2)
        #derivative wrt variable j: (1/n)*(sum 0->n of 2*(actualY-predictedY)*(-xj))
        #derivative wrt to variable j:
        #(-2/n)*(sum 0->n of hj*(actualY-predictedY)
        sum0 = 0
        sum1 = 0
        sum2 = 0 
        sum3 = 0 
        sum4 = 0 
        sum5 = 0
        for data in self.__trainingData:
            actualY = data.getResult()
            predicted = self.__b0 + self.__b1*data.getA1() + self.__b2*data.getA2() + self.__b3*data.getA3() + self.__b4*data.getA4() + self.__b5*data.getA5()
            difference = (actualY - predicted)
            y0 = 1
            sum0+=difference*y0            
            sum1+=difference*data.getA1()            
            sum2+=difference*data.getA2()            
            sum3+=difference*data.getA3()            
            sum4+=difference*data.getA4()            
            sum5+=difference*data.getA5()
            
        derivative0 = sum0/len(self.__trainingData)*(-2)
        derivative1 = sum1/len(self.__trainingData)*(-2)
        derivative2 = sum2/len(self.__trainingData)*(-2)
        derivative3 = sum3/len(self.__trainingData)*(-2)
        derivative4 = sum4/len(self.__trainingData)*(-2)
        derivative5 = sum5/len(self.__trainingData)*(-2)
        
        self.__b0 = self.__b0 - self.__learningRate*derivative0
        self.__b1 = self.__b1 - self.__learningRate*derivative1
        self.__b2 = self.__b2 - self.__learningRate*derivative2
        self.__b3 = self.__b3 - self.__learningRate*derivative3
        self.__b4 = self.__b4 - self.__learningRate*derivative4
        self.__b5 = self.__b5 - self.__learningRate*derivative5
        
    def __test(self):
        #returns average error and maximum error in test data set
        maximum = 0
        sumSquares = 0
        for data in self.__testingData:
            #1 difference between actual value of y (y1) and predicted value of y(y2)
            y1 = data.getResult()
            y2 = self.__b0 + self.__b1*data.getA1() + self.__b2*data.getA2() + self.__b3*data.getA3() + self.__b4*data.getA4() + self.__b5*data.getA5()
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
        while self.__loss() >0.04:
            print(self.__loss())
            self.__updateParameters()
        print("Solution is: ")
        print("f(x) = ",self.__b0," + ",self.__b1,"*x1 + ",self.__b2,"*x2 + ",
              self.__b3,"*x3 + ",self.__b4,"*x4 + ",self.__b5,"*x5")
        print("Average error in test data: ",self.__test()[0])
        print('Maximum error: ',self.__test()[1])
    
def main():
    ui = UI()
    ui.run()
    
main()