
import unittest

# TODO:I don't know why import does not work directly
#import test.metrics.ordinary_differential
from test.common.utilities import *
from test.metrics.algebraic import *
from test.metrics.ordinary_differential import *
from test.models.ordinary_differential import *
from test.solvers.initial_value import *
from test.solvers.initial_value_legacy import *
from test.solvers.nonlinear_algebraic import *
from test.solvers.least_squares import *
from test.solvers.least_squares_algebraic import *

if __name__ == '__main__':
    list_all = unittest.TestLoader().loadTestsFromTestCase()
    suite_all = unittest.TestSuite(list_all)
    unittest.TextTestRunner(verbosity=2).run(suite_all)
