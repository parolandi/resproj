
import unittest
import solvers.monte_carlo_sampling as testme

import numpy


class TestMonteCarloSampling(unittest.TestCase):


    def test_draw_samples(self):
        dv_count = 3
        dv_ranges = numpy.asarray([[0,1], [0,1], [-1,1]])
        trials_count = 10
        seed = 117
        actuals = testme.draw_samples(dv_count, dv_ranges, trials_count, seed)
        expected = [[0.45141113, 0.67584966, -0.94521223], [0.14074832, 0.58374409, 0.460753]]
        [self.assertAlmostEqual(act, dep, 8) for act, dep in zip(actuals[:,0].flatten(), expected[0])]
        [self.assertAlmostEqual(act, dep, 8) for act, dep in zip(actuals[:,-1].flatten(), expected[-1])]


if __name__ == "__main__":
    unittest.main()