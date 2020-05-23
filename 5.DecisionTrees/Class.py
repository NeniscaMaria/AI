# -*- coding: utf-8 -*-

class Class():
    def __init__(self,c,lw,ld,rw,rd):
        self.__result = c
        self.__leftWeight = lw
        self.__leftDistance = ld
        self.__rightWeight = rw
        self.__rightDistance = rd
        
    def getLW(self):
        return self.__leftWeight
    def getLD(self):
        return self.__leftDistance
    def getRW(self):
        return self.__rightWeight
    def getRD(self):
        return self.__rightDistance
    def getResult(self):
        return self.__result
    def __str__(self):
        return (self.__result+" "+str(self.__leftWeight)+" "+str(self.__leftDistance)+
        " "+str(self.__rightWeight)+" "+str(self.__rightDistance))