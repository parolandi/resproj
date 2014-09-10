
from __future__ import print_function

import unittest
import engine.estimation_matrices

import numpy.matlib


class TestEstimationMatrices(unittest.TestCase):


    def test_calculate_information_matrix(self):
        sens_matrix = numpy.matlib.eye(2)
        inf_matrix = engine.estimation_matrices.calculate_information_matrix(sens_matrix)
        [[self.assertEquals(i[ii],j[ii]) for ii in range(len(i))] \
            for i, j in zip(numpy.asarray(sens_matrix), numpy.asarray(inf_matrix))]

        sens_matrix = numpy.matlib.ones((2,2))
        inf_matrix = engine.estimation_matrices.calculate_information_matrix(sens_matrix)
        [[self.assertEquals(i[ii],j[ii]) for ii in range(len(i))] \
            for i, j in zip(numpy.asarray(sens_matrix*2), numpy.asarray(inf_matrix))]


    # TODO: test singular
    # TODO: add more tests
    def test_calculate_covariance_matrix(self):
        sens_matrix = numpy.matlib.eye(2) * 2
        cov_matrix = engine.estimation_matrices.calculate_covariance_matrix(sens_matrix)
        [[self.assertEquals(i[ii],j[ii]) for ii in range(len(i))] \
            for i, j in zip(numpy.asarray(numpy.matlib.eye(2) / 4), numpy.asarray(cov_matrix))]


if __name__ == "__main__":
    unittest.main()
