
import models

def residual_linear(p, x, measured):
    residuals = measured - models.algebraic.linear(p, x)
    return residuals