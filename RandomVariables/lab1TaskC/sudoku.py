# -*- coding: utf-8 -*-
import numpy as np

class Sudoku:
    def __init__(self, sizeFromUser, trials):
        self.noOfTrials=trials
        self.boardSize = sizeFromUser
        self.board=[]
    
    def validateRow(self,row):
        '''
        DESCR: checks if a row is valid and returns a list with the numbers friom the row
        PRE:row=list of strings
        POST:newRow=list of integers
        THROWS: ValueError if the numbers fromt he list are invalid
        '''
        newRow=[]
        if len(row) == self.boardSize:
            for number in row:
                    n = int(number)
                    if n > self.boardSize or n<0:
                        raise ValueError("Numbers must be non-negative and lower than the board size: "+str(self.boardSize))
                    else:
                      newRow.append(n)
        return newRow
                          
    def readBoard(self):
        #reads the board from keyboard
        i=0
        while i < self.boardSize:
            row = input("Enter row "+str(i)+" : ").split(" ")
            try:
                row = self.validateRow(row)
                if row != []:
                    i=i+1
                    self.board.append(row)
                else:
                    print("Insert a valid row. Be careful not to add a space after the last digit.")
            except ValueError as ve:
                print(ve)
    
    def checkNumbers(self,row):
        '''DESCR: check if the row/column can be part of the solution
        PRE: row = list of ints with values >0 and <=boardSize
        POST:true if valid, false otherwise
        '''
        for i in range(1,self.boardSize+1):
            if row.count(i)!=1:
                return False
        return True
    
    def validBlock(self,block):
        '''DESCR: check if the block can be part of the solution
        PRE: block = list of list ints with values >0 and <=boardSize
        POST:true if valid, false otherwise
        '''
        flattenedBlock = sum(block,[])
        for i in range(1,self.boardSize+1):
            if flattenedBlock.count(i)!=1:
                return False
        return True
        
    def generateCandidateSolution(self):
        '''
        DESCR: function that generates a random solution for the user's board
        POST:candidate = matrix of ints boardsize X boardSize
        '''
        print("Generating candidate solution...")
        candidate=[]
        for row in self.board:
            candidateRow=[]
            for number in row:
                if number == 0:
                    n =np.random.randint(1,high = self.boardSize+1, size=1)
                    candidateRow.append(n[0])
                else:
                    candidateRow.append(number)
            candidate.append(candidateRow)
        return candidate
                 
    def checkCandidateSolution(self, candidate):
        '''
        DESCR: function that checks whether the candidate solution is good
        PRE: candidate = matrix of ints size boardSize X boardSize
        POST: True if solution is good, False otherwise
        '''
        #checking the rows
        for row in candidate:
            if not self.checkNumbers(row):
                return False
        #checking the columns
        for i in range (0,self.boardSize):
            column=[]
            for j in range (0,self.boardSize):
                column.append[self.board[i][j]]
            print(column)
            if not self.checkNumbers(column):
                return False
        #getting the blocks
        max=int(np.sqrt(self.boardSize))
        blocks=[]
        horizontalSplits = np.hsplit(np.asarray(candidate),max)
        for split in horizontalSplits:
            verticalSplit = np.vsplit(split,max)
            for vsplit in verticalSplit:
                blocks.append(vsplit.tolist())
        #checking the blocks
        for block in blocks:
            if not self.validBlock(block):
                return False              
        return True
    
    def solve(self):
        solved=False
        print("Solving puzzle...")
        while self.noOfTrials and not solved:
            candidate = self.generateCandidateSolution()
            if self.checkCandidateSolution(candidate):
                print("YAY! Solution found!")
                solved=True
                for row in candidate:
                    print(row)
            else:
                self.noOfTrials-=1
        if not solved:
            print("Solution not found:(")
                
    def start(self):
        print("Please insert the board")
        self.readBoard()
        self.solve()
                
        