
import matplotlib.pyplot as pp

import results.plot as rp


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


def plot_measurements_with_calibration_and_validation_trajectories( \
    independent_calib, measurements_calib, predictions_calib, \
    independent_valid, measurements_valid, predictions_valid):
    # TODO: pre-conditions
    
    dim_obs = len(measurements_calib)
    fig = pp.figure(1)
    plot_data = {}
    plot_data["figure"] = fig
    plot_data["no_rows"] = dim_obs
    plot_data["no_cols"] = 1
    plot_colours = ['r', 'g', 'b', 'y', 'c']
    for ii in range(dim_obs):
        plot_data["plot_count"] = ii+1
        plot_data["colour"] = plot_colours[ii]      
        plot_data["index"] = ii 
        rp.plot_measurements_with_calibration_and_validation_trajectory( \
            independent_calib, measurements_calib[ii], predictions_calib[ii], \
            independent_valid, measurements_valid[ii], predictions_valid[ii], \
            plot_data)
    pp.show()
