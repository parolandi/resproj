
import matplotlib.pyplot as pp
import numpy

import results.plot as rp


def show_all():
    pp.show()


def get_plot_colours(dim):
    assert(dim <= 6)
    return ['r', 'g', 'b', 'y', 'c', 'm']
    

# TODO: parameterise, generalise
# WIP: needs to be re-worked
def plot_fit(independent_meas, measurements, independent_pred, predictions, titles, title):
    # TODO assertions
    
    no_rows = 3
    no_cols = 2
    plot_count = 1
    fig = pp.figure(1)
    x_meas = independent_meas
    y_meas = measurements
    x_pred = independent_pred
    y_pred = predictions
    for ii in range(len(y_meas)):
        sp = fig.add_subplot(no_rows, no_cols, plot_count)
        sp.plot(x_meas, y_meas[ii], 'o')
        sp.plot(x_pred, y_pred[ii], '-')
        sp.set_xlim(x_pred[0], x_pred[len(x_pred)-1])
        if titles is not None:
            sp.set_title(titles[ii])
        plot_count += 1
    pp.subplots_adjust(hspace = 0.4)
    if title is not None:
        pp.suptitle(title)
    pp.show()


'''
Plot states and sensitivities in a tiled layout
'''
# TODO: consider removing dim_dv
def plot_states_and_sensitivities(time, states, sensitivities, dim_dv):
    no_rows = dim_dv+1
    no_cols = len(states)
    fig = pp.figure(1)
    for dv_col in range(no_cols):
        sp = fig.add_subplot(no_rows, no_cols, dv_col+1)
        sp.plot(time, states[dv_col])
        for x_row in range(no_rows-1):
            plot_no = no_cols*(x_row+1)+(dv_col+1)
            sp = fig.add_subplot(no_rows, no_cols, plot_no)
            sp.plot(time, sensitivities[dim_dv*dv_col+x_row])
    pp.show()


# TODO: refactor and make DRY
def plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
    independent_calib, measurements_calib, predictions_calib, errors_calib, \
    independent_valid, measurements_valid, predictions_valid, errors_valid):
    """
    errors_calib and errors_valid can be None
    """
    # TODO: pre-conditions
    
    errors_provided = True
    if errors_calib is None:
        assert(errors_valid is None)
        errors_provided = False
    
    dim_obs = len(measurements_calib)
    fig = pp.figure(1)
    plot_data = {}
    plot_data["figure"] = fig
    plot_data["no_rows"] = dim_obs
    plot_data["no_cols"] = 1
    plot_colours = get_plot_colours(dim_obs)
    calib_errors = None
    valid_errors = None
    for ii in range(dim_obs):
        plot_data["plot_count"] = ii+1
        plot_data["colour"] = plot_colours[ii]      
        plot_data["index"] = ii
        if errors_provided:
            calib_errors = errors_calib[ii]
            valid_errors = errors_valid[ii]
        rp.plot_measurements_with_calibration_and_validation_trajectory_with_errors( \
            independent_calib, measurements_calib[ii], predictions_calib[ii], calib_errors, \
            independent_valid, measurements_valid[ii], predictions_valid[ii], valid_errors, \
            plot_data)
    fig.show()


# TODO: refactor and make DRY
def plot_residual_trajectories_with_errors( \
    independent_calib, measurements_calib, predictions_calib, errors_calib, \
    independent_valid, measurements_valid, predictions_valid, errors_valid):
    """
    errors_calib and errors_valid can be None
    """
    # TODO: pre-conditions
    
    errors_provided = True
    if errors_calib is None:
        assert(errors_valid is None)
        errors_provided = False

    dim_obs = len(measurements_calib)
    fig = pp.figure(2)
    plot_data = {}
    plot_data["figure"] = fig
    plot_data["no_rows"] = dim_obs
    plot_data["no_cols"] = 1
    plot_colours = get_plot_colours(dim_obs)
    calib_errors = None
    valid_errors = None
    for ii in range(dim_obs):
        plot_data["plot_count"] = ii+1
        plot_data["colour"] = plot_colours[ii]      
        plot_data["index"] = ii 
        if errors_provided:
            calib_errors = errors_calib[ii]
            valid_errors = errors_valid[ii]
        rp.plot_residuals_with_calibration_and_validation_trajectory_with_errors( \
            independent_calib, measurements_calib[ii], predictions_calib[ii], calib_errors, \
            independent_valid, measurements_valid[ii], predictions_valid[ii], valid_errors, \
            plot_data)
    fig.show()


def plot_ensemble_trajectories(independent, ensembles, measurements, errors, plot_config):
    """
    Plots the ensemble trajectories of a set of states
    arguments: measurements and errors can be None
    independent numpy array NT
    ensembles numpy array NExNSxNT
    """
    
    fig = pp.figure("ensembles")
    dim_obs = len(ensembles[0])
    plot_data = {}
    plot_data["figure"] = fig
    plot_data["no_rows"] = dim_obs
    plot_data["no_cols"] = 1
    plot_colours = get_plot_colours(dim_obs)

    for ii in range(dim_obs):
        plot_data["plot_count"] = ii+1
        plot_data["colour"] = plot_colours[ii]    
        plot_data["index"] = ii
        plot_data["ylabel"] = plot_config["output_names"][ii]
        if measurements is not None and errors is not None:
            rp.plot_ensemble_trajectories(independent, ensembles[:,ii,:], measurements[ii], errors[ii], plot_data)
        else:
            rp.plot_ensemble_trajectories(independent, ensembles[:,ii,:], measurements, errors, plot_data)
    fig.show()
