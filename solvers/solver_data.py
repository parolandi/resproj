
import numpy

algorithm_structure = {
    "callback": None,
    "initial_guesses": numpy.empty(1),
    "method": "",
    "tolerance": None,
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
