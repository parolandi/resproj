
import math

import models

def residual_linear(p, x, measured):
    residual = measured - models.algebraic.linear(p, x)
    return residual

def residual(parameters, independent, function, measured):
    residual = measured - function(parameters, independent)
    return residual

def sum_absolute_value_residuals(values):
    sum_abs_res = 0
    for value in values:
        sum_abs_res += math.fabs(value)
    return sum_abs_res
        