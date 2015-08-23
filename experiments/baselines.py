
import numpy

# Calibration and validation only
# --------------------------------------------------------------------------- #
# Semi-legacy

def set_baseline_point(baseline):
    baseline["decision_variables"] = numpy.array([7.06036656e-05, 5.95280934e+06, 7.86546429e-03, 5.61758623e-01])
    baseline["objective_function"] = 55.73031631952742
    return baseline


def set_baseline_eps(baseline):
    baseline["decision_variables_eps"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01])
    baseline["dv_deltas"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01])
    baseline["of_delta"] = 0.000000000001
    return baseline


# --------------------------------------------------------------------------- #
# 0-20 hr

def set_baseline_point_0_20(baseline):
    baseline["point"]["decision_variables"] = numpy.array([7.06036656e-05, 5.95280934e+06, 7.86546429e-03, 5.61758623e-01])
    baseline["point"]["objective_function"] = 55.73031631952742
    return baseline


def set_baseline_eps_0_20(baseline):
    return set_baseline_eps(baseline)


# --------------------------------------------------------------------------- #
# 0-60 hr

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


# --------------------------------------------------------------------------- #
# Yes-no-yes 0-60 hr

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

# --------------------------------------------------------------------------- #
# Yes-yes-no 0-60 hr

def set_baseline_point_0_60_yesyesno(baseline):
    baseline["point"]["objective_function"] = 91.42486076854522
    baseline["point"]["decision_variables"] = numpy.array( \
        [  7.09002587e-05,   6.01415123e+06,   7.70693208e-03, 1.85838333e-01])
    return baseline


def set_baseline_eps_0_60_yesyesno(baseline):
    baseline["of_delta"] = 0.000000001
    baseline["dv_deltas"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])
    baseline["decision_variables_eps"] = numpy.array( \
        [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])
    return baseline


def get_baseline_point_0_60_yesyesno():
    return 181.34162033753552


# --------------------------------------------------------------------------- #
# Yes10-yes15-no5 0-60 hr

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


# --------------------------------------------------------------------------- #
# Yes15-no5-yes10 0-60 hr

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

# Nonlinear confidence regions
# --------------------------------------------------------------------------- #
# 0-20 hr

def set_baseline_nonlinconfreg_0_20(baseline):
    baseline["number_of_points"] = 5
    #[[0, 0], [8, 8], [9, 0], [9, 0]]
    baseline["intervals"] = [ \
        [6.7423531083919105e-05, 7.1302641907052986e-05], 
        [5762389.5624994077, 6378145.4846736873], 
        [0.0078654640574383552, 0.0086133532544531884], 
        [0.056175862279003279, 5.6175862279003272]]
    return baseline


def set_baseline_nonlinconfreg_0_20_lowconf(baseline):
    baseline["number_of_points"] = 4
    #[[0, 0], [0, 9], [4, 0], [9, 0]]
    baseline["intervals"] = [ \
        [6.9175518497167294e-05, 7.1302641907052973e-05],
        [5702299.2268772349, 5952809.792997444], 
        [0.0080379219184788138, 0.0081855207184086225], 
        [0.056175862279003279, 1.2635196340831445]]
    return baseline


# --------------------------------------------------------------------------- #
# 0-60 hr

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
# Yes-no-yes 0-60 hr

def set_baseline_nonlinconfreg_0_60_yesnoyes(baseline):
    baseline["number_of_points"] = 0
    # [9, 4], [9, 4], [9, 9], [8, 9]
    baseline["intervals"] = [ \
        [5.303839254978861e-05, 6.7928643137517991e-05], \
        [5900150.185800408, 59065454.091839552], \
        [0.01009237303638489, 0.01429891307608047], \
        [0.018628141421802392, 0.033995558368361149]]
    return baseline

# Linear confidence regions
# --------------------------------------------------------------------------- #
# 0-20 hr

