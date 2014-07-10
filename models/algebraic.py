
def linear(p, x):
    return p * x

def jacobian_linear(p, x, model, y):
    return -x

def quadratic(p, x):
    return p * x**2

def jacobian_quadratic(p, x, model, y):
    return -x**2
