
import unittest
import models.kremlingetal_bioreactor as mk

import numpy


class TestKremlingEtAlBioreactor(unittest.TestCase):


    def test_zeros_and_ones(self):
        t = 0
        
        x = numpy.ones(len(mk.xvec))
        p = numpy.zeros(len(mk.pvec))
        u = numpy.zeros(len(mk.uvec_0h))
        actual = mk.evaluate_modelA(x, t, p, u)
        expected = numpy.zeros(len(x))
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = mk.evaluate_modelB(x, t, p, u)
        expected = numpy.zeros(len(x))
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]

        x = numpy.zeros(len(mk.xvec))
        x[mk.xmap["V"]] = 1.0
        p = numpy.ones(len(mk.pvec))
        u = numpy.ones(len(mk.uvec_0h))
        actual = mk.evaluate_modelA(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[mk.xmap["S"]] = 1.0
        expected[mk.xmap["E"]] = 1.0
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = mk.evaluate_modelB(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[mk.xmap["S"]] = 1.0
        expected[mk.xmap["E"]] = 1.0
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]

        x = numpy.ones(len(mk.xvec))
        p = numpy.ones(len(mk.pvec))
        u = numpy.zeros(len(mk.uvec_0h))
        actual = mk.evaluate_modelA(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[mk.xmap["X"]] = 0.5
        expected[mk.xmap["S"]] = -342.3 * 1E-6 / 2
        expected[mk.xmap["M1"]] = -0.25
        expected[mk.xmap["M2"]] = -0.75
        expected[mk.xmap["E"]] = 0.5
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = mk.evaluate_modelB(x, t, p, u)
        expected = numpy.zeros(len(x))
        expected[mk.xmap["X"]] = 0.5
        expected[mk.xmap["S"]] = -342.3 * 1E-6 / 2
        expected[mk.xmap["M1"]] = -0.5
        expected[mk.xmap["M2"]] = -0.5
        expected[mk.xmap["E"]] = 0.0
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]

    
if __name__ == "__main__":
    unittest.main()
