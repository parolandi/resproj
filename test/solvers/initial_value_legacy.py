
import unittest
import numpy

import common.utilities
import solvers.initial_value_legacy


# states, time, parameters, inputs
def linear_mock(x, t, p, u):
    return p[0] * u[0]


class TestInitialValueLegacySolvers(unittest.TestCase):

    def test_solve_lsoda(self):
        times = numpy.arange(0.0, 1.0, 1.0 / 10)
        param = 1.0
        inputf = 1.0
        initc = 0.0
        result, stuff = solvers.initial_value_legacy.solve_lsoda(linear_mock, initc, times, [param], [inputf])
        actual = common.utilities.sliceit_assnapshot(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

    
    def test_compute_trajectory(self):
        times = numpy.arange(0.0, 1.0, 1.0 / 10)
        param = [1.0]
        inputf = [1.0]
        initc = [0.0]
        actual = solvers.initial_value_legacy.compute_trajectory(param, linear_mock, initc, inputf, times)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


if __name__ == "__main__":
    unittest.main()
