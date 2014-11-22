
import unittest

# TODO:I don't know why import does not work directly
from experiments.experiment_01 import *
from experiments.experiment_02 import *
from experiments.experiment_03 import *
from experiments.experiment_04 import *

import experiments.experiment as ee


if __name__ == '__main__':
    ee.set_showing_plots(False)

    list_all = unittest.TestLoader().loadTestsFromTestCase()
    suite_all = unittest.TestSuite(list_all)
    unittest.TextTestRunner(verbosity=2).run(suite_all)
