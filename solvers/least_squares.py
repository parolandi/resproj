
import scipy.optimize

# TODO: validate use of data structure
import solvers.solver_data


def solve_st(metric, model, model_instance, problem_instance, algorithm_structure):
    diag = {
        "disp": False,
        }
    return scipy.optimize.minimize( \
        fun =     metric, \
        x0 =      algorithm_structure["initial_guesses"], \
        args =    (model, model_instance, problem_instance), \
        method =  algorithm_structure["method"],
        bounds =  problem_instance["bounds"],
        callback = algorithm_structure["callback"],
        options = diag,
        tol = algorithm_structure["tolerance"],
        )


class DecisionVariableLogger():
    
    def __init__(self):
        self.decision_variables = []
    
    def log_decision_variables(self, x):
        self.decision_variables.append([x])
        
    def print_decision_variables(self):
        print("Decision variables", self.decision_variables)
        
    def get_decision_variables(self):
        return self.decision_variables
