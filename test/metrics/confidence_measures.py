
from __future__ import print_function
import unittest
import numpy

import metrics.confidence_measures


# TODO: test singular matrix
class TestConfidenceMeasures(unittest.TestCase):


    def test_compute_covariance_matrix_1s1p(self):
        err = numpy.array([1.5])
        cov_obs_err = numpy.dot(err, numpy.transpose(err))
        sens = numpy.array([[2]])
        actual = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_err)
        expected = 2*2/2.25
        self.assertEqual(actual, expected)

    
    def test_compute_covariance_matrix_1s2p(self):
        err = numpy.array([1, 0.5])
        cov_obs_err = numpy.dot(err, numpy.transpose(err))
        sens = numpy.array([[1], [2]])
        actual = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_err)
        expected = (1*1+2*2)/1.25
        self.assertEqual(actual, expected)


    def test_compute_covariance_matrix_2s1p(self):
        err = numpy.array([[1, 0.0], [0.0, 0.5]])
        cov_obs_err = numpy.dot(err, numpy.transpose(err))
        sens = numpy.array([[1], [0.5]])
        actual = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_err)
        icv_dot_s = [1*1+0*0.5, 0*1+4*0.5]
        st_dot_icv_dot_s = 1*icv_dot_s[0]+0.5*icv_dot_s[1]
        expected = numpy.asarray(numpy.transpose(st_dot_icv_dot_s)) 
        self.assertEqual(actual, expected)

    
    def test_compute_covariance_matrix_2s2p(self):
        err = numpy.array([[1, 0.0], [0.0, 0.5]])
        cov_obs_err = numpy.dot(err, numpy.transpose(err))
        sens = numpy.array([[1, 0.5], [0.5, 0.25]])
        actual = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_err)
        icv_dot_s = [[1*1+0*0.5, 0*1+4*0.5],[1*0.5+0*0.25, 0*0.5+4*0.25]]
        st_dot_icv_dot_s = [[1*icv_dot_s[0][0]+0.5*icv_dot_s[0][1], 0.5*icv_dot_s[0][0]+0.25*icv_dot_s[0][1]], [1*icv_dot_s[1][0]+0.5*icv_dot_s[1][1], 0.5*icv_dot_s[1][0]+0.25*icv_dot_s[1][1]]]
        expected = numpy.asarray(numpy.transpose(st_dot_icv_dot_s)) 
        [[self.assertEqual(act, exp) for act, exp in zip(acts, exps)] for acts, exps in zip(actual, expected)]


    # TODO: test non-diag

if __name__ == "__main__":
    unittest.main()
