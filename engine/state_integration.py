
import models.model_data as momoda
import data.data_splicing as dadasp
import solvers.initial_value as soiv

import numpy


# WIP: 2015-05-18, rename trajectory filters
def compute_timecourse_trajectories(model, problem):
    '''
    Compute timecourse trajectories and apply trajectory *splicing* filters if they exist
    This affects the outputs, not time
    return numpy.array with the trajectories (spliced or not)
    '''
    trajectories = soiv.compute_timecourse_trajectories(None, model, problem)
    if problem["output_filters"] is None or problem["output_filters"]["measurement_splices"] is None:
        return trajectories
    
    assert(problem["output_filters"]["measurement_splices"] is not None)
    spliced_trajectories = []
    for ii in range(len(model["states"])):
        spliced_trajectories.append( \
            dadasp.splice_data(problem["output_filters"]["measurement_splices"], trajectories[ii]))
    return numpy.asarray(spliced_trajectories)    


def compute_calibration_and_validation_timecourse_trajectories(model, problem):
    '''
    Raises     exception if "output filters" has not been defined
    returns    models.model_data.calib_valid_experimental_dataset
    '''
    trajectories = soiv.compute_timecourse_trajectories(None, model, problem)
    if problem["output_filters"] is None:
        assert(False)
        raise

    calib_trajectories = []
    for ii in range(len(model["states"])):
        calib_trajectories.append( \
            dadasp.splice_data( \
                dadasp.convert_mask_to_index_expression( \
                    problem["output_filters"]["calibration_mask"]),
                    trajectories[ii]))
    valid_trajectories = []
    for ii in range(len(model["states"])):
        valid_trajectories.append( \
            dadasp.splice_data( \
                dadasp.convert_mask_to_index_expression( \
                    problem["output_filters"]["validation_mask"]),
                    trajectories[ii]))
    
    calib_valid_trajectories = dict(momoda.calib_valid_experimental_dataset)
    
    calib_valid_trajectories["calib"]["time"] = dadasp.splice_data( \
        dadasp.convert_mask_to_index_expression( \
            problem["output_filters"]["calibration_mask"]),
            problem["time"])
    calib_valid_trajectories["valid"]["time"] = dadasp.splice_data( \
        dadasp.convert_mask_to_index_expression( \
            problem["output_filters"]["validation_mask"]),
            problem["time"])
    calib_valid_trajectories["calib"]["observables"] = numpy.asarray(calib_trajectories)
    calib_valid_trajectories["valid"]["observables"] = numpy.asarray(valid_trajectories)
    return calib_valid_trajectories
    
