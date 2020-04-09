# -*- coding: utf-8 -*-

class Tree:
    def __init__(self):
        self.__root = None
    
    def setRoot(self,root):
        self.__root = root
    def getRoot(self):
        return self.__root