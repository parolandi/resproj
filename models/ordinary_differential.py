
import numpy

import models.model_data

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


def linear_st(y, t, instance):
    assert(len(instance["states"]) == 1)
    assert(len(instance["parameters"]) == 1)
    assert(len(instance["inputs"]) == 1)
    instance["states"][0] = y
    return instance["parameters"][0] * instance["inputs"][0] - instance["states"][0]


def epo_receptor(states, time, params, inputs):
    d_dt = {
        "Epo": 0.0,
        "EpoR": 0.0,
        "Epo_EpoR": 0.0,
        "Epo_EpoR_i": 0.0,
        "dEpo_i": 0.0,
        "dEpi_e": 0.0,
    }
    v = {
        "1": 0.0,
        "2": 0.0,
        "3": 0.0,
        "4": 0.0,
        "5": 0.0,
        "6": 0.0,
        "7": 0.0,
        "8": 0.0,
    }
    v["1"] = params["k_on"]*states["Epo"]*states["EpoR"]
    v["2"] = params["k_off"]*states["Epo_EpoR"]
    v["3"] = params["k_t"]*inputs["B_max"]
    v["4"] = params["k_t"]*states["EpoR"]
    v["5"] = params["k_e"]*states["Epo_EpoR"]
    v["6"] = params["k_ex"]*states["Epo_EpoR_i"]
    v["7"] = params["k_di"]*states["Epo_EpoR_i"]
    v["8"] = params["k_de"]*states["Epo_EpoR_i"] 
    d_dt["Epo"] = -v["1"]+v["2"]+v["6"]
    d_dt["EpoR"] = -v["1"]+v["2"]+v["3"]-v["4"]+v["6"]
    d_dt["Epo_EpoR"] = v["1"]-v["2"]-v["5"]
    d_dt["Epo_EpoR_i"] = v["5"]-v["6"]-v["7"]-v["8"]
    d_dt["dEpo_i"] = v["7"]
    d_dt["dEpo_e"] = v["8"]
    return numpy.array([d_dt["Epo"], d_dt["EpoR"], d_dt["Epo_EpoR"], d_dt["Epo_EpoR_i"], d_dt["dEpo_i"], d_dt["dEpo_e"]])
