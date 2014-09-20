
#return sum_sq_res, sums_sq_res, residuals_values, ssr_test, ssr_tests, \
#    cov_matrix, est_stdev, ell_radius, confidence_intervals
point_results = {
    "ssr": 0.0,
    "ssrs": [],
    "ress_vals": [],
    "ssr_test": False,
    "ssrs_tests": [],
    "cov_matrix": None,
    "est_stdev": 0.0,
    "ell_radius": 0.0,
    "conf_intvs": [],
    }


algorithmic_statistics = {
    "iters": 0,
    }


workflow_data = {
    "params": [],
    "obj": [],
    "obj_contribs": [],
    "ssr": [],
    "ssr_contribs": [],
    "conf_intervs": [],
    "algo_stats": dict(algorithmic_statistics),
    }


workflow_results = {
    "full": dict(workflow_data),
    "calibration": dict(workflow_data),
    "validation": dict(workflow_data),
    "calib+valid": dict(workflow_data), 
    }

# TODO: there is something wrong with the use of these datastructures