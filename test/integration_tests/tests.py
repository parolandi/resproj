
import unittest

# TODO:I don't know why import does not work directly
from test.integration_tests.algebraic_linear import *
from test.integration_tests.epo_receptor import *
from test.integration_tests.kremlingetal_bioreactor import *
from test.integration_tests.ordinary_differential import *


if __name__ == '__main__':
    list_all = unittest.TestLoader().loadTestsFromTestCase()
    suite_all = unittest.TestSuite(list_all)
    unittest.TextTestRunner(verbosity=2).run(suite_all)
