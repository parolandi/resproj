
# TODO: migrate to scipy
import numpy.random

def set_seed(value):
    numpy.random.seed(value)

    
def unset_seed():
    numpy.random.seed()


def normal_distribution(count):
    return numpy.random.randn(count)
