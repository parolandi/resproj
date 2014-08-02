
import scipy.optimize

# TODO: validate use of data structure
import solvers.solver_data


def solve_st(metric, model, model_instance, problem_instance, algorithm_structure):
    diag = {
        "disp": False,
        }
    return scipy.optimize.minimize( \
        fun=metric, \
        x0=algorithm_structure["initial_guesses"], \
        args=(model, model_instance, problem_instance), \
        method=algorithm_structure["method"],
        options = diag,
        bounds = problem_instance["bounds"])
