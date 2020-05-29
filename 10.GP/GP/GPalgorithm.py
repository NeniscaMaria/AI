import random
from Population import Population
from Chromosome import Chromosome

#global header that will later be used in Node
HEADER = []

class GPalgorithm:
    def __init__(self,dataFile,nrIndividuals,accuracy):
        self.dataSize = 0
        #mapping the resulting classes to integers, so that we can apply the functions
        self.map={"Slight-Right-Turn":0, "Sharp-Right-Turn":1, "Move-Forward":2,"Slight-Left-Turn":3}
        self.__dataFile = dataFile
        self.__accuracy = accuracy
        self.__nrIndividuals = nrIndividuals
    
        self.input = []
        self.output = []
        self.inputTest = []
        self.outputTest = []
        self.inputTrain = []
        self.outputTrain = []
        
        self.population = Population(nrIndividuals)
        self.probability_mutate = 0.5
        self.probability_crossover = 0.5
        
    def loadData(self):
        #loading the data from the file
        global HEADER
        print("Loading training data ... this may take a while")
        with open(self.__dataFile, "r") as f:
            HEADER = f.readline().split(',')[:]
            for line in f.readlines():
                words = line.split(',')
                values = list(map(float, words[:-1]))
                self.input.append(values)
                self.output.append(self.map[words[-1].strip()])
                self.dataSize += 1
        random.shuffle(self.input)
        random.shuffle(self.output)

        #split data in 70% train and 30% test
        self.inputTrain = self.input[:int(self.dataSize * 0.7)]
        self.outputTrain = self.output[:int(self.dataSize * 0.7)]
        self.inputTest = self.input[int(self.dataSize * 0.7):]
        self.outputTest = self.output[int(self.dataSize * 0.7):]

        print("Training size: " + str(len(self.inputTrain)))
        print("Testing size: " + str(len(self.outputTest)))
        
    def iteration(self, i):
        parents = range(self.__nrIndividuals)
        #two parent => one child
        nrChildren = len(parents) // 2
        #generate the population of offsprings
        offspringPopulation = Population(nrChildren)
        
        #create the offsprings
        for i in range(nrChildren):
            #random indexes for the parents
            crossover = False
            while not crossover:
                i1=random.randint(0,self.__nrIndividuals-1)
                i2=random.randint(0,self.__nrIndividuals-1)
                #select parents
                if (i1!=i2):
                    crossover = True
                    #combine parents
                    parent1=self.population.individuals[i1]
                    parent2=self.population.individuals[i2]
                    offspringPopulation.individuals[i] = Chromosome.crossover(parent1, parent2, self.probability_crossover)
            
                    #mutate offspring
                    offspringPopulation.individuals[i].mutate(self.probability_mutate)
                    
        #evaluating the offspring population
        offspringPopulation.evaluate(self.inputTrain, self.outputTrain)
        #we add the population of children to the population of parents
        self.population.reunion(offspringPopulation)
        #select tot nrIndividuals from the new population, i.e. only the best individuals survive to the next generation
        self.population.selection(self.__nrIndividuals)
        
   # def test(self):
     #   best = self.population.best(1)[0].root()
    #    for input in self.inputTest:
            
        
    def run(self):
        self.loadData()
        self.population.evaluate(self.inputTrain, self.outputTrain)
        for i in range(100):
            print("Iteration: " + str(i))
            self.iteration(i)
            self.population.evaluate(self.inputTrain, self.outputTrain)
        best = self.population.best(1)[0]
        print("Best: " + str(best.root) + "\n*********************\n"+ "Fitness: " + str(best.fitness))
            