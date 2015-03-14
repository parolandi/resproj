
import math
import numpy


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


def linear_2p2s(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    
    dx_dt = p * u - x
    return dx_dt


# note that in this particular case there is no dependence x
# that's the reason we can compute the sensitivities so trivially
def sensitivities_linear_2p2s(s, t, p, u):
    assert(len(s) == 4)
    assert(len(p) == 2)
    assert(len(u) == 2)
    
    ds_dt = []
    ds_dt.append(u[0] - s[0])
    ds_dt.append(0.0)
    ds_dt.append(0.0)
    ds_dt.append(u[1] - s[3])
    return ds_dt


'''
Compute full augmented state and sensitivity system
d: indices of decision variables for parameters p
'''
#TODO: add dp
def state_and_sensitivities_linear_2p2s(xs, t, p, u):
    assert(len(xs) == 6)
    assert(len(p) == 2)
    assert(len(u) == 2)
#    assert(len(dp) == 2)
    
    dx_dt = []
    dx_dt.append(p[0] * u[0] - xs[0])
    dx_dt.append(p[1] * u[1] - xs[1])
    
    ds_dt = []
    ds_dt.append(u[0] - xs[2])
    ds_dt.append(0.0)
    ds_dt.append(0.0)
    ds_dt.append(u[1] - xs[5])
    
    dxs_dt = numpy.concatenate((dx_dt, ds_dt))
    return dxs_dt


def nonlinear_2p2s(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    
    dx_dt = [0,0]
    dx_dt[0] = p[0] * u[0] - 2*math.sqrt(x[0])
    dx_dt[1] = p[1] * u[1] - 2*math.sqrt(x[1])
    return dx_dt


# TODO: perhpas move to epo_receptor module?
epo_receptor_default_parameters = {
    "k_on": 0.00010496,
    "k_off": 0.0172135,
    "k_t": 0.0329366,
    "k_e": 0.0748267,
    "k_ex": 0.00993805,
    "k_di": 0.00317871,
    "k_de": 0.0164042,
}


epo_receptor_states = {
    "Epo": 0.0,
    "EpoR": 0.0,
    "Epo_EpoR": 0.0,
    "Epo_EpoR_i": 0.0,
    "dEpo_i": 0.0,
    "dEpo_e": 0.0,
}


epo_receptor_default_inputs = {
    "B_max": 516,
}


epo_receptor_velocities = {
    "1": 0.0,
    "2": 0.0,
    "3": 0.0,
    "4": 0.0,
    "5": 0.0,
    "6": 0.0,
    "7": 0.0,
    "8": 0.0,
}


# dictionary-based model
def epo_receptor_di(states, time, params, inputs):
    v = epo_receptor_velocities
    v["1"] = params["k_on"]*states["Epo"]*states["EpoR"]
    v["2"] = params["k_off"]*states["Epo_EpoR"]
    v["3"] = params["k_t"]*inputs["B_max"]
    v["4"] = params["k_t"]*states["EpoR"]
    v["5"] = params["k_e"]*states["Epo_EpoR"]
    v["6"] = params["k_ex"]*states["Epo_EpoR_i"]
    v["7"] = params["k_di"]*states["Epo_EpoR_i"]
    v["8"] = params["k_de"]*states["Epo_EpoR_i"] 
    d_dt = epo_receptor_states
    d_dt["Epo"] = -v["1"]+v["2"]+v["6"]
    d_dt["EpoR"] = -v["1"]+v["2"]+v["3"]-v["4"]+v["6"]
    d_dt["Epo_EpoR"] = v["1"]-v["2"]-v["5"]
    d_dt["Epo_EpoR_i"] = v["5"]-v["6"]-v["7"]-v["8"]
    d_dt["dEpo_i"] = v["7"]
    d_dt["dEpo_e"] = v["8"]
    return numpy.array([d_dt["Epo"], d_dt["EpoR"], d_dt["Epo_EpoR"], d_dt["Epo_EpoR_i"], d_dt["dEpo_i"], d_dt["dEpo_e"]])


params_i = {
    "k_on": 0,  # Epo
    "k_off": 1, # Epo
    "k_t": 2,
    "k_e": 3,
    "k_ex": 4,  # Epo
    "k_di": 5,
    "k_de": 6,
}


states_i = {
    "Epo": 0,
    "EpoR": 1,
    "Epo_EpoR": 2,
    "Epo_EpoR_i": 3,
    "dEpo_i": 4,
    "dEpo_e": 5,
}


inputs_i = {
    "B_max": 0,
}

# TODO: extract into dedicated module
# array-based model
def epo_receptor(states, time, params, inputs):
    v = numpy.zeros(len(epo_receptor_velocities))
    v[0] = params[params_i["k_on"]]*states[states_i["Epo"]]*states[states_i["EpoR"]]    # Epo
    v[1] = params[params_i["k_off"]]*states[states_i["Epo_EpoR"]]                       # Epo
    v[2] = params[params_i["k_t"]]*inputs[inputs_i["B_max"]]
    v[3] = params[params_i["k_t"]]*states[states_i["EpoR"]]
    v[4] = params[params_i["k_e"]]*states[states_i["Epo_EpoR"]]
    v[5] = params[params_i["k_ex"]]*states[states_i["Epo_EpoR_i"]]                      # Epo
    v[6] = params[params_i["k_di"]]*states[states_i["Epo_EpoR_i"]]
    v[7] = params[params_i["k_de"]]*states[states_i["Epo_EpoR_i"]] 
    d_dt = numpy.zeros(len(states))
    d_dt[states_i["Epo"]] = -v[1-1]+v[2-1]+v[6-1]
    d_dt[states_i["EpoR"]] = -v[1-1]+v[2-1]+v[3-1]-v[4-1]+v[6-1]
    d_dt[states_i["Epo_EpoR"]] = v[1-1]-v[2-1]-v[5-1]
    d_dt[states_i["Epo_EpoR_i"]] = v[5-1]-v[6-1]-v[7-1]-v[8-1]
    d_dt[states_i["dEpo_i"]] = v[7-1]
    d_dt[states_i["dEpo_e"]] = v[8-1]
    return d_dt


def J_epo_receptor(dof, states, time, params, inputs):
    assert(len(dof) == 1)
    params[0] = dof[0]
    J = numpy.zeros(len(states))
    dv0_dp0 = states[states_i["Epo"]]*states[states_i["EpoR"]]
    J[0] = -dv0_dp0 
    J[1] = -dv0_dp0
    J[2] = dv0_dp0
    return J.transpose()
    
# array-based model
def epo_receptor_nonneg(states, time, params, inputs):
    correct_states = True
    correct_time_derivs = True
    states_l = states
    if correct_states:
        if states[states_i["Epo"]] <= 0.0:
            states[states_i["Epo"]] = 0.0
        if states[states_i["EpoR"]] <= 0.0:
            states[states_i["EpoR"]] = 0.0
        if states[states_i["Epo_EpoR"]] <= 0.0:
            states[states_i["Epo_EpoR"]] = 0.0
        if states[states_i["Epo_EpoR_i"]] <= 0.0:
            states[states_i["Epo_EpoR_i"]] = 0.0
        if states[states_i["dEpo_i"]] <= 0.0:
            states[states_i["dEpo_i"]] = 0.0
        if states[states_i["dEpo_e"]] <= 0.0:
            states[states_i["dEpo_e"]] = 0.0
    v = numpy.zeros(len(epo_receptor_velocities))
    v[0] = params[params_i["k_on"]]*states[states_i["Epo"]]*states[states_i["EpoR"]]
    v[1] = params[params_i["k_off"]]*states[states_i["Epo_EpoR"]]
    v[2] = params[params_i["k_t"]]*inputs[inputs_i["B_max"]]
    v[3] = params[params_i["k_t"]]*states[states_i["EpoR"]]
    v[4] = params[params_i["k_e"]]*states[states_i["Epo_EpoR"]]
    v[5] = params[params_i["k_ex"]]*states[states_i["Epo_EpoR_i"]]
    v[6] = params[params_i["k_di"]]*states[states_i["Epo_EpoR_i"]]
    v[7] = params[params_i["k_de"]]*states[states_i["Epo_EpoR_i"]] 
    d_dt = numpy.zeros(len(states))
    d_dt[states_i["Epo"]] = -v[1-1]+v[2-1]+v[6-1]
    d_dt[states_i["EpoR"]] = -v[1-1]+v[2-1]+v[3-1]-v[4-1]+v[6-1]
    d_dt[states_i["Epo_EpoR"]] = v[1-1]-v[2-1]-v[5-1]
    d_dt[states_i["Epo_EpoR_i"]] = v[5-1]-v[6-1]-v[7-1]-v[8-1]
    d_dt[states_i["dEpo_i"]] = v[7-1]
    d_dt[states_i["dEpo_e"]] = v[8-1]
    if correct_time_derivs:
        if states[states_i["Epo"]] <= 0.0 and d_dt[states_i["Epo"]] <= 0.0:
            d_dt[states_i["Epo"]] = 0.0
        if states[states_i["EpoR"]] <= 0.0 and d_dt[states_i["EpoR"]] <= 0.0:
            d_dt[states_i["EpoR"]] = 0.0
        if states[states_i["Epo_EpoR"]] <= 0.0 and d_dt[states_i["Epo_EpoR"]] <= 0.0:
            d_dt[states_i["Epo_EpoR"]] = 0.0
        if states[states_i["Epo_EpoR_i"]] <= 0.0 and d_dt[states_i["Epo_EpoR_i"]] <= 0.0:
            d_dt[states_i["Epo_EpoR_i"]] = 0.0
        if states[states_i["dEpo_i"]] <= 0.0 and d_dt[states_i["dEpo_i"]] <= 0.0:
            d_dt[states_i["dEpo_i"]] = 0.0
        if states[states_i["dEpo_e"]] <= 0.0 and d_dt[states_i["dEpo_e"]] <= 0.0:
            d_dt[states_i["dEpo_e"]] = 0.0
        states = states_l
    return d_dt
