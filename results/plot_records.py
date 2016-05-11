
import common.io as coio
import results.plot_strips as replst
import results.plot_data as replda
import results.plots_regions as replre
import results.plot_3d as repl3d

import numpy as np


def read_trajectories_from_files(loc):
    raw = coio.read_from_headless_dataframe(loc)
    if raw is None:
        return [None, None]
    data = np.transpose(raw)
    time = data[0]
    vals = data[1:]
    return [time, vals]


def read_multiple_realisation_data_points_from_files(loc):
    assert(loc is not None)
    raw = coio.read_from_csv(loc)
    return raw
    

def plot_tiled_calibration_and_validation_trajectories_at_record(config, locator):
    [time_measured, vals_measured] = read_trajectories_from_files( \
        locator["locator"].get_measured_calibration())
    # TODO: time_predicted
    [_, vals_predicted] = read_trajectories_from_files( \
        locator["locator"].get_predicted_calibration())
    # TODO: time_error
    [_, vals_error] = read_trajectories_from_files( \
        locator["locator"].get_error_calibration())
    # TODO: from predicted to observed
    data_calib = replda.TimeCourseData(). \
        set_independent(time_measured). \
        set_measurements(vals_measured). \
        set_predictions(vals_predicted). \
        set_errors(vals_error)

    [time_measured, vals_measured] = read_trajectories_from_files( \
        locator["locator"].get_measured_validation())
    # TODO: time_predicted
    [_, vals_predicted] = read_trajectories_from_files( \
        locator["locator"].get_predicted_validation())
    # TODO: time_error
    [_, vals_error] = read_trajectories_from_files( \
        locator["locator"].get_error_validation())
    # TODO: from predicted to observed
    data_valid = replda.TimeCourseData(). \
        set_independent(time_measured). \
        set_measurements(vals_measured). \
        set_predictions(vals_predicted). \
        set_errors(vals_error)
    if time_measured is None:
        data_valid = None

    replst.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
        data_calib, data_valid, config)


def plot_nonlinear_confidence_region_2D_projections_combinatorial_at_record(config, locator):
    realisations = read_multiple_realisation_data_points_from_files( \
        locator["locator"].get_multiple_realisations())
    
    replre.plot_nonlinear_confidence_region_2D_projections_combinatorial( \
        config, realisations)


def plot_nonlinear_confidence_region_3D_projections_combinatorial_at_record(config, locator):
    realisations = read_multiple_realisation_data_points_from_files( \
        locator["locator"].get_multiple_realisations())
    
    repl3d.plot_nonlinear_confidence_region_3D_projections_combinatorial( \
        config, realisations)
