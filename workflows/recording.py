
import common.environment as coen
import common.io as coio
import common.results as core
import engine.state_integration as enstin
import models.model_data_utils as momodaut
import setups.setup_data_utils as sesedaut

def write_trajectories_to_files(time, measured, predicted, app):
    coio.write_as_dataframe_to_csv(\
        core.append_traces_to_time_and_transpose(time, measured), \
        coen.get_results_location() + app + "_measured.csv")
    coio.write_as_dataframe_to_csv(\
        core.append_traces_to_time_and_transpose(time, predicted), \
        coen.get_results_location() + app + "_predicted.csv")


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
    
    write_trajectories_to_files(\
        data_instance["calib"]["time"], \
        data_instance["calib"]["observables"], \
        predictions["calib"]["observables"], \
        "calib")
    write_trajectories_to_files(
        data_instance["valid"]["time"], \
        data_instance["valid"]["observables"], \
        predictions["valid"]["observables"], \
        "valid")
