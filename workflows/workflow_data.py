
import copy


# TODO: document
point_results = {
    "params": [],
    "ssr": 0.0,
    "ssrs": [],
    "ress_vals": [],
    "ssr_test": False,
    "ssrs_tests": [],
    "cov_matrix": None,
    "est_var": 0.0,
    "ell_radius": 0.0,
    "conf_intvs": [],
    }

'''
Values of sum-squared-residuals, overall and contributions
Values of chi-squared test, overall and contributions
Full set of residual values
To compute these values the system itself should only be required
'''
system_based_point_results = {
    "params": [],
    "ssr": [], # float
    "ssrs": [],
    "ress_vals": [],
    "ssr_test": [], # boolean
    "ssrs_tests": [],
    "ssr_thresh_lb": 0.0,
    "ssr_thresh_ub": 0.0,
    "ssrs_thresh_lb": [],
    "ssrs_thresh_ub": [],
    }


'''
The covariance matrix and the confidence intervals
Also the estimated standard deviation and the ellipsoid radius
To compute these values the system and sensitivities should both be required
'''
sensitivity_based_point_results = {
    "params": [], # numpy.array
    "cov_matrix": [], # numpy.matrix
    "cov_det": 0.0,
    "est_var": [], # float
    "ell_radius": [], # float
    "conf_intvs": [],
    "corr_matrix": [], # numpy.matrix
    "corr_det": 0.0,
    }


# TODO: document
algorithmic_statistics = {
    "iters": 0,
    }


# TODO: document
workflow_data = {
    "params": [],
    "obj": [],
    "obj_contribs": [],
    "ssr": [],
    "ssr_contribs": [],
    "conf_intervs": [],
    "algo_stats": dict(algorithmic_statistics),
    }


# TODO: document
workflow_results = {
    "full": copy.deepcopy(workflow_data),
    "calibration": copy.deepcopy(workflow_data),
    "validation": copy.deepcopy(workflow_data),
    "calib+valid": copy.deepcopy(workflow_data), 
    }


# TODO: add unit-tests
# e.g., dict vs copy.deepcopy