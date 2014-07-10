
import math

def residuals(parameters, independent, function, measured):
    res = measured - function(parameters, independent)
    return res

def sum_squared_residuals(parameters, independent, function, measured):
    ssr = 0
    for res in residuals(parameters, independent, function, measured):
        ssr += res**2
    return ssr

def sum_absolute_value_residuals(values):
    sar = 0
    for value in values:
        sar += math.fabs(value)
    return sar
