# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 15:54:46 2020

@author: nenis
"""
from sudoku import Sudoku
from geometricForms import GeometricForms
from cryptoarithmeticGame import CryptoarithmeticGame

def showMenu():
    print("\nPlease choose one from below:")
    print("0.Exit")
    print("1.Sudoku")
    print("2.Cryptarithmetic game")
    print("3.Geometric forms")
    
def sudoku():
    print("Welcome to Sudoku!")
    finished =False
    while not finished:
        try:
            trials = int(input("Please insert the number of trials."))
            if trials==0:
                print("Please insert a non-negative number of trials.")
            else:
                size = int(input("Please enter the size of the board: "))
                if size == 0:
                    print("Please choose a non-negative size.")
                else:
                    game = Sudoku(size,trials)
                    game.start()
                    finished = True
        except ValueError:
            print("Please insert a number.")
    
def cryptoarithmeticGame():
    print("Welcome to the Cryptoarithmetic Game!")
    try:
        trials = int(input("Please enter the number of trials:" ))
        if trials == 0:
            print("Please insert a non-negative number of trials.")
        else:
            game = CryptoarithmeticGame(trials)
            game.start()
    except ValueError:
        print("Please input a non-negative number.")
    
def geometricForms():
    print("Welcome to Geometric Forms!")
    try:
        trials = int(input("Please enter the number of trials:" ))
        if trials == 0:
            print("Please insert a non-negative number of trials.")
        else:
            game = GeometricForms(trials)
            game.start()
    except ValueError:
        print("Please input a non-negative number.")

def main():
    finished = False
    while not finished:
        showMenu()
        try:
            choice=int(input("Your choice: "))
            if choice==0:
                finished=True
            elif choice==1:
                sudoku()
            elif choice==2:
                cryptoarithmeticGame()
            elif choice==3:
                geometricForms()
            else:
                print("Please choose a valid option.")
        except ValueError:
            print("The choice must be a number: 0, 1, 2 or 3")
            
main()
        
    