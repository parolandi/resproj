
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
    baseline["decision_variables_eps"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
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


def set_baseline_point_0_60_yes10yes15no5(baseline):
    baseline["point"]["objective_function"] = 149.207796219
    baseline["point"]["decision_variables"] = numpy.array( \
        [  7.12884597e-05, 5.77667582e+06, 9.31968630e-03, 4.32751249e-02])
    return baseline


def set_baseline_eps_0_60_yes10yes15no5(baseline):
    baseline["of_delta"] = 0.000000001
    baseline["dv_deltas"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-02])
    baseline["decision_variables_eps"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-02])
    return baseline


def set_baseline_point_0_60_yes15no5yes10(baseline):
    baseline["point"]["objective_function"] = 169.703820093
    baseline["point"]["decision_variables"] = numpy.array( \
        [  7.22076277e-05, 6.00994312e+06, 1.11374646e-02, 2.03026444e-02])
    return baseline


def set_baseline_eps_0_60_yes15no5yes10(baseline):
    baseline["of_delta"] = 0.000000001
    baseline["dv_deltas"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
    baseline["decision_variables_eps"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
    return baseline

# --------------------------------------------------------------------------- #

def set_baseline_nonlinconfreg_0_60(baseline):
    baseline["number_of_points"] = 0
    # [[0, 0], [8, 0], [9, 8], [9, 9]]
    baseline["intervals"] = [ \
        [7.1815198110426653e-05, 7.2828378864918741e-05], \
        [5927979.0165858017, 5928271.2840146916], \
        [0.0012124961140420856, 0.12124961140420856], \
        [0.0017173506980212713, 0.1717350698021271]]
    return baseline

# --------------------------------------------------------------------------- #

def set_baseline_linconfreg_0_60(baseline):
    baseline["intervals"] = [ \
        [-3.6187550012739073e-06, 0.00014784764670326163], \
        [-24913161.381240699, 36769694.845824882], \
        [-0.082429882550159719, 0.10667980483100144], \
        [-0.19659946743068038, 0.23094648139110582]]
    baseline["ellipsoid"] = [ \
        [  1.81621236e-08, -3.17434040e+03,  3.60528005e-06, -3.73862376e-06], \
        [ -3.17434040e+03,  3.01205545e+15, -5.49626381e+06, -6.51653101e+04], \
        [  3.60528005e-06, -5.49626381e+06,  2.83114142e-02, -4.97156180e-02], \
        [ -3.73862376e-06, -6.51653101e+04, -4.97156180e-02,  1.44710353e-01]]
    baseline["delta"] = [ \
        [  0.00000001e-08,  0.00000001e+03,  0.00000001e-06,  0.00000001e-06], \
        [  0.00000001e+03,  0.00000001e+15,  0.00000001e+06,  0.00000001e+04], \
        [  0.00000001e-06,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02], \
        [  0.00000001e-06,  0.00000001e+04,  0.00000001e-02,  0.00000001e-01]]
    return baseline
