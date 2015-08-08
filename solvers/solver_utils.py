
import logging


class DecisionVariableLogger():
    
    def __init__(self):
        self.decision_variables = []

    
    def log_decision_variables(self, x):
        self.decision_variables.append([x])


    def let_decision_variables_be_positive_and_log(self, x):
        logit = False
        
        eps = 1e-30
        corrected = []
        for ii in range(len(x)):
            if x[ii] < eps:
                x[ii] = eps
                corrected.append(ii)
        if len(corrected) > 0 and logit:
            print("corrected", x, corrected)

        self.decision_variables.append([x])
        if logit:
            logging.info(x)
        
        
    def let_decision_variables_be_bounded_and_log(self, x):
        logit = False
        
        eps_lb = 1E-10
        eps_ub = 1E+10
        corrected = []
        for ii in range(len(x)):
            if x[ii] < eps_lb:
                x[ii] = eps_lb
                corrected.append(ii)
        for ii in range(len(x)):
            if x[ii] > eps_ub:
                x[ii] = eps_ub
                corrected.append(ii)
        if len(corrected) > 0 and logit:
            print("corrected", x, corrected)

        self.decision_variables.append([x])
        if logit:
            logging.info(x)

    
    def print_decision_variables(self):
        print("Decision variables", self.decision_variables)

        
    def get_decision_variables(self):
        return self.decision_variables
