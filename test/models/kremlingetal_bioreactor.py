
import unittest
import models.kremlingetal_bioreactor as testme

import numpy


class TestKremlingEtAlBioreactor(unittest.TestCase):


    def test_zeros_and_ones(self):
        t = 0
        
        x = numpy.ones(len(testme.xvec))
        p = numpy.zeros(len(testme.pvec))
        u = numpy.zeros(len(testme.uvec_0h))
        actual = testme.evaluate_modelA(x, t, p, u)
        expected = numpy.zeros(len(x))
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = testme.evaluate_modelB(x, t, p, u)
        expected = numpy.zeros(len(x))
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]

        x = numpy.zeros(len(testme.xvec))
        x[testme.xmap["V"]] = 1.0
        p = numpy.ones(len(testme.pvec))
        u = numpy.ones(len(testme.uvec_0h))
        actual = testme.evaluate_modelA(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[testme.xmap["S"]] = 1.0
        expected[testme.xmap["E"]] = 1.0
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = testme.evaluate_modelB(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[testme.xmap["S"]] = 1.0
        expected[testme.xmap["E"]] = 1.0
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]

        x = numpy.ones(len(testme.xvec))
        p = numpy.ones(len(testme.pvec))
        u = numpy.zeros(len(testme.uvec_0h))
        actual = testme.evaluate_modelA(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[testme.xmap["X"]] = 0.5
        expected[testme.xmap["S"]] = -342.3 * 1E-6 / 2
        expected[testme.xmap["M1"]] = -0.25
        expected[testme.xmap["M2"]] = -0.75
        expected[testme.xmap["E"]] = 0.5
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = testme.evaluate_modelB(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[testme.xmap["X"]] = 0.5
        expected[testme.xmap["S"]] = -342.3 * 1E-6 / 2
        expected[testme.xmap["M1"]] = -0.5
        expected[testme.xmap["M2"]] = -0.5
        expected[testme.xmap["E"]] = 0.0
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]


if __name__ == "__main__":
    unittest.main()