def set_baseline_linconfreg_0_20(baseline):
    # TODO
    baseline["intervals"] = [ \
        [-3.3298285820135265e-05, 0.00017450561705501587], \
        [-49451538.410624318, 61357157.092140831], \
        [-0.12466235582771625, 0.14039328439852158], \
        [-239.32962521727927, 240.45314246285932]]
    baseline["ellipsoid"] = [ \
        [  2.98950610e-08, -5.02656235e+03, -1.09127528e-06,  1.47544377e-02], \
        [ -5.02656235e+03,  8.50040716e+15, -1.64934543e+07,  1.38933597e+10], \
        [ -1.09127528e-06, -1.64934543e+07,  4.86369289e-02, -7.21011214e+01], \
        [  1.47544377e-02,  1.38933597e+10, -7.21011214e+01,  1.59360739e+05]]
    baseline["delta"] = [ \
        [  0.00000001e-08,  0.00000001e+03,  0.00000001e-06,  0.00000001e-02], \
        [  0.00000001e+03,  0.00000001e+15,  0.00000001e+07,  0.00000001e+10], \
        [  0.00000001e-06,  0.00000001e+07,  0.00000001e-02,  0.00000001e+01], \
        [  0.00000001e-02,  0.00000001e+10,  0.00000001e+01,  0.00000001e+05]]
    return baseline


def set_baseline_linconfreg_0_20_lowconf(baseline):
    # TODO
    baseline["intervals"] = [ \
        [5.4023221176441136e-05, 8.7184110058439464e-05], \
        [-2888494.3784842957, 14794113.060000809], \
        [-0.013283033195825902, 0.029013961766631242], \
        [-37.719579760198528, 38.843097005778588]]
    baseline["ellipsoid"] = [ \
        [  5.62378564e-09, -9.45584596e+02, -2.05288032e-07,  2.77556868e-03], \
        [ -9.45584596e+02,  1.59907577e+15, -3.10270822e+06,  2.61358480e+09], \
        [ -2.05288032e-07, -3.10270822e+06,  9.14945992e-03, -1.35634863e+01], \
        [  2.77556868e-03,  2.61358480e+09, -1.35634863e+01,  2.99785518e+04]]
    baseline["delta"] = [ \
        [  0.00000001e-09,  0.00000001e+02,  0.00000001e-07,  0.00000001e-03], \
        [  0.00000001e+02,  0.00000001e+15,  0.00000001e+06,  0.00000001e+09], \
        [  0.00000001e-07,  0.00000001e+06,  0.00000001e-03,  0.00000001e+01], \
        [  0.00000001e-03,  0.00000001e+09,  0.00000001e+01,  0.00000001e+04]]
    return baseline


# --------------------------------------------------------------------------- #
# 0-60 hr

def set_baseline_linconfreg_0_60(baseline):
    # TODO
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

# --------------------------------------------------------------------------- #
# Yes-no-yes 0-60 hr

def set_baseline_linconfreg_0_60_yesnoyes(baseline):
    #[  7.56554088e-05   2.91525905e+07   1.12109587e-01   1.90596930e-01]
    baseline["intervals"] = [ \
        [-3.0646243181683128e-06, 0.00014824619334586535], \
        [-23246045.041966371, 35059135.860334285], \
        [-0.099179900018504408, 0.12503927405308463], \
        [-0.17612731808104753, 0.2050665415761122]]
    baseline["ellipsoid"] = [ \
        [  1.73525275e-08, -2.74919325e+03,  3.68822159e-06, -4.13995073e-06], \
        [ -2.74919325e+03,  2.57654113e+15, -5.77296913e+06,  1.33779063e+06], \
        [  3.68822159e-06, -5.77296913e+06,  3.81037994e-02, -5.41225289e-02], \
        [ -4.13995073e-06,  1.33779063e+06, -5.41225289e-02,  1.10132267e-01]]
    baseline["delta"] = [ \
        [  0.00000001e-08,  0.00000001e+03,  0.00000001e-06,  0.00000001e-06], \
        [  0.00000001e+03,  0.00000001e+15,  0.00000001e+06,  0.00000001e+06], \
        [  0.00000001e-06,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02], \
        [  0.00000001e-06,  0.00000001e+06,  0.00000001e-02,  0.00000001e-01]]
    return baseline
