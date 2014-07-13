
# TODO: change to gain and time constant and first order
def linear(states, time, parameters, inputs):
    assert(len(states) == 1)
    assert(len(parameters) == 1)
    assert(len(inputs) == 1)
    return parameters[0] * inputs[0] - states[0]


# TODO: change to gain and time constant and first order
def linear_ty(time, states, parameters, inputs):
    assert(len(states) == 1)
    assert(len(parameters) == 1)
    assert(len(inputs) == 1)
    return parameters[0] * inputs[0] - states[0]
