
from __future__ import print_function
import logging
import time


def get_return_on_quick_tests_only():
    return "doing quick tests only!"


def print_and_log_return_on_quick_tests_only():
    print("Warning: " + get_return_on_quick_tests_only())
    logging.warn(get_return_on_quick_tests_only())
    

def get_date_and_time():
    return time.strftime("%Y/%m/%d") + "@" + time.strftime("%H:%M:%S")


def get_name_logging_file():
    return "/Users/mamuts/code/resproj/app.log"


def get_logging_level():
    return logging.INFO
    

def get_debugging_level():
    return logging.DEBUG


def legacy_code_message():
    return "Warning: this is a legacy code path"


def print_legacy_code_message():
    print(legacy_code_message())


def unexpected_code_branch_message():
    return "Warning: this is an unexpected code branch path"
    

def print_unexpected_code_branch_message():
    msg = unexpected_code_branch_message()
    print(msg)
    logging.warn(msg)


def wall_time_message():
    return "Wall time:"
    

def print_wall_time_message(value):
    print(wall_time_message(), value)
    
    
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


def print_measurements_est_var_and_ellipsoid_radius(meas, est_var, ellrad):
    print("no measurements:", meas)
    print("estimated variance:", est_var)
    print("ellipsoid radius:", ellrad)


def print_covariance_matrix_and_determinant(cov_matrix, det):
    print("covariance matrix:", cov_matrix)
    print("covariance matrix's determinant:", det)


def warning_error_code_message():
    return "Warning/Error: there is something wrong!"


def print_warning_error_code_message():
    print(warning_error_code_message())


def print_ellipsoid(it):
    print("ellipsoid", it)
    
    
def write_info(data):
    f = open('/Users/mamuts/code/resproj/diag.txt', 'a')
    f.write(str(data) + "\n")