
import common.io as coio
import results.plot_strips as replst
import results.plot_data as replda

import numpy as np

def read_trajectories_from_files(loc):
    raw = coio.read_from_headless_dataframe(loc)
    data = np.transpose(raw)
    time = data[0]
    vals = data[1:]
    return [time, vals]

def plot_tiled_calibration_and_validation_trajectories_at_record(config, locator):
    [time_measured, vals_measured] = read_trajectories_from_files( \
        locator["locator"].get_measured_calibration())
    # TODO: time_predicted
    [_, vals_predicted] = read_trajectories_from_files( \
        locator["locator"].get_predicted_calibration())
    [_, vals_error] = read_trajectories_from_files( \
        locator["locator"].get_error_calibration())
    # TODO: from predicted to observed
    data = replda.TimeCourseData()
    data.independent = time_measured
    data.measurements = vals_measured
    data.predictions = vals_predicted
    data.errors = vals_error
    replst.plot_measurements_with_trajectories_with_errors(data, config)
    #replst.show_all()
    # see reporting_unlegacy
    # for calib and valid
    # unfold time and trace
    # plot
    pass