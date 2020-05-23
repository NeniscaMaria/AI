from controller import Controller
from description import FuzzyDescriptions
from rule import FuzzyRule

class UI:
    def __init__(self):
        self.__inputFile = 'input.in'
        self.__ruleFile = 'problem.in'
        #representing the fuzzy facts(fuzzy sets)
        self.__temperature = self.__initializeTemperature()
        self.__humidity = self.__initializeHumidity()
        self.__time = self.__initializeTime()
        #initialize the rules defined in the self.__ruleFile file
        self.__rules = self.__initializeRules() 
    
    def trapezoidalRegion(self,a, b, c, d):
        return lambda x: max(0, min((x - a) / (b - a), 1, (d - x) / (d - c)))
    
    def triangularRegion(self,a, b, c):
        return self.trapezoidalRegion(a, b, b, c)
    
    def __initializeTemperature(self):
        temperature = FuzzyDescriptions()
        temperature.addRegion('very cold', self.trapezoidalRegion(-1000, -30, -20, 5))
        temperature.addRegion('cold', self.triangularRegion(-5, 0, 10))
        temperature.addRegion('normal', self.trapezoidalRegion(5, 10, 15, 20))
        temperature.addRegion('warm', self.triangularRegion(15, 20, 25))
        temperature.addRegion('hot', self.trapezoidalRegion(25, 30, 35, 1000))
        return temperature
        
    def __initializeHumidity(self):
        humidity = FuzzyDescriptions()
        humidity.addRegion('dry', self.triangularRegion(-1000, 0, 50))
        humidity.addRegion('normal', self.triangularRegion(0, 50, 100))
        humidity.addRegion('wet', self.triangularRegion(50, 100, 1000))
        return humidity
        
    def inverseLine(self,a, b):
        return lambda x: x*(b - a) + a
    
    def inverse_tri(self,a, b, c):
        return lambda x: (self.inverseLine(a, b)*x + self.inverseLine(c, b)*x)/2
    
    def __initializeTime(self):
        time = FuzzyDescriptions()
        time.addRegion('short', self.triangularRegion(-1000, 0, 50), self.inverseLine(50, 0))
        time.addRegion('medium', self.triangularRegion(0, 50, 100), self.inverse_tri(0, 50, 100))
        time.addRegion('long', self.triangularRegion(50, 100, 1000), self.inverseLine(50, 100))
        return time 
    
    def __initializeRules(self):
        rules=[]
        try:
            with open(self.__ruleFile,'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line != "":
                        words = line.strip().split(",")
                        if(words[-1]==''):
                            words.remove('')
                        rules.append(FuzzyRule({'temperature': words[1], 'humidity': words[0]},
                           {'time':words[2]}))
        except FileNotFoundError :
            print("Inexistent file : "+self.__ruleFile)
        return rules
        
    def __readInput(self):
        inputData={}
        try:
            with open(self.__inputFile,'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line != "":
                        words = line.strip().split(",")
                        if(words[-1]==''):
                            words.remove('')
                        inputData[int(words[0])] = int(words[1])
        except FileNotFoundError :
            print("Inexistent file : "+self.__inputFile)
        return inputData
    
    def run(self):
        ctrl = Controller(self.__temperature, self.__humidity, self.__time, self.__rules)
        #read input data from file
        inputData = self.__readInput()
        for key in inputData.keys():
            print(ctrl.compute({'humidity':key, 'temperature':inputData[key]}))
        
if __name__ == '__main__':
    ui = UI()
    ui.run()