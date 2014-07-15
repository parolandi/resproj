
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


model_structure = {
    "parameters": [],
    "inputs": [],
    "states": [],
    "outputs": [],
    "time": 0.0,
    }


problem_structure = {
    "initial_conditions": [],
    "time": [],
    "performance_measure": "",
    "model": "",
    "parameters": [],
    "inputs": [],
    "outputs": [],
    }


def linear_st(y, t, instance):
    assert(len(instance["states"]) == 1)
    assert(len(instance["parameters"]) == 1)
    assert(len(instance["inputs"]) == 1)
    instance["states"][0] = y
    return instance["parameters"][0] * instance["inputs"][0] - instance["states"][0]