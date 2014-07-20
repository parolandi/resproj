
import unittest

import numpy

import models.model_data
import models.ordinary_differential

class TestOrdinaryDifferentialModels(unittest.TestCase):

    def test_linear_st(self):
        instance = dict(models.model_data.model_structure)
        instance["states"] = [1.0]
        instance["inputs"] = [1.0]
        instance["parameters"] = [1.0]
        instance["time"] = 0.0
        solution = models.ordinary_differential.linear_st(instance["states"][0], instance["time"], instance)
        self.assertEquals(0.0, solution)


    def test_epo_receptor_di_null(self):
        params = models.ordinary_differential.epo_receptor_default_parameters
        states = models.ordinary_differential.epo_receptor_states
        inputs = models.ordinary_differential.epo_receptor_default_inputs
        inputs["B_max"] = 0.0
        time = 0.0
        actual = models.ordinary_differential.epo_receptor_di(states, time, params, inputs)
        expected = numpy.zeros(6)
        [self.assertEquals(act, exp) for act, exp in zip(actual, expected)]


    # TODO: disable because it gives different result depending on whether it is executed alone
    # or as part of the overall test suite
    def test_epo_receptor_null(self):
        params = numpy.ones(len(models.ordinary_differential.params_i))
        for par in models.ordinary_differential.params_i.items():
            params[par[1]] = models.ordinary_differential.epo_receptor_default_parameters[par[0]]
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.asarray(params)
        model_instance["states"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        model_instance["inputs"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_default_inputs))
        actual = models.ordinary_differential.epo_receptor(model_instance["states"], 0.0, model_instance["parameters"], model_instance["inputs"])
        expected = numpy.zeros(len(model_instance["states"]))
        [self.assertEquals(act, exp) for act, exp in zip(actual, expected)]

    
if __name__ == "__main__":
    unittest.main()
