
import engine.state_integration as enstin
import models.model_data_utils as momodaut
import results.plot_tiles as replti
import setups.setup_data_utils as sesedaut


'''
A collection or "reporting" methods that require more than simple plotting of data series
as they demand the calculation of trajectories, etc
'''

# WIP: 2015-05-25; point could be None
def plot_tiled_calibration_and_validation_trajectories_at_point(config, point):
    '''
    Does as it says on the tin
    point
    config: models.model_data.calib_valid_experimental_dataset
    '''
    model_data, data_instance, problem_data, _ = sesedaut.get_model_data_problem_protocol(config)
    momodaut.apply_values_to_parameters(point["decision_variables"], model_data, problem_data)

    # TODO: assert dimensions are correct
    # do plotting
    trajectories = enstin.compute_calibration_and_validation_timecourse_trajectories(model_data, problem_data)
    predictions = momodaut.get_observable_calibration_and_validation_trajectories(trajectories, problem_data)
    replti.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
        data_instance["calib"]["time"], data_instance["calib"]["observables"], predictions["calib"]["observables"], None, \
        data_instance["valid"]["time"], data_instance["valid"]["observables"], predictions["valid"]["observables"], None)
    replti.show_all()
