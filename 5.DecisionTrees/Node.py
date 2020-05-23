# -*- coding: utf-8 -*-

class Node:
    def __init__(self):
        self.children = []
        self.__label = None
        
    def setLabel(self,label):
        self.__label = label
        
    def addChild(self,child):
        self.children.append(child)
    
    def getLabel(self):
        return self.__label
    
    def getChildren(self):
        return self.children
    def __str__(self):
        return self.__label
