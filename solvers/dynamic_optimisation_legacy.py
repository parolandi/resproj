
import scipy.optimize

import solvers.initial_value_legacy


def solve_slsqp_optimise_with_bounds(objective, model, initial_guess, initial_conditions, t, p, simple_bounds):
    return scipy.optimize.minimize( \
        fun=objective, x0=initial_guess, args=(model, initial_conditions, t, p), method='SLSQP', bounds=simple_bounds)


def maximise_it(inputs, model, initial_condition, timepoints, parameters):
    return -1.0 * solvers.initial_value_legacy.compute_endpoint(inputs, model, initial_condition, timepoints, parameters)


def minimise_it(inputs, model, initial_condition, timepoints, parameters):
    return solvers.initial_value_legacy.compute_endpoint(inputs, model, initial_condition, timepoints, parameters)
