from system import FuzzySystem

class Controller:
    def __init__(self, temperature, humidity, time, rules):
        self.system = FuzzySystem(rules)
        self.system.addDescription('temperature', temperature)
        self.system.addDescription('humidity', humidity)
        self.system.addDescription('time', time, out=True)
        
        self.__outputFile = 'output.out'
        
    def __logResult(self,result,inputs):
        try:
            with open(self.__outputFile,'a') as f:
                f.write(str(inputs)+" " +str(result))
                f.write('\n')
        except FileNotFoundError :
            print("Inexistent file : "+self.__outputFile)

    def compute(self, inputs):
        result = self.system.compute(inputs)
        self.__logResult(inputs,result)
        return "For humidity: " + str(inputs['humidity']) + " and temperature: " + str(inputs['temperature']) + " the sprinkle will run for: " + str(result)+" minutes."