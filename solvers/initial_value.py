
import numpy
import scipy.integrate

import common.utilities
import models.ordinary_differential

def solve_lsoda(model, initial_condition, timepoints, parameters, alginputs):
    return scipy.integrate.odeint(
        func=models.ordinary_differential.linear, \
        y0=initial_condition, \
        t=timepoints, \
        args=(parameters, alginputs), \
        full_output=True, \
        printmessg=True, \
        ixpr=True)
    

def compute_trajectory(parameters, model, initial_condition, alginputs, timepoints):
    trajectory_t, info = solve_lsoda(model, initial_condition, timepoints, parameters, alginputs)
    trajectory = common.utilities.sliceit(trajectory_t)
    return trajectory


def compute_endpoint(alginputs, model, initial_condition, timepoints, parameters):
    trajectory = compute_trajectory(alginputs, model, initial_condition, timepoints, parameters)
    return trajectory[len(trajectory)-1]


def solve_ode_lsoda(model, initial_condition, timepoints, parameters, alginputs):
    integrator = scipy.integrate.ode(model)
    integrator.set_f_params(parameters, alginputs)
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
