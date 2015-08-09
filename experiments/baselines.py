
import numpy


def set_baseline_point(baseline):
    baseline["decision_variables"] = numpy.array([7.06036656e-05, 5.95280934e+06, 7.86546429e-03, 5.61758623e-01])
    baseline["objective_function"] = 55.73031631952742
    return baseline


def set_baseline_eps(baseline):
    baseline["decision_variables_eps"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01])
    baseline["dv_deltas"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01])
    baseline["of_delta"] = 0.000000000001
    return baseline


def set_baseline_point_0_60(baseline):
    baseline["point"]["objective_function"] = 191.9159661
    baseline["point"]["decision_variables"] = numpy.array( \
        [  7.21144459e-05,  5.92826673e+06,  1.21249611e-02,  1.71735070e-02])
    return baseline


def set_baseline_eps_0_60(baseline):
    baseline["of_delta"] = 0.0000001
    baseline["dv_deltas"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
    baseline["decision_variables_eps"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
    return baseline
    
    
def set_baseline_point_0_60_yesnoyes(baseline):
    baseline["point"]["objective_function"] = 153.05359591605975
    baseline["point"]["decision_variables"] = numpy.array( \
        [  7.25907845138e-05, 5906545.40918, 0.0129296870173, 0.0144696117475])
    return baseline


def set_baseline_eps_0_60_yesnoyes(baseline):
    baseline["of_delta"] = 0.000000001
    baseline["dv_deltas"] = numpy.array( \
        [0.00000001e-05, 0.00000001e+06, 0.00000001e-02, 0.00000001e-02])
    return baseline


def get_baseline_point_0_60_yesnoyes():
    return 40.78092219391061


def set_baseline_point_0_60_yesnoyes_global(baseline):
    baseline["point"]["objective_function"] = 153.05363120711212
    baseline["point"]["decision_variables"] = numpy.array( \
        [7.25862257e-05, 5.90781801e+06, 1.29356451e-02, 1.44543579e-02])
    return baseline


def get_baseline_point_0_60_yesnoyes_global():
    return 40.76668320905531