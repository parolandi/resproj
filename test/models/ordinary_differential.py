
import unittest

import numpy

import models.ordinary_differential

class TestOrdinaryDifferentialModels(unittest.TestCase):

    def test_linear_st(self):
        instance = dict(models.ordinary_differential.model_structure)
        instance["states"] = [1.0]
        instance["inputs"] = [1.0]
        instance["parameters"] = [1.0]
        instance["time"] = 0.0
        self.assertEquals(0.0, models.ordinary_differential.linear_st(instance["states"][0], instance["time"], instance))


    def test_epo_receptor(self):
        params = {
            "k_on": 0.00010496,
            "k_off": 0.0172135,
            "k_t": 0.0329366,
            "k_e": 0.0748267,
            "k_ex": 0.00993805,
            "k_di": 0.00317871,
            "k_de": 0.0164042,
        }
        states = {
            "Epo": 0.0,
            "EpoR": 0.0,
            "Epo_EpoR": 0.0,
            "Epo_EpoR_i": 0.0,
            "dEpo_i": 0.0,
            "dEpo_e": 0.0,
        }
        inputs = {
            "B_max": 0.0,
        }
        time = 0.0
        actual = models.ordinary_differential.epo_receptor(states, time, params, inputs)
        expected = numpy.zeros(6)
        [self.assertEquals(act, exp) for act, exp in zip(actual, expected)]

if __name__ == "__main__":
    unittest.main()
