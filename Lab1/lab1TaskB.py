# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:33:12 2020

@author: nenis
application that creates and displays in graphs random distributions: normal, geometric and poisson
"""

import numpy as np
import matplotlib.pyplot as plt

def showMenu():
    print("\nPlease choose a distribution:")
    print("0.Exit")
    print("1.Normal")
    print("2.Geometric")
    print("3.Poisson")
    
def validateChoice(choice):
    return choice>=0 and choice<4

def normalDistribution():
    print("You chose normal")
    loc=np.random.random_sample() #random mean of distribution
    scale=np.random.random_sample() #random standard deviation
    size=np.random.randint(10,10000) #random size
    sample = np.random.normal(loc,scale,size)
    count, bins, ignored = plt.hist(sample, 30, density=True)  #generating the histogram
    
    plt.plot(bins, 1/(scale * np.sqrt(2 * np.pi)) *
             np.exp( - (bins - loc)**2 / (2 * scale**2) ),
             linewidth=2, color='r')
    plt.show()

def geometricDistribution():
    print("Your chose geometric")
    probability=np.random.random_sample()#random probability of success in a trial
    size = np.random.randint(10,1000) #how many numbers to generate
    sample = np.random.geometric(probability,size)
    plt.plot(sample,'ro')
    plt.show()
    plt.hist(sample, 30, density=True)
    plt.show()  
    
def poissonDistribution():
    print("Your choice is Poisson")
    size=np.random.randint(10,10000) #random size
    sample = np.random.poisson(np.random.randint(0,10), size)
    count,bins,ignored = plt.hist(sample, 30, density=True)
    plt.show()    
    plt.plot(sample,'ro')
    plt.show()
    
def main():
    finished=False
    while not finished:
        showMenu()
        try:
            choice=int(input("Your choice: "))
            if(validateChoice(choice)):
                if choice==0:
                    finished=True
                elif choice==1:
                    normalDistribution()
                elif choice==2:
                    geometricDistribution()
                elif choice==3:
                    poissonDistribution()
            else:
                print("Please choose a valid option.")
        except ValueError:
            print("The choice must be a number: 0, 1, or 2")
            
main()