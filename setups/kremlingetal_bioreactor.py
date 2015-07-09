
import copy
import numpy

import common.utilities as cu
import data.experimental_data_splicing as deds
import workflows.protocol_data as wpd
import metrics.ordinary_differential as mod
import models.kremlingetal_bioreactor as mkb
import models.model_data
import models.model_data_utils as mmdu
import setups.setup_data
import setups.numerics as senu
import solvers.local_sensitivities
import solvers.solver_data as sosoda
import solvers.solver_utils as sosout

import models.model_data as momoda


def get_parameters_to_be_estimated():
    return [0, 3, 8, 9]


def do_model_setup(model_key):
    p = numpy.ones(len(mkb.pmap))
    for par in mkb.pmap.items():
        p[par[1]] = mkb.pvec[par[0]]
    
    u = numpy.ones(len(mkb.umap))
    for inp in mkb.umap.items():
        u[inp[1]] = mkb.uvec_0h[inp[0]]
    
    x = numpy.ones(len(mkb.xmap))
    
    for ste in mkb.xmap.items():
        x[ste[1]] = mkb.xvec[ste[0]]
    
    model_data = dict(models.model_data.model_structure)
    model_data["parameters"] = copy.deepcopy(p)
    model_data["inputs"] = copy.deepcopy(u)
    model_data["states"] = copy.deepcopy(x)
    if model_key is "modelA":
        model_data["model"] = mkb.evaluate_modelA
    else:
        model_data["model"] = mkb.evaluate_modelB
    
    return model_data


def do_model_setup_model_A():
    return do_model_setup("modelA")


def do_model_setup_model_B():
    return do_model_setup("modelB")

# --------------------------------------------------------------------------- #

def do_get_published_data_0_20():
    # TODO: handle gracefully
    published_data = open("C:/documents/resproj/bench/data_time_0_20.txt", 'r')
    data = numpy.loadtxt(published_data)
    trajectories_without_V = cu.sliceit_astrajectory(data)
    return trajectories_without_V


def do_get_published_data_0_60():
    # TODO: handle gracefully
    published_data = open("C:/documents/resproj/bench/data_time_0_60.txt", 'r')
    data = numpy.loadtxt(published_data)
    trajectories_without_V = cu.sliceit_astrajectory(data)
    return trajectories_without_V


