
import models

def residual_linear(p, x, measured):
    residual = measured - models.algebraic.linear(p, x)
    return residual

def residual(parameters, independent, function, measured):
    residual = measured - function(parameters, independent)
    return residual