
import common.diagnostics as cd
import models.model_data as mmd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr
import workflows.workflow_data_utils as wwdu

import copy


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
