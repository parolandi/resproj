
import models.model_data as mmd
import workflows.protocols as wpr

import common.diagnostics as cd


baseline = {
    "point": dict(mmd.optimisation_problem_point),
    "of_delta": 0.0,
    "dv_deltas" : [],
    }


# self.do_experiment_setup
def test_baseline_calibration(setup, baseline, unittester):
    config = setup()
    calibrated = wpr.do_calibration_and_compute_performance_measure(config)
    # test
    actual = calibrated["objective_function"]
    expected = baseline["point"]["objective_function"]
    unittester.assertAlmostEquals(actual, expected, delta=baseline["of_delta"])
    # test
    actual = calibrated["decision_variables"]
    expected = baseline["point"]["decision_variables"]
    deltas = baseline["dv_deltas"]
    [unittester.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
    # output
    if False:
        cd.print_decision_variables_and_objective_function(calibrated)
