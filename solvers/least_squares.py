
import scipy.optimize

def solve(metric, model, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True)

def solve_with_jacobian(metric, model, jacobian, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True, Dfun=jacobian)
