
import scipy.stats
import numpy


'''
Compute the confidence ellipsoid for the following assumptions:
TODO:
no_params: number of parameters estimated
no_meas: number of measurement points
est_stdev: estimated standard deviation (e.g., R/(n-p))
significance: confidence level (e.g., 0.95 for 95%)
'''
def compute_confidence_ellipsoid_radius(no_params, no_meas, est_stdev, significance):
    assert(no_params > 0)
    assert(no_meas > 0)
    assert(no_meas > no_params)
    assert(est_stdev > 0)
    assert(significance > 0 and significance < 1)
    
    q = 1 - significance
    f_value = scipy.stats.f.isf(q, no_params, no_meas - no_params)
    radius = no_params * est_stdev **2 * f_value

    user_messages = False
    if user_messages:
        print("est-stdev: ", est_stdev)
        print("f-value: ", f_value)

    return radius

# TODO: documentation
def compute_measurements_standard_deviation(ssr, no_params, no_meas):
    return ssr / (no_meas - no_params)


# TODO: documentation
def compute_confidence_intervals(covariance_matrix, ellipsoid_radius):
    assert(isinstance(ellipsoid_radius, float))
    assert(len(covariance_matrix) > 0)
    
    no_params = len(covariance_matrix)
    confidence_intervals = numpy.zeros(no_params)
    for ii in range(no_params):
        confidence_intervals[ii] = ellipsoid_radius * covariance_matrix[ii, ii]
    return confidence_intervals
