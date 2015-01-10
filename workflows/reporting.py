
import models.model_data_utils as mmdu
import results.plot_tiles as rpt
import solvers.initial_value as siv

import numpy


'''
config: models.model_data.calib_valid_experimental_dataset
'''
def plot_tiled_calibration_and_validation_trajectories_at_point(config, point):
    # setup
    model_data = config["model_setup"]()
    data_instance = config["data_setup"]()
    # do calib trajectories
    problem_data  = config["problem_setup"](model_data, data_instance["calib"])
    mmdu.apply_values_to_parameters(point["decision_variables"], model_data, problem_data)
    calib_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
    calib_observables = mmdu.get_observable_trajectories(problem_data, calib_trajectories)
    # do valid trajectories
    problem_data  = config["problem_setup"](model_data, data_instance["valid"])
    valid_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
    valid_observables = mmdu.get_observable_trajectories(problem_data, valid_trajectories)
    # do plotting
    rpt.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], calib_observables, None, \
        data_instance["valid"]["time"], data_instance["valid"]["observables"], valid_observables, None)
    rpt.show_all()


# TODO: error should be parameterisable
def plot_tiled_calibration_validation_and_residual_trajectories_at_point(config, point):
    # setup
    model_data = config["model_setup"]()
    data_instance = config["data_setup"]()
    # do calib trajectories
    problem_data  = config["problem_setup"](model_data, data_instance["calib"])
    mmdu.apply_values_to_parameters(point["decision_variables"], model_data, problem_data)
    calib_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
    calib_observables = mmdu.get_observable_trajectories(problem_data, calib_trajectories)
    # do valid trajectories
    problem_data  = config["problem_setup"](model_data, data_instance["valid"])
    valid_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
    valid_observables = mmdu.get_observable_trajectories(problem_data, valid_trajectories)
    
    calib_errors = []
    valid_errors = []
    cvm = problem_data["measurements_covariance_trace"]
    calib_dimT = len(data_instance["calib"]["time"])
    valid_dimT = len(data_instance["valid"]["time"])
    error_factor = 3
    for ii in range(len(cvm)):
        calib_errors.append(error_factor * numpy.ones(calib_dimT) * cvm[ii])
        valid_errors.append(error_factor * numpy.ones(valid_dimT) * cvm[ii])

    # do plotting
    rpt.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], calib_observables, calib_errors, \
        data_instance["valid"]["time"], data_instance["valid"]["observables"], valid_observables, valid_errors)
    rpt.plot_residual_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], calib_observables, calib_errors, \
        data_instance["valid"]["time"], data_instance["valid"]["observables"], valid_observables, valid_errors)
    rpt.show_all()