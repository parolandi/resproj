
import numpy.linalg


def compute_covariance_matrix(sensitivities, covariance_observation_errors):
    cov = 0
    if len(covariance_observation_errors.shape) == 0:
        cov = numpy.dot(numpy.transpose(sensitivities), sensitivities) / covariance_observation_errors
    else:
        inv_cov = numpy.linalg.inv(covariance_observation_errors)
        inv_cov_dot_sens = numpy.dot(inv_cov, sensitivities)
        cov = numpy.dot(numpy.transpose(sensitivities), inv_cov_dot_sens)
    return cov
    