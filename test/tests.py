import unittest

# TODO:I don't know why import does not work directly
#import test.metrics.tests
from test.metrics.tests import *

if __name__ == '__main__':
    list_all = unittest.TestLoader().loadTestsFromTestCase(test_metrics)
    suite_all = unittest.TestSuite(list_all)
    unittest.TextTestRunner(verbosity=2).run(suite_all)
