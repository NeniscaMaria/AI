class FuzzyDescriptions:
    #description of a fuzzy variable
    #contains a set of functions for each fuzzy region
    def __init__(self):
        self.regions = {}
        self.inverse = {}

    def addRegion(self, variableName, membershipFunction, inverseFunction=None):
        #Adds a region with a given membership function, an inverse function for the Sugeno method
        self.regions[variableName] = membershipFunction
        self.inverse[variableName] = inverseFunction

    def fuzzify(self, value):
        #Return the fuzzified values for each region
        return {name: membership_function(value)
                for name, membership_function in self.regions.items()
                }

    def defuzzify(self, variableName, value):
        return self.inverse[variableName](value)