
import setups.kremlingetal_bioreactor as sekrbi

import copy

import algorithms.algorithm_data as alalda
import algorithms.algorithm_setup as alalse
import setups.setup_data as seseda
import solvers.solver_utils as sosout

# --------------------------------------------------------------------------- #
# Algorithm setup

def do_algorithm_setup_default(instrumentation_data):
    """
    Settings as follows
    solvers.model_calibration.least_squares.numerics        := lq.solve
    solvers.model_calibration.least_squares.method          := nelder-mead
    solvers.model_calibration.least_squares.initial_guesses := nominal
    solvers.model_calibration.least_squares.call_back       := none
    solvers.parameter_confidence_estimation.region_estimation.nonlinear_programming.numerics := nlpi.solve
    solvers.parameter_confidence_estimation.region_estimation.nonlinear_programming.call     := nlpi.lq
    solvers.parameter_confidence_estimation.region_estimation.nonlinear_programming.method   := 'slsqp'
    solvers.parameter_confidence_estimation.region_estimation.nonlinear_programming.callback := dvs-positive-and-log
    solvers.parameter_confidence_estimation.region_estimation.monte_carlo_simulation.numerics                 := mcmiv.solve
    solvers.parameter_confidence_estimation.region_estimation.monte_carlo_simulation.number_of_trials         := 10
    solvers.parameter_confidence_estimation.region_estimation.monte_carlo_simulation.decision_variable_ranges := 0.1,10
    """
    algorithm_data = dict(alalda.algorithmic_data)
    algorithm_data["solvers"] = dict(alalda.solvers_data)
    
    algorithm_data["solvers"]["model_calibration"] = dict(alalda.numerics_data)
    ls = algorithm_data["solvers"]["model_calibration"]["least_squares"]

    ls["numerics"] = alalse.sonlpi.solesq.solve
    ls["method"] = 'Nelder-Mead'
    ls["initial_guesses"] = [7e-05, 6000000.0, 0.0168, 0.01]
    ls["callback"] = None
    
    algorithm_data["solvers"]["parameter_confidence_estimation"] = dict(alalda.numerics_data)
    re = algorithm_data["solvers"]["parameter_confidence_estimation"]["region_estimation"]
    
    re["nonlinear_programming"]["numerics"] = alalse.sonlpi.solve_unlegacy
    re["nonlinear_programming"]["call"] = alalse.sonlpi.solesq
    re["nonlinear_programming"]["method"] = 'SLSQP'
    logger = sosout.DecisionVariableLogger()
    re["nonlinear_programming"]["callback"] = logger.let_decision_variables_be_positive_and_log
    
    re["monte_carlo_simulation"]["numerics"] = alalse.somcmiv.solve
    re["monte_carlo_simulation"]["number_of_trials"] = 10
    sekrbi.do_algorithm_config_mcm_ranges_10xpm(re["monte_carlo_simulation"])  

    return algorithm_data

# --------------------------------------------------------------------------- #
# Protocol setup

def do_protocol_setup_0_20_default():
    protocol = copy.deepcopy(seseda.experiment_protocol)
    protocol["steps"] = []
    setup = sekrbi.do_experiment_setup_0_20()
    setup["algorithm_setup"] = do_algorithm_setup_default
    setup["local_setup"]["do_plotting"] = False
    protocol["steps"].append(copy.deepcopy(setup))
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol


def do_protocol_setup_0_20_low_confidence():
    protocol = do_protocol_setup_0_20_default()
    problem = sekrbi.do_problem_setup_with_covariance_2_and_low_confidence
    protocol["steps"][0]["problem_setup"] = problem
    protocol["steps"][1]["problem_setup"] = problem
    return protocol


def do_protocol_setup_0_20_2x_default():
    protocol = copy.deepcopy(seseda.experiment_protocol)
    protocol["steps"] = []
    setup = sekrbi.do_experiment_setup_0_20_twice()
    setup["algorithm_setup"] = do_algorithm_setup_default
    setup["local_setup"]["do_plotting"] = False
    protocol["steps"].append(copy.deepcopy(setup))
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol


def do_protocol_setup_0_60_default():
    protocol = copy.deepcopy(seseda.experiment_protocol)
    protocol["steps"] = []
    setup = sekrbi.do_experiment_setup_0_60()
    setup["algorithm_setup"] = do_algorithm_setup_default
    setup["local_setup"]["do_plotting"] = False
    protocol["steps"].append(copy.deepcopy(setup))
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol
