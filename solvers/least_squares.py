
import scipy.optimize

import copy
import logging

# TODO: validate use of data structure
import common.diagnostics as cdi


# TODO: exceptions
# raise ValueError unknown solver
def solve(model_instance, problem_instance, algorithm_structure):
    """
    return: OptimizeResult
    """
    assert(len(problem_instance["parameter_indices"]) == len(algorithm_structure["initial_guesses"]))
    assert(model_instance["model"] is not None)
    assert(problem_instance["performance_measure"] is not None)
    #TODO: preconditions
    if problem_instance["bounds"] is not None:
        assert(len(problem_instance["parameter_indices"]) == len(problem_instance["bounds"]))
    
    # WIP: 2015-07-11; hard-coded cannot be
    algorithm_structure["solver_settings"] = {}
    # WIP: 2015-0718; regressions
    algorithm_structure["solver_settings"]["eps"] = 1e-6
    #algorithm_structure["solver_settings"]["maxiter"] = 100
    
    result = scipy.optimize.minimize( \
        args =     (model_instance, problem_instance), \
        bounds =   problem_instance["bounds"], \
        callback = algorithm_structure["callback"], \
        fun =      problem_instance["performance_measure"], \
        method =   algorithm_structure["method"], \
        options =  algorithm_structure["solver_settings"], \
        tol =      algorithm_structure["tolerance"], \
        x0 =       algorithm_structure["initial_guesses"] \
        )
    logging.info("solvers.least_squares.solve")
    logging.info(algorithm_structure)
    logging.info(result)
    return result


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
