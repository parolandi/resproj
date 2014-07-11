
import scipy.integrate

import models.differentialalgebraic

def solve_lsoda(model, initial_condition, timepoints, parameters, alginputs):
    return scipy.integrate.odeint(
        func=models.differentialalgebraic.linear, \
        y0=initial_condition, \
        t=timepoints, \
        args=(parameters, alginputs), \
        full_output=True, \
        printmessg=True, \
        ixpr=True)