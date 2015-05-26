
import data.generator as dg
import models.model_data_utils as mmdu
import results.plot_tiles as rpt
import solvers.initial_value as siv


def plot_tiled_trajectories_at_point(config, point):
    '''
    Legacy-ish as of 2015-05-26
    '''
    # setup
    model_data = config["model_setup"]()
    data_instance = config["data_setup"]()
    # do calib trajectories
    problem_data  = config["problem_setup"](model_data, data_instance["calib"])
    mmdu.apply_values_to_parameters(point["decision_variables"], model_data, problem_data)
    calib_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
    calib_observables = mmdu.get_observable_trajectories(problem_data, calib_trajectories)
    # do plotting
    rpt.plot_measurements_with_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], calib_observables, None)
    rpt.show_all()


def plot_tiled_calibration_and_validation_trajectories_at_point(config, point):
    '''
    Legacy-ish as of 2015-05-26
    '''
    '''
    config: models.model_data.calib_valid_experimental_dataset
    '''
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
    '''
    Legacy-ish as of 2015-05-26
    '''
    '''
    config: models.model_data.calib_valid_experimental_dataset
    '''
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
    
    calib_errors, valid_errors = dg.compute_measurement_errors(problem_data, data_instance)

    # do plotting
    rpt.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], calib_observables, calib_errors, \
        data_instance["valid"]["time"], data_instance["valid"]["observables"], valid_observables, valid_errors)
    rpt.plot_residual_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], calib_observables, calib_errors, \
        data_instance["valid"]["time"], data_instance["valid"]["observables"], valid_observables, valid_errors)
    rpt.show_all()