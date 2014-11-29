
import scipy.optimize
import copy

# TODO: validate use of data structure
import common.diagnostics as cdi
import solvers.solver_data


# TODO: exceptions
# raise ValueError unknown solver
def solve(model_instance, problem_instance, algorithm_structure):
    assert(len(problem_instance["parameter_indices"]) == len(algorithm_structure["initial_guesses"]))
    assert(model_instance["model"] is not None)
    assert(problem_instance["performance_measure"] is not None)
    #TODO: preconditions
    
    return scipy.optimize.minimize( \
        args =     (None, model_instance, problem_instance), \
        bounds =   problem_instance["bounds"], \
        callback = algorithm_structure["callback"], \
        fun =      problem_instance["performance_measure"], \
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


# -----------------------------------------------------------------------------
'''
Legacy
'''
# -----------------------------------------------------------------------------
# TODO: remove when possible
def solve_st(metric, model, model_instance, problem_instance, algorithm_structure):
    assert(len(problem_instance["parameter_indices"]) == len(algorithm_structure["initial_guesses"]))
    #TODO: preconditions

    cdi.print_legacy_code_message()

    if model is None:
        assert(model_instance["model"] is not None)
        model = copy.deepcopy(model_instance["model"])
    else:
        cdi.print_legacy_code_message()
    
    if metric is None:
        assert(problem_instance["performance_measure"] is not None)
        metric = copy.deepcopy(problem_instance["performance_measure"])
    else:
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
