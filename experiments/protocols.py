
import copy

import metrics.ordinary_differential as mod
import metrics.statistical_tests as mst
import models.model_data as mmd
import models.model_data_utils as mmdu
import solvers.least_squares
import workflows.workflow_data as wwd


'''
Do calibration
Compute performance measure
config: setups.setup_data.experiment_setup
return: models.model_data.optimisation_problem_solution, models.model_data.optimisation_problem_results
    the decision variable values
    the objective function value
'''
def do_calibration_and_compute_performance_measure(config):
    # setup
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    algorithm_instance = config["algorithm_setup"](None)

    # least-squares
    result = solvers.least_squares.solve(model_instance, problem_instance, algorithm_instance)

    # verification    
    # WIP: should this be needed?
    # need to do this here because problem data is kind of ignored
    problem_instance["parameters"] = copy.deepcopy(result.x)
    for ii in range(len(problem_instance["parameter_indices"])):
        model_instance["parameters"][problem_instance["parameter_indices"][ii]] = copy.deepcopy(result.x[ii])

    ssr_fit = problem_instance["performance_measure"](None, None, model_instance, problem_instance)

    solution = dict(mmd.optimisation_problem_solution)
    results = dict(mmd.optimisation_problem_results)
    solution["decision_variables"] = copy.deepcopy(problem_instance["parameters"])
    results["objective_function"] = ssr_fit
    return solution, results 


'''
Compute SSR, total and contributions
Compute residual trajectories, contributions
Compute chi-squared test, total and contributions
DO NOT...
Compute confidence intervals,
or sensitivities, covariance matrix, estimate standard deviation
and ellipsoid radius
config:
solution_point:
return: workflows.workflow_data.point_results
'''
# TODO: hard-coded stdev
def do_basic_workflow_at_solution_point(config, solution_point):
    assert(solution_point is not None)
    # TODO: preconditions!
    
    # TODO: hard-coded stdev
    stdev = 1.0

    # setup
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    protocol = config["protocol_setup"]()

    mmdu.apply_decision_variables_to_parameters(solution_point, model_instance, problem_instance)
    
    assert(problem_instance["performance_measure"] is protocol["performance_measure"])
    assert(problem_instance["performance_measure"] is mod.sum_squared_residuals_st)

    # objective function
    sum_sq_res = mod.sum_squared_residuals_st( \
        None, None, model_instance, problem_instance)

    # objective-function contributions
    sums_sq_res = mod.sums_squared_residuals( \
        None, None, model_instance, problem_instance)

    # observables' trajectories
    _ = solvers.initial_value.compute_timecourse_trajectories( \
        None, model_instance, problem_instance)
     
    # residuals' trajectories
    residuals_values = mod.residuals_st( \
        None, model_instance, problem_instance)

    # global ssr test
    dof = mst.calculate_degrees_of_freedom( \
        problem_instance["outputs"], problem_instance["parameter_indices"])
    ssr_test = mst.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
        sum_sq_res / stdev **2, dof, 0.95)
    
    # observables' ssr test
    ssr_tests = []
    for ii in range(len(problem_instance["outputs"])):
        dof = mst.calculate_degrees_of_freedom( \
            problem_instance["outputs"][ii], problem_instance["parameter_indices"])
        ssr_tests.append( \
            mst.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sums_sq_res[ii] / stdev **2, dof, 0.95))

    workflow_results = dict(wwd.point_results)
    workflow_results["ssr"] = sum_sq_res
    workflow_results["ssrs"] = sums_sq_res
    workflow_results["ress_vals"] = residuals_values
    workflow_results["ssr_test"] = ssr_test
    workflow_results["ssrs_tests"] = ssr_tests  

    return workflow_results
