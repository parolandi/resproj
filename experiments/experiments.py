
import copy
import numpy

import metrics.ordinary_differential as mod
import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr


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
