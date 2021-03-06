
import numpy
import scipy.optimize

import logging

import metrics.ordinary_differential as mod


# WIP: change name
# TODO: is this a bug?!
def constraint_it(x, model_data, problem_data, ssr_0):
    index = problem_data["confidence_region"]["parameter_index"]
    model_data["parameters"][index] = x[0]
    problem_data["parameters"][index] = x[0]
    # WIP 2015-04-16
    return ssr_0 - mod.sum_squared_residuals(None, model_data, problem_data)


#TODO: rename, perhaps nonstandard
def solve(model, problem, algorithm):

    if algorithm["method"] == 'SLSQP':
        ssr0 = problem["confidence_region"]["ssr"]
        constraints = {'type': 'ineq', \
                       'fun': constraint_it, \
                       'args': (model, problem, ssr0)}
    else:
        assert(problem["constraints"] is None)
        # can't handle anything else
        assert(False)

    settings = {}
    settings["maxiter"] = 100
    #settings["maxiter"] = 500
    #settings["eps"] = 1e-6

    result = scipy.optimize.minimize( \
        fun = problem["performance_measure"], \
        constraints = constraints, \
        x0 = algorithm["initial_guesses"], \
        method = algorithm["method"], \
        bounds = problem["bounds"], \
        options = settings)
    
    logging.debug("solvers.dynamic_optimisation.solve")
    logging.info("algorithm :\n" + str(algorithm))
    logging.info("result :\n" + str(result))
    return result


def solve_std(model, problem, algorithm):
    result = None
    settings = {}
    settings["maxiter"] = 100
    #settings["maxiter"] = 500
    #settings["eps"] = 1e-6
    
    if not has_obj_args(problem) and is_unconstrained(problem):
        result = scipy.optimize.minimize( \
            fun = problem["performance_measure"], \
            x0 = algorithm["initial_guesses"], \
            method = algorithm["method"], \
            bounds = problem["bounds"], \
            callback = algorithm["callback"], \
            options = settings)
    
    if not has_obj_args(problem) and not is_unconstrained(problem):
        result = scipy.optimize.minimize( \
            fun = problem["performance_measure"], \
            constraints = problem["constraints"], \
            x0 = algorithm["initial_guesses"], \
            method = algorithm["method"], \
            bounds = problem["bounds"], \
            callback = algorithm["callback"], \
            options = settings)

    if has_obj_args(problem) and is_unconstrained(problem):
        result = scipy.optimize.minimize( \
            fun = problem["performance_measure"], \
            args = problem["performance_measure_args"], \
            x0 = algorithm["initial_guesses"], \
            method = algorithm["method"], \
            bounds = problem["bounds"], \
            callback = algorithm["callback"], \
            options = settings)

    if has_obj_args(problem) and not is_unconstrained(problem):
        result = scipy.optimize.minimize( \
            fun = problem["performance_measure"], \
            args = problem["performance_measure_args"], \
            constraints = problem["constraints"], \
            x0 = algorithm["initial_guesses"], \
            method = algorithm["method"], \
            bounds = problem["bounds"], \
            callback = algorithm["callback"], \
            options = settings)

    assert(result is not None)
    logging.debug("solvers.dynamic_optimisation.solve")
    logging.info("algorithm :\n" + str(algorithm))
    logging.info("result :\n" + str(result))
    return result


# WIP: change name
def maximise_it(x):
    return -1.0 * x


def minimise_it(x):
    return x


def maximise_distance(x, x0):
    delta = numpy.asarray(x - x0)
    distance = (-1) * numpy.dot(delta, delta)
    return distance


def has_obj_args(problem):
    return problem["performance_measure_args"] is not None


def is_unconstrained(problem):
    return len(problem["constraints"]) == 0