
from __future__ import print_function
import copy
import logging
import numpy
import time

import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import solvers.initial_value as siv
import solvers.monte_carlo_sampling as smcs
import solvers.solver_data as ss


montecarlo_multiple_simulation_params = {
    "class": None,
    "decision_variable_ranges": [()], # tuples
    "number_of_trials": 0,
    "random_number_generator_seed": 117,
    "subsolver_params": dict(ss.algorithm_structure),
    "enable_trajectories": False
    }


inf_obj_func = 1E10


"""
Single point
"""
solution_trajectory = {
    "decision_variables": [],
    "trajectories": [],
    "objective_function": inf_obj_func,
    }


"""
Multiple points
"""
# TODO: 2015-06-28; intended to be numpy.array
ensemble_trajectoryies = {
    "decision_variables": [],
    "trajectories": [],
    "objective_function": [],
    }


"""
Multiple points
"""
solution_ensembles = {
    "decision_variables": numpy.zeros([1,1,1]),
    "trajectories": numpy.zeros([1,1,1]),
    "objective_function": inf_obj_func,
    }


#TODO success, failure
montecarlo_multiple_simulation_result = {
    "failed": copy.deepcopy(solution_ensembles),
    "succeeded": copy.deepcopy(solution_ensembles),
    }


def print_montecarlo_multiple_initial_value(wall_time, result):
    dim_pass = len(result["succeeded"]["objective_function"])
    dim_fail = len(result["failed"]["objective_function"])
    obj_pass = result["succeeded"]["objective_function"]
    print("**********************************************")
    print("* Monte Carlo multiple initial-value summary *")
    print("wall time:                  ", wall_time)
    print("total                       ", dim_pass + dim_fail)
    print("failed                      ", dim_fail)
    print("succeeded                   ", dim_pass)
    print("ssr (succeeded)             ", [obj_pass[ii] for ii in range(dim_pass)])
    print("**********************************************")
    

# TODO: testme
def solve(model, problem, algorithm):
    wall_time0 = time.time()
    result = montecarlo_multiple_initial_value(model, problem, algorithm)
    wall_time = time.time() - wall_time0
    print_montecarlo_multiple_initial_value(wall_time, result)
    return result


# TODO: total number of runs
# TODO: 2015-07-09; parameterise constants
def montecarlo_multiple_initial_value(model, problem, algorithm):
    """
    This does a montecarlo randomisation of initial guesses
    and solves the initial value problem
    return montecarlo_multiple_simulation_result
    """
    assert(model["model"] is not None)
    assert(problem["performance_measure"] is not None)
    assert(problem["performance_measure"] is mod.sum_squared_residuals)
    dv_count = len(problem["parameter_indices"])
    assert(len(algorithm["decision_variable_ranges"]) == dv_count)
    # TODO: preconditions!
    
    monte_carlo_points = smcs.do_sampling(algorithm)
    # TODO
    _ = dict(algorithm["subsolver_params"])
    
    success = copy.deepcopy(ensemble_trajectoryies)
    failure = copy.deepcopy(ensemble_trajectoryies)
    wall_time0 = time.time()
    for ii in range(algorithm["number_of_trials"]):
        if ii % 1000 == 0:
            wall_time = time.time() - wall_time0
            logging.info("mcmiv heartbeat (iter - wall time): " + str(ii) + " -s " + str(wall_time))
        param_vals = []
        for jj in range(dv_count):
            param_vals.append(monte_carlo_points[jj][ii])
        mmdu.apply_values_to_parameters(param_vals, model, problem)
        trial_result = siv.evaluate_timecourse_trajectories(model, problem)
        if trial_result.success:
            success["decision_variables"].append(param_vals)
            if algorithm["enable_trajectories"]:
                success["trajectories"].append(trial_result.trajectories)
            obj = problem["performance_measure"](param_vals, model, problem)
            success["objective_function"].append(obj)
        if not trial_result.success:
            failure["decision_variables"].append(param_vals)
            if algorithm["enable_trajectories"]:
                failure["trajectories"].append(trial_result.trajectories)
            failure["objective_function"].append(inf_obj_func)

    logging.debug("solvers.montecarlo_multiple_initial_value")
    logging.info("decision variables; objective function")
    logging.info(success["decision_variables"])
    logging.info(success["objective_function"])

    result = dict(montecarlo_multiple_simulation_result)
    result["succeeded"]["decision_variables"] = numpy.asarray(success["decision_variables"])
    result["succeeded"]["objective_function"] = numpy.asarray(success["objective_function"])
    result["failed"]["decision_variables"] = numpy.asarray(failure["decision_variables"])
    result["failed"]["objective_function"] = numpy.asarray(failure["objective_function"])
    if algorithm["enable_trajectories"]:
        result["succeeded"]["trajectories"] = numpy.asarray(success["trajectories"])
        result["failed"]["trajectories"] = numpy.asarray(failure["trajectories"])
    return result
