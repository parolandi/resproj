
import scipy.optimize

def solve(metric, model, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True)