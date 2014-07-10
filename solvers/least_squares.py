
import scipy.optimize

def solve_leastsq(metric, model, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True)

def solve_leastsq_with_jacobian(metric, model, jacobian, initial_guess, inputs, outputs):
    return scipy.optimize.leastsq(metric, initial_guess, args=(inputs, model, outputs), full_output=True, Dfun=jacobian)

def solve_slsqp(metric, model, initial_guess, inputs, outputs):
    return scipy.optimize.minimize(fun=metric, x0=initial_guess, args=(inputs, model, outputs), method='SLSQP')
