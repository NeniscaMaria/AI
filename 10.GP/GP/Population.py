from Chromosome import Chromosome

class Population:
    def __init__(self, nrIndividuals):
        self.nrIndividuals = nrIndividuals
        #generate the individuals in the population
        self.individuals = [Chromosome() for _ in range(nrIndividuals)]

    def evaluate(self, inputTrain, outputTrain):
        print("Evaluating population...")
        for chromosome in self.individuals:
            chromosome.evaluate(inputTrain, outputTrain)

    def selection(self, nrIndividuals):
        #select top nrIndividuals from the population
        if nrIndividuals < self.nrIndividuals:
            self.nrIndividuals = nrIndividuals
            #sort the individuals based on their fitness
            self.individuals = sorted(self.individuals, key=lambda x: x.fitness)
            self.individuals = self.individuals[:nrIndividuals]

    def best(self, maxIndividuals):
        #select the best max Individuals individuals from the population
        self.individuals = sorted(self.individuals, key=lambda x: x.fitness)
        return self.individuals[:maxIndividuals]

    def reunion(self, other):
        #unite to populations
        self.nrIndividuals += other.nrIndividuals
        self.individuals = self.individuals + other.individuals