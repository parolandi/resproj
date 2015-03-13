
import scipy.optimize

import metrics.ordinary_differential as mod


# WIP: change name
def constraint_it(x, model_data, problem_data, ssr_0):
    index = problem_data["confidence_region"]["parameter_index"]
    model_data["parameters"][index] = x[0]
    problem_data["parameters"][index] = x[0]
    return ssr_0 - mod.sum_squared_residuals_st(None, None, model_data, problem_data)


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


# WIP: change name
def maximise_it(x):
    return -1.0 * x


def minimise_it(x):
    return x
