
from __future__ import print_function
import collections

import metrics.basic

least_squares_solver_info = {
        "status": "",
        "status_code": 0,
        "user_message": "",
        "objective_function": 0,
        "function_evaluations": 0,
        "jacobian_evaluations": 0,
    }

least_squares_solver_data = {
        "measuement_residuals": [],
        "approximate_jacobian": [],
    }

least_squares_detailed_results = {
        "parameter_estimates": [],
        "covariance_matrix": [],
        "solver_info": least_squares_solver_info,
        "solver_data": least_squares_solver_data,
    }

least_squares_basic_results = {
        "status": "",
        "parameter_estimates": [],
        "objective_function": 0,
    }

# basic
def print_basic(ls_result):
    print("------------------")
    print("Status: ", ls_result["status"])
    print("Estimate: ", ls_result["parameter_estimates"])
    print("Objective function: ", ls_result["objective_function"])
    print("------------------")
    
# detailed
def print_detailed(ls_result):
    print("------------------")
    print("Status: ", ls_result["status"])
    print("Estimate: ", ls_result["parameter_estimates"])
    print("Objective function: ", ls_result["solver_info"]["objective_function"])
    print("Number function calls: ", ls_result["solver_info"]["function_evaluations"])
    print("Number Jacobian calls: ", ls_result["solver_info"]["jacobian_evaluations"])
    print("User message: ", ls_result["solver_info"]["user_message"])
    print("------------------")

def to_friendly_string(code):
    if (code >= 0 and code <=4):
        return "successful"
    else:
        return "failure"

def print_least_squares_basic(estimates, info, err):
    ls_result = collections.defaultdict(dict)
    ls_result["status"] = to_friendly_string(err) 
    ls_result["parameter_estimates"] = estimates[0]
    ls_result["objective_function"] = metrics.basic.sum_absolute_value_residuals(info["fvec"])
    print_basic(ls_result)

def print_least_squares_detailed(estimates, cov, info, msg, err):
    ls_result = collections.defaultdict(dict)
    ls_result["status"] = to_friendly_string(err) 
    ls_result["parameter_estimates"] = estimates[0]
    ls_result["solver_info"]["objective_function"] = metrics.basic.sum_absolute_value_residuals(info["fvec"])
    ls_result["solver_info"]["function_evaluations"] = info["nfev"]
    ls_result["solver_info"]["user_message"] = msg
    if ls_result["solver_info"].has_key("nfev"):
        ls_result["solver_info"]["jacobian_evaluations"] = info["njev"]
    else:
        ls_result["solver_info"]["jacobian_evaluations"] = 0
    print_detailed(ls_result)
