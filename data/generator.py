
# TODO: migrate to scipy
# TODO: rename to noise generator
import numpy.random

def set_seed(value):
    numpy.random.seed(value)

    
def unset_seed():
    numpy.random.seed()


def normal_distribution(count):
    return numpy.random.randn(count)


def uniform_distribution(count):
    return numpy.random.rand(count)
