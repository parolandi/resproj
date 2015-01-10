
from __future__ import print_function


def legacy_code_message():
    return "Warning: this is a legacy code path"


def print_legacy_code_message():
    print(legacy_code_message())


def print_decision_variables_and_confidence_intervals(dvs, cis):
    print("decision variables:", dvs)
    print("confidence intervals:", cis)


'''
point: models.model_data.optimisation_problem_point
'''
def print_decision_variables_and_objective_function(point):
    print("decision variables:", point["decision_variables"])
    print("objective function:", point["objective_function"])


def print_maximum_sensitivities(max_sens):
    print("maximum absolute sensitivities:", max_sens)


def print_observations_parameters_and_timeponts(obs, pars, pnts):
    print("no observations:", obs)
    print("no parameters:", pars)
    print("no timepoints:", pnts)


def print_measurements_stdev_and_ellipsoid_radius(meas, stdev, ellrad):
    print("no measurements:", meas)
    print("standard deviation:", stdev)
    print("ellipsoid radius:", ellrad)


def print_covariance_matrix_and_determinant(cov_matrix, det):
    print("covariance matrix:", cov_matrix)
    print("covariance matrix's determinant:", det)
