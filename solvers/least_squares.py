
import scipy.optimize

# TODO: validate use of data structure
import solvers.solver_data


# TODO: rename; remove _st
def solve_st(metric, model, model_instance, problem_instance, algorithm_structure):
    diag = {
        "disp": False,
        }
    return scipy.optimize.minimize( \
        args =     (model, model_instance, problem_instance), \
        bounds =   problem_instance["bounds"], \
        callback = algorithm_structure["callback"], \
        fun =      metric, \
        method =   algorithm_structure["method"], \
        options =  diag, \
        tol =      algorithm_structure["tolerance"], \
        x0 =       algorithm_structure["initial_guesses"], \
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