def do_get_published_data_spliced_111111():
    trajectories_without_V = do_get_published_data_0_20()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_spliced_111000():
    trajectories_without_V = do_get_published_data_0_20()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111000(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_spliced_000111():
    trajectories_without_V = do_get_published_data_0_20()
    spliced_trajectories = deds.splice_raw_data_with_pattern_000111(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_0_60_spliced_111111():
    trajectories_without_V = do_get_published_data_0_60()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_0_60_spliced_yesyesno():
    trajectories_without_V = do_get_published_data_0_60()
    spliced_trajectories = deds.splice_raw_data_with_pattern_multistage_yesyesno(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_0_60_spliced_yes10yes10no5():
    trajectories_without_V = do_get_published_data_0_60()
    spliced_trajectories = deds.splice_raw_data_with_pattern_multistage_yes10yes15no5(trajectories_without_V)
    return spliced_trajectories
    
    
def do_get_published_data_0_60_spliced_yesnoyes():
    trajectories_without_V = do_get_published_data_0_60()
    spliced_trajectories = deds.splice_raw_data_with_pattern_multistage_yesnoyes(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_0_60_spliced_yes15no5yes10():
    trajectories_without_V = do_get_published_data_0_60()
    spliced_trajectories = deds.splice_raw_data_with_pattern_multistage_yes15no5yes10(trajectories_without_V)
    return spliced_trajectories
    

# --------------------------------------------------------------------------- #

def do_base_problem_setup(model_data, data_instance):
    """
    returns problem
    """
    assert(model_data is not None)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    problem_data["time"] = data_instance["time"]
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["performance_observables"] = mod.sums_squared_residuals_unlegacy
    problem_data["performance_measure"] = mod.sum_squared_residuals
    problem_data["confidence_region"]["performance_measure"] = mod.sum_squared_residuals
    problem_data["confidence_region"]["confidence"] = 0.95
    problem_data["parameter_indices"] = get_parameters_to_be_estimated()
    problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
    
    for ii in range(len(problem_data["parameter_indices"])):
        problem_data["parameters"][ii] = copy.deepcopy(model_data["parameters"][problem_data["parameter_indices"][ii]])
    
    problem_data["bounds"] = [(0,1E30), (0,1E30), (0,1E30), (0,1E30)]
    assert(len(get_parameters_to_be_estimated()) == len(problem_data["bounds"]))
    
    problem_data["output_indices"] = [1, 2, 3, 4, 5]
    if data_instance is not None:
        problem_data["outputs"] = data_instance["observables"]
        assert(len(["output_indices"]) == len(["outputs"]))

    return problem_data


def do_problem_setup(model_data, data_instance):
    return do_base_problem_setup(model_data, data_instance)


def do_problem_setup_unlegacy(model_data, data_instance):
    problem = do_base_problem_setup(model_data, data_instance)
    problem["time"] = numpy.arange(0,61,2)
    return problem
    

# TODO: extract
def do_problem_setup_0_60(model_data, data_instance):
    problem = do_base_problem_setup(model_data, data_instance)
    forcing_inputs = copy.deepcopy(models.model_data.forcing_function_profile)
    forcing_inputs["continuous_time_intervals"] = [0,20,30,60]
    forcing_inputs["piecewise_constant_inputs"] = [numpy.asarray([0.25,0.25,2]), \
                                                   numpy.asarray([0.35,0.35,2]), \
                                                   numpy.asarray([0.35,0.35,0.5])]
    problem["forcing_inputs"] = forcing_inputs
    problem["output_filters"] = dict(momoda.output_filters)
    problem["output_filters"]["measurement_splices"] = [slice(0,31,1)]
    problem["output_filters"]["calibration_mask"] = [31]
    problem["output_filters"]["validation_mask"] = [0]
    return problem


# unlegacy
def do_base_problem_setup_0_60(model_data, data_instance):
    problem = do_problem_setup_unlegacy(model_data, data_instance)
    forcing_inputs = copy.deepcopy(models.model_data.forcing_function_profile)
    forcing_inputs["continuous_time_intervals"] = [0,20,30,60]
    forcing_inputs["piecewise_constant_inputs"] = [numpy.asarray([0.25,0.25,2]), \
                                                   numpy.asarray([0.35,0.35,2]), \
                                                   numpy.asarray([0.35,0.35,0.5])]
    problem["forcing_inputs"] = forcing_inputs
    return problem


def do_problem_setup_0_60_spliced_yesyesno(model_data, data_instance):
    problem = do_problem_setup_unlegacy(model_data, data_instance)
    forcing_inputs = copy.deepcopy(models.model_data.forcing_function_profile)
    forcing_inputs["continuous_time_intervals"] = [0,20,30,60]
    forcing_inputs["piecewise_constant_inputs"] = [numpy.asarray([0.25,0.25,2]), \
                                                   numpy.asarray([0.35,0.35,2]), \
                                                   numpy.asarray([0.35,0.35,0.5])]
    problem["forcing_inputs"] = forcing_inputs
    problem["output_filters"] = dict(momoda.output_filters)
    problem["output_filters"]["measurement_splices"] = [slice(0,15,1)]
    problem["output_filters"]["calibration_mask"] = [15]
    problem["output_filters"]["validation_mask"] = [0,15]
    return problem


def do_problem_setup_0_60_spliced_yes10yes15no5(model_data, data_instance):
    problem = do_base_problem_setup_0_60(model_data, data_instance)
    problem["output_filters"] = dict(momoda.output_filters)
    problem["output_filters"]["measurement_splices"] = []
    problem["output_filters"]["calibration_mask"] = [25]
    problem["output_filters"]["validation_mask"] = [0,25]
    return problem


def do_problem_setup_0_60_spliced_yes15no5yes10(model_data, data_instance):
    problem = do_base_problem_setup_0_60(model_data, data_instance)
    problem["output_filters"] = dict(momoda.output_filters)
    problem["output_filters"]["measurement_splices"] = []
    problem["output_filters"]["calibration_mask"] = [15,20]
    problem["output_filters"]["validation_mask"] = [0,15,20]
    return problem


def do_problem_setup_0_60_spliced_yesnoyes(model_data, data_instance):
    problem = do_problem_setup_unlegacy(model_data, data_instance)
    forcing_inputs = copy.deepcopy(models.model_data.forcing_function_profile)
    forcing_inputs["continuous_time_intervals"] = [0,20,30,60]
    forcing_inputs["piecewise_constant_inputs"] = [numpy.asarray([0.25,0.25,2]), \
                                                   numpy.asarray([0.35,0.35,2]), \
                                                   numpy.asarray([0.35,0.35,0.5])]
    problem["forcing_inputs"] = forcing_inputs
    problem["output_filters"] = dict(momoda.output_filters)
    problem["output_filters"]["measurement_splices"] = [10,15]
    problem["output_filters"]["calibration_mask"] = [10,15]
    problem["output_filters"]["validation_mask"] = [0,10,15]
    return problem


def do_problem_setup_with_exclude(model_data, data_instance):
    problem_data = do_base_problem_setup(model_data, data_instance)
    problem_data["initial"] = "exclude"
    return problem_data
    
    
def do_problem_setup_with_covariance_1(model_data, data_instance):
    problem_data = do_problem_setup(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-001, 2.46E-001, 2.53E-001, 1.16E-002, 3.20E-002])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_0_60_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_0_60(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_0_60_spliced_yesyesno_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_0_60_spliced_yesyesno(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_0_60_spliced_yes10yes15no5_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_0_60_spliced_yes10yes15no5(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_0_60_spliced_yesnoyes_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_0_60_spliced_yesnoyes(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_0_60_spliced_yes15no5yes10_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_0_60_spliced_yes15no5yes10(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_with_covariance_2_and_low_confidence(model_data, data_instance):
    problem_data = do_problem_setup_with_covariance_2(model_data, data_instance)
    do_modify_problem_using_low_confidence(problem_data)
    return problem_data


def do_modify_problem_using_low_confidence(problem):
    problem["confidence_region"]["confidence"] = 0.25


def do_problem_setup_with_exclude_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_with_exclude(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data

# --------------------------------------------------------------------------- #

def do_sensitivity_setup():
    return solvers.local_sensitivities.compute_timecourse_trajectories_and_sensitivities


def do_sensitivity_model_setup():
    model = do_model_setup_model_B()
    x = model["states"]
    dim_dv = 4
    model["states"] = numpy.hstack((x, numpy.zeros(len(mkb.xvec) * dim_dv)))
    model["model"] = mkb.evaluate_system_and_sensitivities
    return model


def do_sensitivity_problem_setup(model_data, data_instance):
    assert(model_data is not None)
    assert(data_instance is not None)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    problem_data["time"] = data_instance["time"]
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["parameter_indices"] = get_parameters_to_be_estimated()
    problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
    
    for ii in range(len(problem_data["parameter_indices"])):
        problem_data["parameters"][ii] = copy.deepcopy(model_data["parameters"][problem_data["parameter_indices"][ii]])
    
    problem_data["output_indices"] = [1, 2, 3, 4, 5]
    problem_data["outputs"] = data_instance["observables"]
    assert(len(["output_indices"]) == len(["outputs"]))

    return problem_data

# --------------------------------------------------------------------------- #

# TODO: think where this should go
def do_labels():
    labels = [""] * len(mkb.xmap)
    for ste in mkb.xmap.items():
        labels[ste[1]] = ste[0]
    
    return labels

# --------------------------------------------------------------------------- #

# TODO: 2015-05-15, split into abstract and NM
def do_algorithm_setup(instrumentation_data):
    p = numpy.ones(len(mkb.pmap))
    for par in mkb.pmap.items():
        p[par[1]] = mkb.pvec[par[0]]
    pi = get_parameters_to_be_estimated()
    initial_guesses = []
    for ii in range(len(pi)):
        initial_guesses.append(copy.deepcopy(p[pi[ii]]))
    algorithm_data = dict(sosoda.algorithm_structure)
    if instrumentation_data is not None:
        algorithm_data["callback"] = instrumentation_data["logger"].log_decision_variables
    algorithm_data["initial_guesses"] = initial_guesses
    algorithm_data["method"] = "Nelder-Mead"
    return algorithm_data

    
def do_algorithm_setup_using_slsqp(instrumentation_data):
    algorithm_data = do_algorithm_setup(instrumentation_data)
    algorithm_data["method"] = "SLSQP"
    return algorithm_data


def do_algorithm_setup_using_slsqp_with_positivity(instrumentation_data):
    algorithm_data = do_algorithm_setup_using_slsqp(instrumentation_data)
    logger = sosout.DecisionVariableLogger()
    algorithm_data["callback"] = logger.let_decision_variables_be_positive_and_log
    return algorithm_data


def do_algorithm_config_mcm_ranges_10xpm(data):
    data["decision_variable_ranges"] = [ \
        (7.21144459e-05*0.1, 7.21144459e-05*10), \
        (5.92826673e+06*0.1, 5.92826673e+06*10), \
        (1.21249611e-02*0.1, 1.21249611e-02*10), \
        (1.71735070e-02*0.1, 1.71735070e-02*10)]
    return data


def do_algorithm_setup_global_neldermead_100_10xpm(instrumentation_data):
    data = dict(senu.sonlin.somcmlesq.montecarlo_multiple_optimisation_params)
    data = senu.do_config_mcm_100(data)
    data = senu.do_config_mcmls_nlp(data)
    data = senu.do_config_mcmls_nm(data)
    data = do_algorithm_config_mcm_ranges_10xpm(data)
    return data

# --------------------------------------------------------------------------- #

def do_instrumentation_setup():
    instrumentation_data = dict(setups.setup_data.instrumentation_data)
    instrumentation_data["logger"] = sosout.DecisionVariableLogger()
    return instrumentation_data


def do_protocol_setup():
    protocol_data = dict(wpd.protocol_data)
    protocol_data["performance_measure"] = mod.sum_squared_residuals
    return protocol_data

# --------------------------------------------------------------------------- #

def do_experiment_setup_base():
    config = copy.deepcopy(setups.setup_data.experiment_setup)
    config["algorithm_setup"] = do_algorithm_setup
    config["data_setup"] = do_get_published_data_spliced_111111
    config["model_setup"] = do_model_setup_model_B
    config["problem_setup"] = do_problem_setup_with_covariance_2
    config["protocol_setup"] = do_protocol_setup
    config["protocol_step"]["calib"] = "do"
    config["protocol_step"]["valid"] = "do"
    # TODO: () or not ()?
    config["sensitivity_setup"] = do_sensitivity_setup()
    return config


def do_experiment_setup_0_20():
    return do_experiment_setup_base()
    

def do_experiment_setup_0_60():
    config = copy.deepcopy(setups.setup_data.experiment_setup)
    config["algorithm_setup"] = do_algorithm_setup
    config["data_setup"] = do_get_published_data_0_60_spliced_111111
    config["model_setup"] = do_model_setup_model_B
    config["problem_setup"] = do_problem_setup_0_60_with_covariance_2
    config["protocol_setup"] = do_protocol_setup
    config["protocol_step"]["calib"] = "do"
    config["protocol_step"]["valid"] = "do"
    # TODO: () or not ()?
    config["sensitivity_setup"] = do_sensitivity_setup()
    return config


def do_experiment_setup_0_60_with_global_neldermead_100_10xpm():
    config = do_experiment_setup_0_60()
    config["algorithm_setup"] = do_algorithm_setup_global_neldermead_100_10xpm
    return config


def do_experiment_setup_0_60_with_slsqp_with_positivity():
    config = do_experiment_setup_0_60()
    config["algorithm_setup"] = do_algorithm_setup_using_slsqp_with_positivity
    return config


def do_experiment_setup_0_60_spliced_yesyesno():
    config = do_experiment_setup_0_60()
    config["problem_setup"] = do_problem_setup_0_60_spliced_yesyesno_with_covariance_2
    config["data_setup"] = do_get_published_data_0_60_spliced_yesyesno
    return config
    

def do_experiment_setup_0_60_spliced_yesyesno_with_global_neldermead_100_10xpm():
    config = do_experiment_setup_0_60_spliced_yesyesno()
    config["algorithm_setup"] = do_algorithm_setup_global_neldermead_100_10xpm
    return config


def do_experiment_setup_0_60_spliced_yesnoyes():
    config = do_experiment_setup_0_60()
    config["problem_setup"] = do_problem_setup_0_60_spliced_yesnoyes_with_covariance_2
    config["data_setup"] = do_get_published_data_0_60_spliced_yesnoyes
    return config


def do_experiment_setup_0_60_spliced_yesnoyes_with_global_neldermead_100_10xpm():
    config = do_experiment_setup_0_60_spliced_yesnoyes()
    config["algorithm_setup"] = do_algorithm_setup_global_neldermead_100_10xpm
    return config


def do_experiment_setup_0_60_spliced_yes10yes15no5():
    config = do_experiment_setup_0_60()
    config["problem_setup"] = do_problem_setup_0_60_spliced_yes10yes15no5_with_covariance_2
    config["data_setup"] = do_get_published_data_0_60_spliced_yes10yes10no5
    return config


def do_experiment_setup_0_60_spliced_yes10yes15no5_with_global_neldermead_100_10xpm():
    config = do_experiment_setup_0_60_spliced_yes10yes15no5()
    config["algorithm_setup"] = do_algorithm_setup_global_neldermead_100_10xpm
    return config


def do_experiment_setup_0_60_spliced_yes15no5yes10():
    config = do_experiment_setup_0_60()
    config["problem_setup"] = do_problem_setup_0_60_spliced_yes15no5yes10_with_covariance_2
    config["data_setup"] = do_get_published_data_0_60_spliced_yes15no5yes10
    return config


def do_experiment_setup_0_60_spliced_yes15no5yes10_with_global_neldermead_100_10xpm():
    config = do_experiment_setup_0_60_spliced_yes15no5yes10()
    config["algorithm_setup"] = do_algorithm_setup_global_neldermead_100_10xpm
    return config


def do_experiment_setup_0_20_twice():
    config = copy.deepcopy(setups.setup_data.experiment_setup)
    config["algorithm_setup"] = do_algorithm_setup
    config["data_setup"] = do_get_published_data_spliced_111111
    config["model_setup"] = do_model_setup_model_B
    config["problem_setup"] = do_problem_setup_twice_with_covariance_2
    config["protocol_setup"] = do_protocol_setup
    config["protocol_step"]["calib"] = "do"
    config["protocol_step"]["valid"] = "donot"
    # TODO: () or not ()?
    config["sensitivity_setup"] = do_sensitivity_setup()
    return config


def do_problem_setup_twice_with_covariance_2(model_data, data_instance):
    problem_data = do_problem_setup_twice(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.array([3.80E-002, 2.46E-002, 2.53E-002, 1.16E-003, 3.20E-003])
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data


def do_problem_setup_twice(model_data, data_instance):
    problem = do_base_problem_setup(model_data, data_instance)
    experiment = {}

    experiment["initial_condition_measurements"] = copy.deepcopy(problem["initial_conditions"])
    experiment["time"] = copy.deepcopy(problem["time"])
    experiment["input_measurements"] = copy.deepcopy(problem["inputs"])
    experiment["output_measurements"] = copy.deepcopy(problem["outputs"])

    problem["experiments"] = []
    problem["experiments"].append(experiment)
    problem["experiments"].append(experiment)
    
    problem["performance_measure"] = mod.sum_squared_residuals
    return problem

# --------------------------------------------------------------------------- #

def do_experiment_protocol_setup_0_20_calib_ncr():
    protocol = copy.deepcopy(setups.setup_data.experiment_protocol)
    protocol["steps"] = []
    setup = do_experiment_setup_0_20()
    setup["algorithm_setup"] = do_algorithm_setup_using_slsqp_with_positivity
    protocol["steps"].append(copy.deepcopy(setup))
    setup["algorithm_setup"] = senu.do_config_mcmiv_100
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol


def do_experiment_protocol_setup_0_20_calib_ncr_low_confidence():
    protocol = copy.deepcopy(setups.setup_data.experiment_protocol)
    protocol["steps"] = []
    setup = do_experiment_setup_0_20()
    setup["problem_setup"] = do_problem_setup_with_covariance_2_and_low_confidence
    setup["algorithm_setup"] = do_algorithm_setup_using_slsqp_with_positivity
    protocol["steps"].append(copy.deepcopy(setup))
    setup["algorithm_setup"] = senu.do_config_mcmiv_100
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol


def do_experiment_protocol_setup_0_60_calib_ncr():
    protocol = copy.deepcopy(setups.setup_data.experiment_protocol)
    protocol["steps"] = []
    setup = do_experiment_setup_0_60()
    setup["algorithm_setup"] = do_algorithm_setup_using_slsqp_with_positivity
    setup["local_setup"]["do_plotting"] = True
    protocol["steps"].append(copy.deepcopy(setup))
    setup["algorithm_setup"] = senu.do_config_mcmiv_10
    setup["local_setup"]["do_plotting"] = True
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol


def do_experiment_protocol_setup_0_20_2x_calib_ncr():
    protocol = copy.deepcopy(setups.setup_data.experiment_protocol)
    protocol["steps"] = []
    setup = do_experiment_setup_0_20_twice()
    setup["algorithm_setup"] = do_algorithm_setup_using_slsqp_with_positivity
    protocol["steps"].append(copy.deepcopy(setup))
    setup["algorithm_setup"] = senu.do_config_mcmiv_100
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol


def do_experiment_protocol_setup_0_60_yesnoyes_ncr():
    protocol = copy.deepcopy(setups.setup_data.experiment_protocol)
    protocol["steps"] = []
    setup = do_experiment_setup_0_60_spliced_yesnoyes()
    setup["algorithm_setup"] = do_algorithm_setup_using_slsqp_with_positivity
    protocol["steps"].append(copy.deepcopy(setup))
    setup["algorithm_setup"] = senu.do_config_mcmiv_100
    protocol["steps"].append(copy.deepcopy(setup))
    return protocol
