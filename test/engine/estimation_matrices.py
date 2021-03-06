
from __future__ import print_function

import unittest
import engine.estimation_matrices as testme

import numpy.matlib


class TestEstimationMatrices(unittest.TestCase):


    def test_prepare_sensitivity_matrix(self):
        sens_trajectories = numpy.asarray([[1], [0], [0], [0], \
                                           [0], [0], [0], [0], \
                                           [1], [1], [0], [0], \
                                           [1], [1], [0], [0], \
                                           [1], [0], [1], [1]])
        actual = testme.prepare_sensitivity_matrix(5, 4, 1, sens_trajectories)
        expected = numpy.asmatrix([[1, 0, 1, 1, 1], \
                                  [0, 0, 1, 1, 0], \
                                  [0, 0, 0, 0, 1], \
                                  [0, 0, 0, 0, 1]]).transpose()
        [self.assertEquals(act, exp) for act, exp in zip( \
            numpy.asarray(actual).flatten(), numpy.asarray(expected).flatten())] 
        

    def test_calculate_information_matrix_with_sens_identity(self):
        sens_matrix = numpy.matlib.eye(2)
        inf_matrix = testme.calculate_information_matrix(sens_matrix)
        [[self.assertEquals(i[ii],j[ii]) for ii in range(len(i))] \
            for i, j in zip(numpy.asarray(sens_matrix), numpy.asarray(inf_matrix))]


    def test_calculate_information_matrix_with_sens_all_ones(self):
        sens_matrix = numpy.matlib.ones((2,2))
        inf_matrix = testme.calculate_information_matrix(sens_matrix)
        [[self.assertEquals(i[ii],j[ii]) for ii in range(len(i))] \
            for i, j in zip(numpy.asarray(sens_matrix*2), numpy.asarray(inf_matrix))]


    # TODO: test singular
    # TODO: add more tests
    def test_calculate_covariance_matrix_with_sens_identity_times_two(self):
        sens_matrix = numpy.matlib.eye(2) * 2
        cov_matrix = testme.calculate_covariance_matrix(sens_matrix)
        [[self.assertEquals(i[ii],j[ii]) for ii in range(len(i))] \
            for i, j in zip(numpy.asarray(numpy.matlib.eye(2) / 4), numpy.asarray(cov_matrix))]



    def test_calculate_calculate_correlation_matrix(self):
        cov_matrix = numpy.eye(2, 2)
        corr_matrix = testme.calculate_correlation_matrix(cov_matrix)
        [self.assertEquals(act, exp) for act, exp in zip( \
            numpy.asarray(corr_matrix).flatten(), numpy.asarray(cov_matrix).flatten())] 
        
        cov_matrix = numpy.ones([2, 2])
        actual = testme.calculate_correlation_matrix(cov_matrix)
        expected = cov_matrix
        [self.assertEquals(act, exp) for act, exp in zip( \
            numpy.asarray(actual).flatten(), numpy.asarray(expected).flatten())] 

        cov_matrix = numpy.array([[1, 1], [1, 0.5]])
        actual = testme.calculate_correlation_matrix(cov_matrix)
        invsqrt = 1/numpy.sqrt(0.5)
        expected = numpy.array([[1, invsqrt], [invsqrt, 1]])
        [self.assertEquals(act, exp) for act, exp in zip( \
            numpy.asarray(actual).flatten(), numpy.asarray(expected).flatten())] 


if __name__ == "__main__":
    unittest.main()
