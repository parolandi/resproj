
import common.io as coio
import common.results as core
import engine.state_integration as enstin
import models.model_data_utils as momodaut
import setups.setup_data_utils as sesedaut

def write_trajectories_to_file(time, trajectories, url):
    coio.write_as_dataframe_to_csv(\
        core.append_traces_to_time_and_transpose(time, trajectories), \
        url)


def record_calibration_and_validation_trajectories_at_point(config, point):
    '''
    Does as it says on the tin
    point
    config: models.model_data.calib_valid_experimental_dataset
    '''
    model_data, data_instance, problem_data, _ = \
        sesedaut.get_model_data_problem_protocol_with_calib(config)
    momodaut.apply_values_to_parameters(\
        point["decision_variables"], model_data, problem_data)

    # TODO: assert dimensions are correct
    trajectories = enstin.compute_calibration_and_validation_timecourse_trajectories(\
        model_data, problem_data)
    predictions = momodaut.get_observable_calibration_and_validation_trajectories(\
        trajectories, problem_data)
    
    write_trajectories_to_file(\
        data_instance["calib"]["time"], \
        data_instance["calib"]["observables"], \
        config["locator"].get_measured_calibration())
    write_trajectories_to_file(\
        data_instance["calib"]["time"], \
        predictions["calib"]["observables"], \
        config["locator"].get_predicted_calibration())
    write_trajectories_to_file(\
        data_instance["valid"]["time"], \
        data_instance["valid"]["observables"], \
        config["locator"].get_measured_validation())
    write_trajectories_to_file(\
        data_instance["valid"]["time"], \
        predictions["valid"]["observables"], \
        config["locator"].get_predicted_validation())
