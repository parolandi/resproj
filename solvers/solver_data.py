
import numpy

algorithm_structure = {
    "callback": None,
    "initial_guesses": numpy.empty(1),
    "method": "",
    "tolerance": 0.0,
    }

nonlinear_algebraic_methods = {
    "key-hybr-suite-MINPACK-method-modified-Powell-ref-More-Garbow-Hillstrom-aff-ANL": 'hybr'
    }

algorithmic_methods = {
    "nonlinear_algebraic": dict(nonlinear_algebraic_methods)
    }
