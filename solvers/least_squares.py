
import numpy
import scipy.optimize

def solve_leastsq(metric, model, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True)


def solve_leastsq_with_jacobian(metric, model, jacobian, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True, Dfun=jacobian)


def solve_slsqp(metric, model, initial_guess, inputs, outputs):
    return scipy.optimize.minimize(fun=metric, x0=initial_guess, args=(inputs, model, outputs), method='SLSQP')


def solve_slsqp_orddiff(metric, model, initial_guess, inputs, outputs, initial_conditions, t):
    return scipy.optimize.minimize( \
        fun=metric, x0=initial_guess, args=(model, t, inputs, initial_conditions, outputs), method='SLSQP')


algorithm_structure = {
    "method": "",
    "initial_guesses": numpy.empty(1),
    }


def solve_slsqp_orddiff_st(metric, model, model_instance, problem_instance, algorithm_structure):
    return scipy.optimize.minimize( \
        fun=metric, \
        x0=algorithm_structure["initial_guesses"], \
        args=(model, model_instance, problem_instance), \
        method=algorithm_structure["method"])
