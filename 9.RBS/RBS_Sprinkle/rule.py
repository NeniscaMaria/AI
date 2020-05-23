class FuzzyRule:
    #this rule is a conjunctive one because
    #because we have to predict Z from: 
    #if humidity = x AND temperature = Y => time = Z
    
    def __init__(self, inputs, out):
        #Receives the set of inputs and expected output
        self.outputVariable = out  
        self.inputs = inputs

    def evaluate(self, inputs):
        #Receives a dictionary of all the input values and returns the conjunction of their values
        #conjunction => minimum
        #=> return the minimum value from inputs
        return [self.outputVariable, min([inputs[descr][var] for descr, var in self.inputs.items()])]
