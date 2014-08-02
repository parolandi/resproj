
import math
import numpy

import common.utilities
import solvers.initial_value
import solvers.initial_value_legacy


def residuals(parameters, model, times, inputs, initial_conditions, measured):
    res = measured - solvers.initial_value_legacy.compute_trajectory(parameters, model, initial_conditions, inputs, times)
    return res


def sum_squared_residuals(parameters, model, times, inputs, initial_conditions, measured):
    return math.fsum(res**2 for res in residuals(parameters, model, times, inputs, initial_conditions, measured))



def simple_residuals_st(model, model_instance, problem_instance):
    measured = problem_instance["outputs"]
    predicted = solvers.initial_value.compute_trajectory_st(model, model_instance, problem_instance)
    res = []
    for meas, pred in zip(measured, predicted):
        res.append(meas - pred) 
    return res


def simple_sum_squared_residuals_st(dof, model, model_instance, problem_instance):
    model_instance["parameters"] = dof
    problem_instance["parameters"] = dof
    return math.fsum(res**2 for res in simple_residuals_st(model, model_instance, problem_instance))


def residuals_st(model, model_instance, problem_instance):
    # TODO: preconditions    
    measured = numpy.asarray(problem_instance["outputs"])
    result = solvers.initial_value.compute_trajectory_st(model, model_instance, problem_instance)
    predicted = common.utilities.sliceit_astrajectory(result)
    # there is one residual per experiment
    # but for the moment there is also a single experiment
    # there is one residual per state (and per experiment)
    res = 0
    # TODO: more pythonic
    if len(measured.shape) == 1:
        measured_s = measured
        predicted_s = predicted[problem_instance["output_indices"][0]]
        res = numpy.subtract(measured_s, predicted_s)
        return res
    states = 0
    res = numpy.empty(measured.shape)
    for jj in range(measured.shape[states]):
        measured_s = measured[jj]
        predicted_s = predicted[problem_instance["output_indices"][jj]]
        res[jj] = numpy.subtract(measured_s, predicted_s)
    return res


# TODO: compute state-wise and experiment-wise
def sum_squared_residuals_st(dof, model, model_instance, problem_instance):
    # TODO: preconditions
    # TODO: more pythonic
    if len(problem_instance["parameter_indices"]) > 0:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            model_instance["parameters"][index] = dof[ii]
            problem_instance["parameters"][ii] = dof[ii]
    
    # TODO: more pythonic
    res = 0.0
    if len(problem_instance["output_indices"]) == 1:
        res = math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance))
        return res
    for ii in range(len(problem_instance["outputs"])):
        res += math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance)[ii])
    return res
