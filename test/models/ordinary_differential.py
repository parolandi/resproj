
import unittest

import models.ordinary_differential

class TestOrdinaryDifferentialModels(unittest.TestCase):

    def test_linear_st(self):
        instance =dict( models.ordinary_differential.model_structure)
        instance["states"] = [1.0]
        instance["inputs"] = [1.0]
        instance["parameters"] = [1.0]
        instance["time"] = 0.0
        self.assertEquals(0.0, models.ordinary_differential.linear_st(instance["states"][0], instance["time"], instance))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()