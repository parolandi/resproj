
import models

def residual_linear(p, x, measured):
    residual = measured - models.algebraic.linear(p, x)
    return residual