
import scipy.optimize

# TODO: validate use of data structure
import solvers.solver_data


# return scipy.OptimizeResult
def solve(model, model_instance, problem_instance, algorithm_instance):
    t0 = 0.0
    return scipy.optimize.root( \
        fun = model, \
        x0 = algorithm_instance["initial_guesses"], \
        args = (t0, model_instance["parameters"], model_instance["inputs"]), \
        method = algorithm_instance["method"], \
        jac = None, \
        tol = algorithm_instance["tolerance"], \
        callback = None,
        options = None)
