
import math

def residuals(parameters, independent, function, measured):
    res = measured - function(parameters, independent)
    return res


def sum_squared_residuals(parameters, independent, function, measured):
    return math.fsum(res**2 for res in residuals(parameters, independent, function, measured))


def sum_absolute_value_residuals(values):
    return math.fsum([math.fabs(value) for value in values])
