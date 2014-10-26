
import scipy.optimize

# TODO: validate use of data structure
import common.diagnostics as cdi
import solvers.solver_data


# TODO: rename; remove _st
def solve_st(metric, model, model_instance, problem_instance, algorithm_structure):
    assert(len(problem_instance["parameter_indices"]) == len(algorithm_structure["initial_guesses"]))
    #TODO: preconditions

    if model is None:
        assert(model_instance["model"] is not None)
        model = model_instance["model"]
        cdi.print_legacy_code_message()
    
    if metric is None:
        assert(problem_instance["performance_measure"] is not None)
        metric = problem_instance["performance_measure"]
        cdi.print_legacy_code_message()
        
    return scipy.optimize.minimize( \
        args =     (model, model_instance, problem_instance), \
        bounds =   problem_instance["bounds"], \
        callback = algorithm_structure["callback"], \
        fun =      metric, \
        method =   algorithm_structure["method"], \
        options =  algorithm_structure["solver_settings"], \
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
