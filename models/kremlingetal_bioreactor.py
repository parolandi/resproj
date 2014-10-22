
import numpy


pmap = {
    "Yxs": 0, #
    "r1max": 1,
    "KS": 2,
    "k2": 3, #
    "KM1": 4,
    "KIA": 5, # 
    "r3max": 6,
    "KM2": 7,
    "ksynmax": 8, #
    "KIB": 9, #
    }


# Table 2 and Table 9, with correction following contact with Andreas
pvec = {
    "Yxs": 7E-5,       # g/umol      - Table 9
    "r1max": 2.4E4,    # umol/g/h DW - Table 2
    "KS": 0.4437,      # umol/g DW   - Table 2
    "k2": 6E6,         # L/h         - Table 9
    "KM1": 12.2,       # umol/g DW   - Table 2
    "KIA": 10.0,       # umol/g DW   - Table 9
    "r3max": 3E6,      # umol/g DW   - Table 2
    "KM2": 10.0,       # umol/g DW   - Table 2
    "ksynmax": 0.0168, # umol/g/h DW - Table 9
    "KIB": 0.01,       # umol/g DW   - Table 9
    }


# Table 2 and Table 3; modelA
pvec_table3_modelA = {
    "Yxs": 6.968E-5,   # g/umol      - Table 3
    "r1max": 2.4E4,    # umol/g/h DW - Table 2
    "KS": 0.4437,      # umol/g DW   - Table 2
    "k2": 5.988E6,     # L/h         - Table 3
    "KM1": 12.2,       # umol/g DW   - Table 2
    "KIA": 0.104,      # umol/g DW   - Table 3
    "r3max": 3E6,      # umol/g DW   - Table 2
    "KM2": 10.0,       # umol/g DW   - Table 2
    "ksynmax": 7.2E-3, # umol/g/h DW - Table 3
    "KIB": 0.0,        # umol/g DW   - Table 3
    }


# Table 2 and Table 3; modelB
pvec_table3_modelB = {
    "Yxs": 7.031E-5,   # g/umol      - Table 3
    "r1max": 2.4E4,    # umol/g/h DW - Table 2
    "KS": 0.4437,      # umol/g DW   - Table 2
    "k2": 5.559E6,     # L/h         - Table 3
    "KM1": 12.2,       # umol/g DW   - Table 2
    "KIA": 0.0,        # umol/g DW   - Table 3
    "r3max": 3E6,      # umol/g DW   - Table 2
    "KM2": 10.0,       # umol/g DW   - Table 2
    "ksynmax": 8.2E-3, # umol/g/h DW - Table 3
    "KIB": 0.166,      # umol/g DW   - Table 3
    }


xmap = {
    "V": 0,
    "X": 1,
    "S": 2,
    "M1": 3,
    "M2": 4,
    "E": 5, # M3
    }


xvec = {
    "V": 1, # L
    "X": 0.1, # g/L
    "S": 2.0, # g/L 
    "M1": 0.07, # umol/g DW
    "M2": 0.01, # umol/g DW
    "E": 0.07, # umol/g DW # M3
    }


umap = {
    "qin": 0,
    "qout": 1,
    "cin": 2,
    }


uvec_0h = {
    "qin": 0.25, # L/h
    "qout": 0.25, # L/h
    "cin": 2.0, # g/L
    }


uvec_20h = {
    "qin": 0.35,
    "qout": 0.35,
    "cin": 2.0,
    }


uvec_30h = {
    "qin": 0.35,
    "qout": 0.35,
    "cin": 0.5,
    }


ymap = {
    "mu": 0,
    "r1": 1,
    "r2": 2,
    "r3": 3,  
    "rsyn": 4,
    }


yvec = {
    "mu": 0, # [1/h]
    "r1": 0,
    "r2": 0,
    "r3": 0,    
    "rsyn": 0,
    }

# x: states
# t: time
# p: parameters
# u: inputs
def evaluate(x, t, p, u, model_form):
    for ii in range(len(x)):
        if x[ii] < 0:
            x[ii] = 0.0
    
    Mw = 342.3 * 1E-6 # molar mass of substrate
    # [g/umol] = [g/mol] * [mol/umol]

    y = numpy.zeros(len(yvec))
    y[ymap["r1"]] = p[pmap["r1max"]] * x[xmap["S"]] / (p[pmap["KS"]] + x[xmap["S"]])
    #             = [umol/g/h DW]    * [g/L]        / (              + [g/L])
    y[ymap["mu"]] = p[pmap["Yxs"]] * y[ymap["r1"]]
    # [1/h]       = [g/umol]       * [umol/g/h DW] 
    if model_form == "modelA":
        y[ymap["r2"]] = p[pmap["k2"]] * x[xmap["E"]] * x[xmap["M1"]] / (p[pmap["KM1"]] + x[xmap["M1"]]) * p[pmap["KIA"]] / (p[pmap["KIA"]] + x[xmap["M2"]])
        y[ymap["rsyn"]] = p[pmap["ksynmax"]]
    else:
        y[ymap["r2"]] = p[pmap["k2"]] * x[xmap["E"]] * x[xmap["M1"]] / (p[pmap["KM1"]] + x[xmap["M1"]])
        y[ymap["rsyn"]] = p[pmap["ksynmax"]] * p[pmap["KIB"]] / (p[pmap["KIB"]] + x[xmap["M2"]])
        # [umol/g/h DW] = [umol/g/h DW]
    y[ymap["r3"]] = p[pmap["r3max"]] * x[xmap["M2"]] / (p[pmap["KM2"]] + x[xmap["M2"]])

    dx_dt = numpy.zeros(len(x)) 
    dx_dt[xmap["V"]] = u[umap["qin"]] - u[umap["qout"]]
    dx_dt[xmap["X"]] = (y[ymap["mu"]] - u[umap["qin"]] / x[xmap["V"]]) * x[xmap["X"]]
    # [g/L/h]        = ([1/h]         - [L/h]          / [L]         ) * [g/L]
    dx_dt[xmap["S"]] = u[umap["qin"]] * (u[umap["cin"]] - x[xmap["S"]]) - y[ymap["r1"]] * Mw * x[xmap["X"]]
    # [g/L/h]        = [L/h]          * ([g/L]          - [g/L]       ) - [umol/g/h DW] * [g/umol] * [g/L]
    # missing a V   
    dx_dt[xmap["M1"]] = y[ymap["r1"]] - y[ymap["r2"]] - y[ymap["mu"]] * x[xmap["M1"]]
    #                                                 - [1/h]         * [umol/g-DW]
    dx_dt[xmap["M2"]] = y[ymap["r2"]] - y[ymap["r3"]] - y[ymap["mu"]] * x[xmap["M2"]]
    #
    dx_dt[xmap["E"]] = y[ymap["rsyn"]] - y[ymap["mu"]] * x[xmap["E"]]
    #                = [umol/g/h DW]   - [1/h]         * [umol/g DW]
    
    return dx_dt


def evaluate_modelA(x, t, p, u):
    return evaluate(x, t, p, u, "modelA")


def evaluate_modelB(x, t, p, u):
    return evaluate(x, t, p, u, "modelB")
