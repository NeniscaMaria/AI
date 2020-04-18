# -*- coding: utf-8 -*-

class Data:
    def __init__(self, a1,a2,a3,a4,a5,r):
        self.__attr1 = a1
        self.__attr2 = a2
        self.__attr3 = a3
        self.__attr4 = a4
        self.__attr5 = a5
        self.__result = r
        
    def getA1(self):
        return self.__attr1
    
    def getA2(self):
        return self.__attr2
    
    def getA3(self):
        return self.__attr3
    
    def getA4(self):
        return self.__attr4
    
    def getA5(self):
        return self.__attr5
    
    def getResult(self):
        return self.__result