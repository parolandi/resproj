
import numpy.random

def set_seed(value):
    numpy.random.seed(value)
    return
    
def unset_seed():
    numpy.random.seed()
    return

def normal_distribution(count):
    return numpy.random.randn(count)

