from GPalgorithm import GPalgorithm

class UI:
    def __init__(self,dataFile):
        self.__dataFile = dataFile
    
    def run(self):
        accuracy = float(input("Accuracy: "))
        algorithm = GPalgorithm(self.__dataFile,10,accuracy)
        algorithm.run()
    
if __name__=='__main__':
    ui = UI("sensor_readings_24.data")
    ui.run()
    