
import numpy
import scipy.integrate

import common.utilities
#import models.ordinary_differential

def solve_lsoda(model, initial_condition, timepoints, parameters, inputs):
    return scipy.integrate.odeint(
        func=model, \
        y0=initial_condition, \
        t=timepoints, \
        args=(parameters, inputs), \
        full_output=True, \
        printmessg=True, \
        ixpr=True)
    

def compute_trajectory(parameters, model, initial_condition, inputs, timepoints):
    trajectory_t, info = solve_lsoda(model, initial_condition, timepoints, parameters, inputs)
    trajectory = common.utilities.sliceit(trajectory_t)
    return trajectory


def compute_endpoint(inputs, model, initial_condition, timepoints, parameters):
    trajectory = compute_trajectory(inputs, model, initial_condition, timepoints, parameters)
    return trajectory[len(trajectory)-1]


def solve_ode_lsoda(model, initial_condition, timepoints, parameters, inputs):
    integrator = scipy.integrate.ode(model)
    integrator.set_f_params(parameters, inputs)
    integrator.set_integrator("lsoda")
    integrator.set_initial_value(y=initial_condition, t=0.0)
    
    ii = 0
    ts = []
    ts.append(timepoints[ii])
    ys = []
    ys. append(numpy.array([initial_condition]))
    tf = timepoints[len(timepoints)-1]
    
    while integrator.successful() and integrator.t < tf:
        ii += 1
        integrator.integrate(timepoints[ii])
        ts.append(integrator.t)
        ys.append(integrator.y)
    return ts, ys


# -----------------------------------------------------------------------------

def solve_lsoda_st(model, model_data, problem_data):
    model_data["parameters"] =  problem_data["parameters"]
    model_data["inputs"] = problem_data["inputs"]
    return scipy.integrate.odeint(
        func=model, \
        y0=problem_data["initial_conditions"], \
        t=problem_data["time"], \
        args=(model_data["parameters"], model_data["inputs"]), \
        full_output=True, \
        printmessg=True, \
        ixpr=True)


def compute_trajectory_st(model, model_data, problem_data):
    trajectory_t, info = solve_lsoda_st(model, model_data, problem_data)
    trajectory = common.utilities.sliceit(trajectory_t)
    return trajectory
