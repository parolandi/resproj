
class DecisionVariableLogger():
    
    def __init__(self):
        self.decision_variables = []
    
    def log_decision_variables(self, x):
        self.decision_variables.append([x])


    def let_decision_variables_be_positive_and_log(self, x):
        eps = 1E-30
        logit = False
        corrected = []
        for ii in range(len(x)):
            if x[ii] < eps:
                x[ii] = eps
                corrected.append(ii)
        if len(corrected) > 0 and logit:
            print("corrected", x, corrected)

        self.decision_variables.append([x])
        
    def print_decision_variables(self):
        print("Decision variables", self.decision_variables)
        
    def get_decision_variables(self):
        return self.decision_variables
