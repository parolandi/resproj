
import unittest

# TODO:I don't know why import does not work directly
from test.common.utilities import *
from test.data.data_splicing import *
from test.data.generator import *
from test.engine.estimation_matrices import *
from test.engine.statistical_inference import *
from test.metrics.algebraic_legacy import *
from test.metrics.algebraic import *
from test.metrics.confidence_measures import *
from test.metrics.ordinary_differential import *
from test.metrics.statistical_tests import *
from test.models.algebraic import *
from test.models.model_data_utils import *
from test.models.ordinary_differential import *
#from test.results.plot_tiles import *
from test.solvers.initial_value_legacy import *
from test.solvers.initial_value import *
from test.solvers.least_squares_algebraic import *
from test.solvers.least_squares_legacy import *
from test.solvers.least_squares import *
from test.solvers.local_sensitivities import *
from test.solvers.monte_carlo_multiple_initial_value import *
from test.solvers.monte_carlo_multiple_least_squares import *
from test.solvers.monte_carlo_sampling import *
from test.solvers.nonlinear_algebraic import *
from test.solvers.solver_data import *


if __name__ == '__main__':
    list_all = unittest.TestLoader().loadTestsFromTestCase()
    suite_all = unittest.TestSuite(list_all)
    unittest.TextTestRunner(verbosity=2).run(suite_all)
