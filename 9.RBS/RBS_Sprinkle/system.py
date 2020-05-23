class FuzzySystem:
    def __init__(self, rules):
        self.inputDescriptions = {}
        self.outputDescription = None
        self.rules = rules

    def addDescription(self, name, descr, out=False):
        #out = True if the variable is an output variable, False otherwise
        if out:
            if self.outputDescription is None:
                self.outputDescription = descr
            else:
                raise ValueError('An output variable already exists!')
        else:
            self.inputDescriptions[name] = descr

    def compute(self, inputs):
        ruleValues = self._computeFuzzyRule(self._computeDescriptions(inputs))

        fuzzyOutputVariables = [(list(descr[0].values())[0], descr[1]) for descr in
                          ruleValues]
        #defuzzification with COA
        weightedTotal = 0
        sumW = 0
        for var in fuzzyOutputVariables:
            sumW += var[1]
            weightedTotal += self.outputDescription.defuzzify(*var) * var[1]
        return weightedTotal / sumW

    def _computeDescriptions(self, inputs):
        return {var_name: self.inputDescriptions[var_name].fuzzify(inputs[var_name])
            for var_name, val in inputs.items()}

    def _computeFuzzyRule(self, fuzzyValues):
        #Returns the fuzzy output of all rules
        #in this step we eliminate the ones that evaluate to 0
        return [rule.evaluate(fuzzyValues) for rule in self.rules if rule.evaluate(fuzzyValues)[1] != 0]