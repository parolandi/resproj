
import scipy.optimize

import solvers.differentialalgebraic

def solve_slsqp_optimise_with_bounds(objective, model, initial_guess, initial_conditions, t, p, simple_bounds):
    return scipy.optimize.minimize( \
        fun=objective, x0=initial_guess, args=(model, initial_conditions, t, p), method='SLSQP', bounds=simple_bounds)


def maximise_it(alginputs, model, initial_condition, timepoints, parameters):
    return -1.0 * solvers.differentialalgebraic.compute_trajectory(alginputs, model, initial_condition, timepoints, parameters)


def minimise_it(alginputs, model, initial_condition, timepoints, parameters):
    return solvers.differentialalgebraic.compute_trajectory(alginputs, model, initial_condition, timepoints, parameters)
    