
import scipy.integrate

import common.utilities
import models.differential_algebraic

def solve_lsoda(model, initial_condition, timepoints, parameters, alginputs):
    return scipy.integrate.odeint(
        func=models.differential_algebraic.linear, \
        y0=initial_condition, \
        t=timepoints, \
        args=(parameters, alginputs), \
        full_output=True, \
        printmessg=True, \
        ixpr=True)
    
def compute_trajectory(alginputs, model, initial_condition, timepoints, parameters):
    trajectory_t, info = solve_lsoda(model, initial_condition, timepoints, parameters, alginputs)
    trajectory = common.utilities.sliceit(trajectory_t)
    return trajectory[len(trajectory)-1]
