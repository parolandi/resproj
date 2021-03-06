
from __future__ import print_function

import copy
import logging
import numpy
import time

import metrics.ordinary_differential as mod
import solvers.least_squares as sls
import solvers.monte_carlo_sampling as smcs
import solvers.solver_data as ss


montecarlo_multiple_optimisation_params = {
    "class": None,
    "decision_variable_ranges": [],
    "number_of_trials": 0,
    "random_number_generator_seed": 117,
    "subsolver_params": dict(ss.algorithm_structure)
    }


inf_obj_func = 1E10


solution_point = {
    "decision_variables": [],
    "objective_function": inf_obj_func,
    }


# TODO: success
# TODO: 2015-07-11; numpy.array
montecarlo_multiple_optimisation_result = {
    "all": [],
    "local": [],
    "global": dict(solution_point)
    }


def print_montecarlo_multiple_least_squares(wall_time, result, nom_params, nom_ssr, fit_ssr):
    print("**********************************************")
    print("* Monte Carlo multiple least-squares summary *")
    print("wall time:                  ", wall_time)
    print("number of local optima:     ", len(result["local"]))
    print("ssr (local)                 ", [result["local"][ii]["objective_function"] for ii in range(len(result["local"]))])
    print("nominal parameter values:   ", nom_params)
    print("optimal parameter estimates:", result["global"]["decision_variables"])
    print("ssr (raw):                  ", nom_ssr)
    print("ssr (opt):                  ", fit_ssr)
    print("ssr (fit):                  ", result["global"]["objective_function"])        
    print("**********************************************")
    

# TODO: testme
def solve(model, problem, algorithm):
    wall_time0 = time.time()
    result = montecarlo_multiple_least_squares(model, problem, algorithm)
    wall_time = time.time() - wall_time0
    print_montecarlo_multiple_least_squares(wall_time, result, [], 0.0, result["global"]["objective_function"])
    return result["global"]


def solve_all(model, problem, algorithm):
    wall_time0 = time.time()
    result = montecarlo_multiple_least_squares(model, problem, algorithm)
    wall_time = time.time() - wall_time0
    print_montecarlo_multiple_least_squares(wall_time, result, [], 0.0, result["global"]["objective_function"])
    return result


'''
This does a montecarlo randomisation of initial guesses
and solves the least-squares problem
'''
# TODO: total number of runs
# TODO: change to "flat" structure as in initial_value
def montecarlo_multiple_least_squares(model, problem, algorithm):
    assert(model["model"] is not None)
    assert(problem["performance_measure"] is not None)
    assert(problem["performance_measure"] is mod.sum_squared_residuals)
    dv_count = len(problem["parameter_indices"])
    assert(len(algorithm["decision_variable_ranges"]) == dv_count)
    # TODO: preconditions!
    
    monte_carlo_points = smcs.do_sampling(algorithm)
    logging.debug("mc-points: " + str(monte_carlo_points))
    
    result = dict(montecarlo_multiple_optimisation_result)
    subsolver_algorithm = dict(algorithm["subsolver_params"])
    for ii in range(algorithm["number_of_trials"]):
        logging.info("mc-trial (heart beat): " + str(ii))
        initial_guesses = []
        for jj in range(dv_count):
            initial_guesses.append(monte_carlo_points[jj][ii])
        subsolver_algorithm["initial_guesses"] = initial_guesses
        trial_result = sls.solve(model, problem, subsolver_algorithm)
        sp_copy = copy.deepcopy(solution_point)
        trial_point = dict(sp_copy)
        trial_point["decision_variables"] = numpy.asarray(trial_result.x)
        obj_fun = inf_obj_func
        if trial_result.success:
            obj_fun = problem["performance_measure"](trial_result.x, model, problem) 
        trial_point["objective_function"] = copy.deepcopy(obj_fun)
        result["all"].append(trial_point)
        if trial_result.success:
            result["local"].append(trial_point)
        if trial_result.success and obj_fun < result["global"]["objective_function"]:
            result["global"] = trial_point

    return result
