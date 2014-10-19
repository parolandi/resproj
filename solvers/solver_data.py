
import numpy

solver_settings = {
    "disp": None,
    "maxiter": None,
    "eps": None,
    "ftol": None,
    }


def prune_solver_settings(settings):
    pruned_settings = {}
    for k, v in settings.items():
        if v is not None:
            pruned_settings[k] = v
    return pruned_settings
    

algorithm_structure = {
    "callback": None,
    "initial_guesses": numpy.empty(1),
    "method": "",
    "tolerance": None,
    "solver_settings": None,
    }

# TODO: clone as nonlinear programming methods too
nonlinear_algebraic_methods = {
    "key-CG": 'CG',
    "key-hybr-suite-MINPACK-method-modified-Powell-ref-More-Garbow-Hillstrom-aff-ANL": 'hybr',
    "key-Nelder-Mead": 'Nelder-Mead',
    }

algorithmic_methods = {
    "nonlinear_algebraic": dict(nonlinear_algebraic_methods)
    }
