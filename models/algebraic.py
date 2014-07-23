
def linear(p, x):
    return p * x


def jacobian_linear(p, x, model, y):
    return -x


def quadratic(p, x):
    return p * x**2


def jacobian_quadratic(p, x, model, y):
    return -x**2


# runs a single realisation
def linear_2p2s(p, x):
    assert(len(p) == 2)
    assert(len(x) == 2)
    y = p * x
    return y
