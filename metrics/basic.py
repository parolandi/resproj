
import model

def residual_linear(p, x, measured):
    residual = measured - model.algebraic.linear(p, x)
    return residual

def residual(parameters, independent, function, measured):
    residual = measured - function(parameters, independent)
    return residual