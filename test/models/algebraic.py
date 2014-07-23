
import unittest
import numpy

import models.algebraic

class TestModelsAlgebraic(unittest.TestCase):


    def test_linear_2p2s(self):
        p = numpy.array([2.0, 4.0])
        # three realisations
        x = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])
        y = numpy.empty(x.shape)
        series = 0
        for ii in range(x.shape[series]):
            y[ii] = models.algebraic.linear_2p2s(p, x.take(ii, axis=series))
        actual = y
        expected = numpy.array([[2.0, 40], [4.0, 80], [6.0, 120]])
        # TODO: pythonic; list comprehension
        for ii in range(y.shape[series]):
            for jj in range(y.shape[series+1]):
                self.assertEquals(actual[ii, jj], expected[ii, jj])


if __name__ == "__main__":
    unittest.main()
