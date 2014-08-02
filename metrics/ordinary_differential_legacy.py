
import math

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
