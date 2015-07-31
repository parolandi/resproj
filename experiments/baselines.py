
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
