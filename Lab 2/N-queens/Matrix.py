# -*- coding: utf-8 -*-
import copy

class Matrix:
    def __init__(self,size,board):
        self.__size=size
        self.__board = board
        
    def getSize(self):
        return self.__size
    
    def getBoard(self):
        return self.__board[:]
    
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self.__size != other.getSize():
            return False
        for i in range(self.__size):
            if self.__board[i] != other.getBoard()[i]:
                return False
        return True
        
    def __str__(self):
        return str(self.__board)
    
    def getElement(self,i,j):
        return self.__board[i][j]
    
    def checkOnes(self):
        #checks is the board has all the required number of queens positioned
        count=0
        for i in range (0,self.__size):
            for j in range(0,self.__size):
                if self.__board[i][j]==1:
                    count+=1
        return count == self.__size
    
    def rowFree(self,i):
        #check if row i is free, i.e. has no queen on it
        row=self.__board[i]
        for el in row:
            if el==1:
                return False
        return True
    
    def columnFree(self,j):
        #check if column j is free, i.e. has no queen on it
        for row in self.__board:
            if row[j]==1:
                return False
        return True
    
    #TODO: checkDiagonal is nopt working    
    def auxDiagonal(self,i,j,board):
        #checks if the queen on position (i,j) is attacked by other queens
        for row in range (0,self.__size):
            for column in range (0,self.__size):
                if row!=i and column!=j:
                    if board[row][column]==1:
                        difRow=abs(i-row)
                        difCol=abs(j-column)
                        if difRow-difCol==0:
                            return False
        return True
          
    def checkDiagonal(self,board):
        #checks if no queens atack each other on thwe diagonal
        for i in range(0,self.__size):
            for j in range(0,self.__size):
                if board[i][j]==1:
                    if not self.auxDiagonal(i, j, board):
                        return False
        return True
        
    def nextConfig(self,i):
        '''
        Putting a new queen on the board  on row i
        '''
        nextC = [] #list of new states
        copyBoard = copy.deepcopy(self.__board)
        if self.rowFree(i):
            #try to put the queen on each position in the row
            for j in range(0,self.__size):
                if self.columnFree(j):
                    #put the queen on the position
                    copyBoard[i][j]=1
                    #check diagonal
                    if self.checkDiagonal(copyBoard):
                        nextC.append(Matrix(self.__size,copyBoard))
                copyBoard=copy.deepcopy(self.__board)
        return nextC