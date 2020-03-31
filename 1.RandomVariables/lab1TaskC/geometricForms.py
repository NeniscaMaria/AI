# -*- coding: utf-8 -*-
import numpy as np 
import random

class GeometricForms:
    def __init__(self,trials):
        self.noOfTrials=trials
        self.length=5
        self.height=6
        self.form1=[1,1,1,1]
        
        self.form2=[[1,0,0],
                    [1,1,1]]
        
        self.form3=[[1,0,1],
                    [1,1,1]]
        
        self.form4=[[1,1,1],
                    [0,0,1]]
        
        self.form5=[[0,1,0],
                    [1,1,1]]
        
        self.forms=[self.form1,self.form2,self.form3,self.form4,self.form5]
        
        self.board=np.zeros((self.height,self.length),dtype=int)
                
    def rotateOnce(self,form):
        #function that rotates with 90degrees clockwise a form
        if form == self.form1:
            rotatedForm=zip(form[::-1])
        else:
            rotatedForm = zip(*form[::-1]) #returns list of tuples 
        return [list(elem) for elem in rotatedForm]
        
    def rotateform(self,formNumber,times):
        #function that rotates a form 'times' times
        form=self.forms[formNumber]
        for i in range (times):
            form=self.rotateOnce(form)
        return form
    
    def displayBoard(self):
        for row in self.board.tolist():
            print(row)
     
    def fitForm(self,form,i,j):
        #https://stackoverflow.com/questions/53124061/how-can-i-add-a-small-matrix-into-a-big-one-with-numpy/53124171
        '''
        DESCR: function that tries to put the form on the board st the uperleft corner is on box i,j
        PRE:form=matrix of ints 1 and 0
        POST: true if we managed to put in on that position, false otherwise
        '''
        try:
            #we place the form on the board
            form=np.asarray(form)
            self.board[i:i+form.shape[0],j:j+form.shape[1]]+=form
            
            #verify if we have any overlaps <=> if there are any 2's on the board
            for row in self.board:
                for el in row:
                    if el!=1 and el!=0:
                        #we found an overlap so we remove the piece from the board
                        self.board[i:i+form.shape[0],j:j+form.shape[1]]-=form
                        return False
            return True
        except ValueError:
            #this means that the piece is out of the board
            return False
       
        
    def placeFormOnBoard(self,form):
        '''
        DESCR: function that tries to place a form on the board
        PRE: form : TYPE list on list of ints
        POST: true if we managed to fit the form on the board

        '''
        for i in range (0,self.height):
            for j in range (0,self.length):
                if self.fitForm(form, i, j): #we managed to fit the form
                    return True
        return False
    
    def checkFitting(self,solution):
        '''
        DESCR: function that verifies if the pieces fit in that order on the board
        PRE:solution=list of matrices
        POST:true if they fit, false otherwise
        '''
        #checking fitting from upperleft corner of the board
        for form in solution:
            if not self.placeFormOnBoard(form):
                return False
        #TODO: check if they fit from the other corners
        return True
    
    def verifySolution(self,solution):
        if self.checkFitting(solution):
            return True
        else: #pieces don't fit
            return False
    
    def solve(self):
        solved = False
        while self.noOfTrials and not solved:
            #generating how may times to rotate each form and rotating them
            rotatedForms=[]
            for i in range (len(self.forms)):
                timesToRotate = (np.random.randint(1,5,1)[0])
                rotatedForm=self.rotateform(i, timesToRotate)
                rotatedForms.append(rotatedForm)
                
                #we will shuffle the list of rotated forms so that we get an order for them to be arranged
                random.shuffle(rotatedForms)
            if self.verifySolution(rotatedForms):
                print("YAAY! Solution found.")
                print("Solution generated:")
                for form in rotatedForms:
                    print(form)
                self.displayBoard()
                solved=True
            else:
                self.noOfTrials-=1
        if not solved:
            print("No solution found:(")
                    
    def start(self):
        self.solve()
        