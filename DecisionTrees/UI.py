# -*- coding: utf-8 -*-
from Class import Class
from Tree import Tree
from Node import Node
import random, math
import copy
class UI:
    def __init__(self):
        self.__attributes = ['lw','ld','rw','rd']
        self.__data = self.__readData()
        self.__trainingData, self.__testingData = self.__split()
        self.__tree = Tree()
        
    def __readData(self):
        data = []
        try:
            with open("balance-scale.data",'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line != "":
                        words = line.strip().split(",")
                        r=words[0].strip()
                        lw=int(words[1].strip())
                        ld=int(words[2].strip())
                        rw=int(words[3].strip())
                        rd=int(words[4].strip())
                        c = Class(r,lw,ld,rw,rd)
                        data.append(c)                        
        except FileNotFoundError :
            print("Inexistent file : "+self.__filename)
        return data
    
    def __split(self):
        random.shuffle(self.__data)
        train_data = self.__data[:int((len(self.__data)+1)*.80)] #Remaining 70% to training set
        test_data = self.__data[int(len(self.__data)*.20+1):] #Splits 30% data to test set
        return train_data, test_data
    
    def __checkSameClass(self,data):
        r = data[0].getResult()
        for d in data:
            if d.getResult()!=r:
                return False
        return True
    
    def __getMajority(self,data):
        r = [d.getResult() for d in data]
        countL = r.count("L")
        countB = r.count("B")
        countR = r.count("R")
        
        if countL>=countB and countL>=countR:
            return "L"
        if countB>=countL and countB>=countR:
            return "B"
        return "R"        
    
    def __getGain(self,data,attributes):
        #overall entropy
        total = len(data)
        r = [d.getResult() for d in data]
        sL = r.count("L")/total
        sR = r.count("R")/total
        sB = r.count("B")/total
        entropyS = 0
        if sL!=0 :
            entropyS -= sL*math.log(sL,2)
        if sR!=0:
            entropyS -= sR*math.log(sR,2)
        if sB!=0:
            entropyS -= sB*math.log(sB,2)
                
        gains=[]
        
        for attribute in attributes:
            gain = entropyS
            sumEntropies = 0
            dataForEachvalue = []
            #for each attribute a in the set, we compute a new list of lists
            #that has on position i the list of all data that has attribute a = i+1
            if attribute == 'lw':
                #left weight
                for i in [1,2,3,4,5]:
                    #list of data that has left weight = i
                    dataForEachvalue.append( [d for d in data if d.getLW()==i])
            if attribute == 'ld':
                #leftDistance
                sumEntropies=0
                for i in [1,2,3,4,5]:
                    dataForEachvalue.append( [d for d in data if d.getLD()==i])
            
            if attribute == 'rw':
                #right weight
                sumEntropies=0
                for i in [1,2,3,4,5]:
                    dataForEachvalue.append( [d for d in data if d.getRW()==i])
            
            if attribute == 'rd':
                #right distance
                sumEntropies=0
                for i in [1,2,3,4,5]:
                    dataForEachvalue.append( [d for d in data if d.getRD()==i])
            
            #we compute the entropy of this attribute
            for rd in dataForEachvalue:
                pi = len(rd)/total
                if pi!=0:
                    pL = [d for d in rd if d.getResult()=="L"]
                    probL = len(pL)/len(rd)
                    pR = [d for d in rd if d.getResult()=="R"]
                    probR = len(pR)/len(rd)
                    pB = [d for d in rd if d.getResult()=="B"]
                    probB = len(pB)/len(rd)
                    entropyI = 0
                    if probL!=0:
                        entropyI -= probL*math.log(probL,2)
                    if(probR!=0):
                        entropyI -= probR*math.log(probR,2)
                    if(probB!=0):
                        entropyI -= probB*math.log(probB,2)
                    sumEntropies += pi*entropyI
                else:
                    sumEntropies = 0
            gain -= sumEntropies
            gains.append(gain)
        return gains
        
    def __attributeSelection(self,data,attributes):
        if len(attributes)==1:
            return attributes[0]
        gains = self.__getGain(data, attributes)
        #get maximum gain
        maxGain = max(gains)
        position = gains.index(maxGain)
        return attributes[position]
        
    
    def generateTree(self,data,attributes):
        node = Node()
        if self.__checkSameClass(data):
            node.setLabel(data[0].getResult())
            return node
        else:
            if attributes == []:
                label = self.__getMajority(data)
                node.setLabel(label)
                return node
            else:
                sepparationAttribute  = self.__attributeSelection(data,attributes)
                node.setLabel(sepparationAttribute)
                for v in [1,2,3,4,5]:
                    listData = []
                    for d in data:
                        if sepparationAttribute=="lw" and d.getLW() == v:
                            listData.append(d)
                        if sepparationAttribute=="ld" and d.getLD()==v:
                            listData.append(d)
                        if sepparationAttribute=="rw" and d.getRW()==v:
                            listData.append(d)
                        if sepparationAttribute=="rd" and d.getRD()==v:
                            listData.append(d)
                    #pre pruning
                    if listData == [] or len(listData)==len(data) or len(listData)==2*len(data) or len(listData)<5:
                        newNode = Node()
                        label = self.__getMajority(data)
                        newNode.setLabel(label)
                        node.addChild(newNode)
                        return node
                    else:
                        copyA = copy.deepcopy(attributes)
                        copyA.remove(sepparationAttribute)
                        newNode = self.generateTree(listData,copyA)
                        node.addChild(newNode)
                return node
        
    def print_tree(self,current_node, childattr='children', nameattr='name', indent='', last='updown'):
    #source of this function: https://github.com/clemtoy/pptree/blob/master/pptree/pptree.py
        if hasattr(current_node, nameattr):
            name = lambda node: getattr(node, nameattr)
        else:
            name = lambda node: str(node)
    
        children = lambda node: getattr(node, childattr)
        nb_children = lambda node: sum(nb_children(child) for child in children(node)) + 1
        size_branch = {child: nb_children(child) for child in children(current_node)}
    
        """ Creation of balanced lists for "up" branch and "down" branch. """
        up = sorted(children(current_node), key=lambda node: nb_children(node))
        down = []
        while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
            down.append(up.pop())
    
        """ Printing of "up" branch. """
        for child in up:     
            next_last = 'up' if up.index(child) is 0 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', ' ' * len(name(current_node)))
            self.print_tree(child, childattr, nameattr, next_indent, next_last)
    
        """ Printing of current node. """
        if last == 'up': start_shape = '┌'
        elif last == 'down': start_shape = '└'
        elif last == 'updown': start_shape = ' '
        else: start_shape = '├'
    
        if up: end_shape = '┤'
        elif down: end_shape = '┐'
        else: end_shape = ''
    
        print('{0}{1}{2}{3}'.format(indent, start_shape, name(current_node), end_shape))
    
        """ Printing of "down" branch. """
        for child in down:
            next_last = 'down' if down.index(child) is len(down) - 1 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', ' ' * len(name(current_node)))
            self.print_tree(child, childattr, nameattr, next_indent, next_last)
          
    def test(self):
        correct = 0
        node = self.__tree.getRoot()
        for data in self.__testingData:
            correctResult = data.getResult()
            while node.getLabel() in self.__attributes:
                attribute = node.getLabel()
                if attribute == 'lw':
                    value = data.getLW()                    
                if attribute == 'ld':
                    value = data.getLD()
                if attribute == 'rw':
                    value = data.getRW()
                if attribute == 'rd':
                    value = data.getRD()
                if value not in range(len(node.getChildren())):
                    node = node.getChildren()[-1]
                else:
                    node = node.getChildren()[value-1]
            result = node.getLabel()
            if result == correctResult:
                correct+=1 
                
        return correct/len(self.__testingData)*100
    
    def __prune(self,node):
        if node.getChildren()==[]:
            return
        children = node.getChildren()
        count = 0
        
        l = children[0].getLabel()
        if l in  ['L','R','B']:
            for child in children:
                if child.getLabel() == l:
                    count+=1
        if count == len(children) or count == len(children)-1:
            node.children=[]
            node.setLabel(l)
        else:
            for child in children:
                self.__prune(child)
        
        
        
    def run(self):
        #1construct tree
        root = self.generateTree(self.__trainingData,self.__attributes)
        self.__tree.setRoot(root)
        print("The tree is:")
        self.print_tree(root)
        
        
        #2use tree as problem solver
        p1 = self.test()
       
        
        #3pruning
        self.__prune(root)
        self.print_tree(root)
        p2 = self.test()
        print("Accuracy: ",p1,"%")
        print("Accuracy: ",p2,"%")