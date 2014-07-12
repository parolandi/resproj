
import scipy.integrate

# TODO: change to gain and time constant and first order
def linear(diffstates, time, parameters, alginputs):
    assert(len(diffstates) == 1)
    assert(len(parameters) == 1)
    assert(len(alginputs) == 1)
    return parameters[0] * alginputs[0] - diffstates[0]


# TODO: change to gain and time constant and first order
def linear_ty(time, diffstates, parameters, alginputs):
    assert(len(diffstates) == 1)
    assert(len(parameters) == 1)
    assert(len(alginputs) == 1)
    return parameters[0] * alginputs[0] - diffstates[0]
