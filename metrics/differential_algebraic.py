
import math
import solvers.initial_value

def residuals(parameters, model, times, inputs, initial_conditions, measured):
    res = measured - solvers.initial_value.compute_trajectory(parameters, model, initial_conditions, inputs, times)
    return res


def sum_squared_residuals(parameters, model, times, inputs, initial_conditions, measured):
    return math.fsum(res**2 for res in residuals(parameters, model, times, inputs, initial_conditions, measured))
