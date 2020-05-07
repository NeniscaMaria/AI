import numpy as np
import matplotlib as mpl
import sys
class NeuralNetwork:
   
    def __init__(self, x, y,hidden):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1],hidden) 
        self.weights2   = np.random.rand(hidden,1)  
        print(self.weights1,self.weights2)  
        print()             
        self.y          = y
        self.output     = np.zeros(self.y.shape)
        self.loss       = []
        
    #activation function
    def __linear(self,x):
        return x
        
    def feedforward(self):
        self.layer1 = self.__linear(np.dot(self.input, self.weights1))
        self.output = self.__linear(np.dot(self.layer1, self.weights2))
        
    def backprop(self,l_rate):
        #same formula used in regression lab for updateParameters
        #compute derivative of weights
           d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output)/self.input.shape[0]))
           
           d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y -
                            self.output)/self.input.shape[0] ,
                            self.weights2.T)))
           #multiply derivative with learning rate and update the weights
           self.weights1 += l_rate * d_weights1
           self.weights2 += l_rate * d_weights2
           #error = realValue - outputOfNN : (self.y-self.output)**2
           np.seterr(all='raise')
           try:
               cost = sum((self.y - self.output)**2)/self.input.shape[0]
               print("cost ",cost)
           except FloatingPointError:
               cost = sys.maxsize
           self.loss.append(cost)

        