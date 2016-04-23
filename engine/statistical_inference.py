
import math
import numpy
import scipy.stats


def compute_confidence_ellipsoid_radius(no_params, no_meas, est_var, significance):
    """
    Compute the confidence ellipsoid radius for the following assumptions:
    TODO:
    no_params: number of parameters estimated
    no_meas: number of measurement points
    est_var: estimated variance (e.g., S/(n-p)=R^2/(n-p))
    significance: confidence level (e.g., 0.95 for 95%)
    """
    assert(no_params > 0)
    assert(no_meas > 0)
    assert(no_meas > no_params)
    assert(est_var > 0)
    assert(significance > 0 and significance < 1)
    
    f_value = compute_one_sided_f_value(significance, no_meas, no_params)
    radius = est_var * no_params * f_value

    # TODO: change to settings
    user_messages = False
    if user_messages:
        print("est-var: ", est_var)
        print("f-value: ", f_value)
        print("radius:", radius)

    return radius


# TODO: documentation
def compute_measurements_variance(ssr, no_params, no_meas):
    assert (no_meas > no_params)
    
    est_var = ssr / (no_meas - no_params)
    user_messages = False
    if user_messages:
        print("ssr", ssr)
        print("est-var", est_var)
    
    return est_var


# TODO: documentation
def compute_confidence_intervals(covariance_matrix, t_value):
    assert(t_value > 0)
    assert(len(covariance_matrix) > 0)
    
    no_params = len(covariance_matrix)
    confidence_intervals = numpy.zeros(no_params)
    for ii in range(no_params):
        confidence_intervals[ii] = t_value * math.sqrt(covariance_matrix[ii, ii])
    return confidence_intervals


def compute_one_sided_f_value(significance, no_meas, no_params):
    assert(no_meas > 0 and no_params > 0)
    assert(no_meas > no_params)
    
    q = 1 - significance
    f_value = scipy.stats.f.isf(q, no_params, no_meas - no_params)
    return f_value
