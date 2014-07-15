
import math
import solvers.initial_value

def residuals(parameters, model, times, inputs, initial_conditions, measured):
    res = measured - solvers.initial_value.compute_trajectory(parameters, model, initial_conditions, inputs, times)
    return res


def sum_squared_residuals(parameters, model, times, inputs, initial_conditions, measured):
    return math.fsum(res**2 for res in residuals(parameters, model, times, inputs, initial_conditions, measured))


def residuals_st(model, model_instance, problem_instance):
    measured = problem_instance["outputs"]
    predicted = solvers.initial_value.compute_trajectory_st(model, model_instance, problem_instance)
    res = []
    for meas, pred in zip(measured, predicted):
        res.append(meas - pred) 
    return res


def sum_squared_residuals_st(dof, model, model_instance, problem_instance):
    model_instance["parameters"] = dof
    problem_instance["parameters"] = dof
    return math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance))
