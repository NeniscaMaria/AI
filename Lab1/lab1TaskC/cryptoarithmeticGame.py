# -*- coding: utf-8 -*-
import numpy as np

class CryptoarithmeticGame:
    def __init__(self,trials):
        self.noOfTrials = trials
        self.word1 = "send"
        self.word2 = "more"
        self.result = "money"
        self.cipher={'s':0,'e':0,'n':0,'d':0,
                     'm':0,'o':0,'r':0,
                     'y':0}
        self.encryption = []
     
    def checkSolution(self):
        #converting the encryption nu numbers
        hex_word1 = self.encryption[0]
        hex_int_word1 = int(hex_word1, 16)
        
        hex_word2 = self.encryption[1]
        hex_int_word2 = int(hex_word2, 16)
        
        #adding the encrypted numbers
        new_int = hex_int_word1 + hex_int_word2
        
        hex_solution = self.encryption[2]
        hex_int_solution = int(hex_solution, 16)
    
        
        return new_int==hex_int_solution
            
    def solve(self):
        solved = False
        while self.noOfTrials and not solved:
            #generating random numbers for each letter
            for letter in self.cipher.keys():
                self.cipher[letter] = np.random.randint(0,16,1)[0]
            #encrypting words
            word1Encrypted=''
            for letter in self.word1:
                word1Encrypted+=np.base_repr(self.cipher[letter],base=16)
            word2Encrypted=''
            for letter in self.word2:
                word2Encrypted+=np.base_repr(self.cipher[letter],base=16)
            solutionEncrypted=''
            for letter in self.result:
                solutionEncrypted+=np.base_repr(self.cipher[letter],base=16)
            self.encryption.append(word1Encrypted)
            self.encryption.append(word2Encrypted)
            self.encryption.append(solutionEncrypted)
            if self.checkSolution():
                print("Solution found!")
                solved=True
                for letter in self.cipher.keys():
                    print(letter+" : "+np.base_repr(self.cipher[letter],base=16))
                    self.noOfTrials=0
            else:
                self.noOfTrials-=1
                self.encryption=[]
        if not solved:
            print("Solution not found :(")
    def start(self):
        self.solve()