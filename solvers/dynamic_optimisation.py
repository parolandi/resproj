
import scipy.optimize

import metrics.ordinary_differential as mod

import copy
import numpy


# WIP: change name
# TODO: is this a bug?!
def constraint_it(x, model_data, problem_data, ssr_0):
    index = problem_data["confidence_region"]["parameter_index"]
    model_data["parameters"][index] = x[0]
    problem_data["parameters"][index] = x[0]
    return ssr_0 - mod.sum_squared_residuals_st(None, None, model_data, problem_data)


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
    
    result = scipy.optimize.minimize( \
        fun = problem["performance_measure"], \
        constraints = constraints, \
        x0 = algorithm["initial_guesses"], \
        method = algorithm["method"], \
        bounds = problem["bounds"])
    return result


def solve_std(model, problem, algorithm):
    p0 = copy.deepcopy(problem["parameters"])
    index = problem["confidence_region"]["parameter_index"]
    
    if problem["constraints"] is not None:
        result = scipy.optimize.minimize( \
            fun = problem["performance_measure"], \
            args = (p0, index), \
            constraints = problem["constraints"], \
            x0 = algorithm["initial_guesses"], \
            method = algorithm["method"], \
            bounds = problem["bounds"])
    else:
        result = scipy.optimize.minimize( \
            fun = problem["performance_measure"], \
            args = (p0, problem["confidence_region"]["parameter_index"]), \
            x0 = algorithm["initial_guesses"], \
            method = algorithm["method"], \
            bounds = problem["bounds"])
        
    return result


# WIP: change name
def maximise_it(x):
    return -1.0 * x


def minimise_it(x):
    return x


def maximise_distance(x, x0):
    delta = numpy.asarray(x - x0)
    distance = (-1) * numpy.dot(delta, delta)
    #print("distance", distance) 
    return distance
