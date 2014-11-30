
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
    "est_stdev": 0.0,
    "ell_radius": 0.0,
    "conf_intvs": [],
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