
import common.diagnostics as cd
import models.model_data as mmd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr
import workflows.workflow_data_utils as wwdu

import copy
import logging
import numpy
import time

import engine.confidence_regions as encore
import engine.diagnostics as endi
import results.plot_combinatorial as replco
import solvers.monte_carlo_multiple_initial_value as mcmiv


baseline = {
    "point": dict(mmd.optimisation_problem_point),
    "of_delta": 0.0,
    "dv_deltas" : [],
    }


calib_valid_baseline = {
    "calib": copy.deepcopy(baseline),
    "valid": copy.deepcopy(baseline),
    }


# self.do_experiment_setup
def test_baseline_calibration(setup, baseline, unittester):
    """
    baseline can be None
    """
    config = setup()
    calibrated = wpr.do_calibration_and_compute_performance_measure(config)
    # output
    if True:
        cd.print_decision_variables_and_objective_function(calibrated)
        post_proc = wpr.do_basic_workflow_at_solution_point(config, calibrated)
        wwdu.print_system_based_point_results(post_proc)
        post_proc = wpr.do_sensitivity_based_workflow_at_solution_point(config, calibrated)
        wwdu.print_sensitivity_based_point_results(post_proc)
    # test
    if baseline is not None:
        actual = calibrated["objective_function"]
        expected = baseline["point"]["objective_function"]
        unittester.assertAlmostEquals(actual, expected, delta=baseline["of_delta"])
        # test
        actual = calibrated["decision_variables"]
        expected = baseline["point"]["decision_variables"]
        deltas = baseline["dv_deltas"]
        [unittester.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
    else:
        cd.print_unexpected_code_branch_message()
    return calibrated


# self.do_experiment_setup
def test_baseline_validation(setup, baseline, unittester, point):
    """
    baseline can be None
    """
    config = setup()
    # TODO: should probably be returning here if there is no validation to perform
    # e.g., in order to plot calib and valid
    ssdu.set_next_protocol_step(config)
    validated = wpr.do_validation_and_compute_performance_measure_at_solution_point(config, point)
    # output
    if True:
        cd.print_decision_variables_and_objective_function(validated)
        post_proc = wpr.do_basic_workflow_at_solution_point(config, validated)
        wwdu.print_system_based_point_results(post_proc)
        post_proc = wpr.do_sensitivity_based_workflow_at_solution_point(config, validated)
        wwdu.print_sensitivity_based_point_results(post_proc)
    # test
    if baseline is not None:
        actual = validated["objective_function"]
        expected = baseline["point"]["objective_function"]
        unittester.assertAlmostEquals(actual, expected, delta=baseline["of_delta"])
        # test
        actual = validated["decision_variables"]
        expected = baseline["point"]["decision_variables"]
        deltas = baseline["dv_deltas"]
        [unittester.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
    else:
        cd.print_unexpected_code_branch_message()
    return validated


def test_baseline_calibration_and_validation(setup, baseline, unittester):
    # there is no good reason why this should be different
    refpoint = baseline["calib"]
    basepoint = baseline["valid"]
    basepoint["point"]["decision_variables"] = refpoint["point"]["decision_variables"]
    basepoint["of_delta"] = refpoint["of_delta"]
    basepoint["dv_deltas"] = refpoint["dv_deltas"]

    calibrated = test_baseline_calibration(setup, baseline["calib"], unittester)
    test_baseline_validation(setup, baseline["valid"], unittester, calibrated)
    return calibrated


# TODO: extract to protocol
def test_calibration_with_nonlinear_confidence_region(config, baseline, unittester):
    """
    config setup_data.experiment_setup
    """
    best_point = wpr.do_calibration_and_compute_performance_measure(config)

    # setup
    algorithm = config["algorithm_setup"](None)
    model = config["model_setup"]()
    data = config["data_setup"]()
    problem  = config["problem_setup"](model, data["calib"])
    # TODO: hard coded
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 120000*4
    if True:
        algorithm_mc["number_of_trials"] = 100
    # TODO: hard coded
    if True:
        do_appy_bounds(best_point["decision_variables"], problem)
    
    logging.info(problem["bounds"])
    
    # do nonlin conf reg
    wall_time0 = time.time()
    actual_intervals, actual_points = encore.compute_nonlinear_confidence_region_intervals_and_points_extremal( \
        model, problem, algorithm, algorithm_mc, best_point)
    wall_time = time.time() - wall_time0
    number_of_points = len(numpy.transpose(actual_points["objective_function"]))
    logging.info(endi.log_points(actual_points))
    logging.info(endi.log_wall_time(wall_time))
    logging.info(endi.log_number_of_trials(algorithm_mc["number_of_trials"]))
    logging.info(endi.log_number_of_points(number_of_points))
    unittester.assertEquals(number_of_points, baseline["number_of_points"])
    expected = baseline["intervals"]
    [unittester.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
        numpy.asarray(actual_intervals).flatten(), numpy.asarray(expected).flatten())]
    
    # plot nonlin conf reg
    if True:
        replco.plot_combinatorial_region_projections(numpy.transpose(actual_points["decision_variables"]))


def do_appy_bounds(nominal, problem):
    lf = 1E-2
    uf = 1E+2
    problem["bounds"] = [ \
        (nominal[0]*lf,nominal[0]*uf), \
        (nominal[1]*lf,nominal[1]*uf), \
        (nominal[2]*lf,nominal[2]*uf), \
        (nominal[3]*lf,nominal[3]*uf)]
