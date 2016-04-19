

import unittest

# TODO:I don't know why import does not work directly
from experiments.experiment_01 import *
from experiments.experiment_02 import *
from experiments.experiment_03 import *
from experiments.experiment_04 import *
from experiments.experiment_05 import *
from experiments.experiment_06 import *
from experiments.experiment_07 import *
from experiments.experiment_08 import *
from experiments.experiment_09 import *
from experiments.experiment_10 import *
from experiments.experiment_11 import *
#from experiments.experiment_12 import *
#from experiments.experiment_13 import *
from experiments.experiment_14 import *
from experiments.experiment_15 import *
from experiments.experiment_16 import *
from experiments.experiment_17 import *
from experiments.experiment_18 import *
from experiments.experiment_19 import *
from experiments.experiment_20 import *
from experiments.experiment_21 import *
from experiments.experiment_22 import *
#from experiments.experiment_23 import *
#from experiments.experiment_24 import *

import experiments.experiment as ee


if __name__ == '__main__':
    ee.set_showing_plots(False)

    list_all = unittest.TestLoader().loadTestsFromTestCase()
    suite_all = unittest.TestSuite(list_all)
    unittest.TextTestRunner(verbosity=2).run(suite_all)
