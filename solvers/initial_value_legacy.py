
import numpy
import scipy.integrate

import common.utilities


'''
It calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's
'''
def solve_lsoda(model, initial_condition, timepoints, parameters, inputs):
    y, data, _ = scipy.integrate.odeint(
        func = model, \
        y0 = initial_condition, \
        t = timepoints, \
        args = (parameters, inputs), \
        full_output = True, \
        printmessg = True,
        ixpr = True)
    return y, data
    

def compute_trajectory(parameters, model, initial_condition, inputs, timepoints):
    trajectory_t, info = solve_lsoda(model, initial_condition, timepoints, parameters, inputs)
    trajectory = common.utilities.sliceit_assnapshot(trajectory_t)
    return trajectory


def compute_endpoint(inputs, model, initial_condition, timepoints, parameters):
    trajectory = compute_trajectory(parameters, model, initial_condition, inputs, timepoints)
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
