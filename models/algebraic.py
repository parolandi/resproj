
import numpy

def linear(p, x):
    return p * x

def jacobian_linear(p, x, dummy, y):
    return -x
