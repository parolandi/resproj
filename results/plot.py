
import matplotlib.pyplot as pp

import data.nonparametrics as dnp

# TODO: rename to plot single


def plot_errors_and_residuals(independent,  errors, residuals):
    # TODO assertions
    
    x = independent
    legend = []
    for ii in range(len(errors)):
        pp.plot(x, errors[ii], 'o-')
        legend.append("e" + str(ii))
        pp.plot(x, residuals[ii], '+-')
        legend.append("p" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_fit(independent, measurements, predictions, actuals):
    # TODO assertions
    
    x = independent
    y_meas = measurements
    y_pred = predictions
    y_true = actuals
    legend = []
    for ii in range(len(y_meas)):
        pp.plot(x, y_meas[ii], 'o')
        legend.append("m" + str(ii))
        pp.plot(x, y_pred[ii], '+-')
        legend.append("p" + str(ii))
        pp.plot(x, y_true[ii], '*-')
        legend.append("t" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_measurements_with_calibration_and_validation_trajectory( \
    independent_calib, measurements_calib, predictions_calib, \
    independent_valid, measurements_valid, predictions_valid, \
    plot_data):
    # TODO assertions
    
    fig = plot_data["figure"]
    sp = fig.add_subplot(plot_data["no_rows"], plot_data["no_cols"], plot_data["plot_count"])
    t = independent_calib
    meas = measurements_calib
    pred = predictions_calib
    legend = []
    colour = plot_data["colour"]
    sp.plot(t, meas, colour+'o')
    legend.append("m-c-" + str(plot_data["index"]))
    sp.plot(t, pred, colour+'+')
    legend.append("p-c-" + str(plot_data["index"]))
    t = independent_valid
    meas = measurements_valid
    pred = predictions_valid
    sp.plot(t, meas, colour+'s')
    legend.append("m-v-" + str(plot_data["index"]))
    sp.plot(t, pred, colour+'x')
    legend.append("p-v-" + str(plot_data["index"]))
#    sp.legend(legend)
    

def plot_measurements_with_trajectory_with_errors( \
    independent, measurements, predictions, errors, \
    plot_data):
    """
    errors can be None
    """
    assert(plot_data is not None)
    # TODO assertions
    
    fig = plot_data["figure"]
    sp = fig.add_subplot(plot_data["no_rows"], plot_data["no_cols"], plot_data["plot_count"])
    t = independent
    meas = measurements
    pred = predictions
    err = errors
    legend = []
    colour = plot_data["colour"]
    sp.errorbar(t, meas, fmt = colour+'o', yerr = err)
    legend.append("m-" + str(plot_data["index"]))
    sp.plot(t, pred, colour+'+')
    legend.append("p-" + str(plot_data["index"]))
#    sp.legend(legend)


def plot_measurements_with_calibration_and_validation_trajectory_with_errors( \
    independent_calib, measurements_calib, predictions_calib, errors_calib, \
    independent_valid, measurements_valid, predictions_valid, errors_valid, \
    plot_data):
    """
    errors_calib and errors_valid can be None
    """
    assert(plot_data is not None)
    # TODO assertions
    
    fig = plot_data["figure"]
    sp = fig.add_subplot(plot_data["no_rows"], plot_data["no_cols"], plot_data["plot_count"])
    t = independent_calib
    meas = measurements_calib
    pred = predictions_calib
    err = errors_calib
    legend = []
    colour = plot_data["colour"]
    sp.errorbar(t, meas, fmt = colour+'o', yerr = err)
    legend.append("m-c-" + str(plot_data["index"]))
    sp.plot(t, pred, colour+'+')
    legend.append("p-c-" + str(plot_data["index"]))
    t = independent_valid
    meas = measurements_valid
    pred = predictions_valid
    err = errors_valid
    sp.errorbar(t, meas, fmt = colour+'s', yerr = err)
    legend.append("m-v-" + str(plot_data["index"]))
    sp.plot(t, pred, colour+'x')
    legend.append("p-v-" + str(plot_data["index"]))
#    sp.legend(legend)


def plot_residuals_with_calibration_and_validation_trajectory_with_errors( \
    independent_calib, measurements_calib, predictions_calib, errors_calib, \
    independent_valid, measurements_valid, predictions_valid, errors_valid, \
    plot_data):
    # TODO assertions
    
    fig = plot_data["figure"]
    sp = fig.add_subplot(plot_data["no_rows"], plot_data["no_cols"], plot_data["plot_count"])
    t = independent_calib
    meas = measurements_calib
    pred = predictions_calib
    res = pred - meas
    err = errors_calib
    legend = []
    colour = plot_data["colour"]
    sp.errorbar(t, res, fmt = colour+'o', yerr = err)
    sp.axhline(color = 'r')
    legend.append("r-c-" + str(plot_data["index"]))
    t = independent_valid
    meas = measurements_valid
    pred = predictions_valid
    res = pred - meas
    err = errors_valid
    sp.errorbar(t, res, fmt = colour+'s', yerr = err)
    sp.axhline(color = 'r')
    legend.append("r-v-" + str(plot_data["index"]))
#    sp.legend(legend)


def plot_ensemble_trajectories(independent, ensemble, measurements, errors, plot_data):
    """
    Plots the ensemble trajectories of a given state
    arguments: measurements and errors can be None
    independent numpy array NT
    ensembles numpy array NExNT
    """
    
    NE = len(ensemble)
    fig = plot_data["figure"]
    sp = fig.add_subplot(plot_data["no_rows"], plot_data["no_cols"], plot_data["plot_count"])
    colour = plot_data["colour"]
    for ii in range(NE):
        sp.plot(independent, ensemble[ii,:], colour+'+')
        sp.set_ylabel(plot_data["ylabel"])
    if measurements is not None and errors is not None:
        sp.errorbar(independent, measurements, fmt = colour+'o', yerr = errors)


def plot_observations(independent,  measurements):
    x = independent
    y_meas = measurements
    legend = [] 
    for ii in range(len(y_meas)):
        pp.plot(x, y_meas[ii], 'o')
        legend.append("m" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_residuals(independent,  residuals):
    x = independent
    ress = residuals
    legend = [] 
    for ii in range(len(ress)):
        pp.plot(x, ress[ii], 'o')
        legend.append("r" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_observation_ensembles(independent,  measurements):
    x = independent
    y_meass = measurements
    legend = []
    # ensembles
    done_already = False
    color_cycle = ['r', 'g', 'b', 'y']
    for ii in range(len(y_meass)):
        # observations
        for jj in range(len(y_meass[ii])):
            
            pp.plot(x, y_meass[ii][jj], color=color_cycle[jj], linestyle='', marker='o')
            if not done_already:
                legend.append("m" + str(jj))
        done_already = True
    pp.legend(legend)
    pp.show()


def plot_histogram_cutoff_by_count(data, bins, count):
    cutoff_data = dnp.cutoff_tail_by_count(data, count)
    pp.hist(cutoff_data, bins = bins)
    pp.show()


def plot_scatter(x, y):
    pp.plot(x, y, 'o')
    pp.show()
    
    
def plot_box(vertices):
    pp.vlines(vertices[0], vertices[1][0], vertices[1][1], colors='b')
    pp.hlines(vertices[1], vertices[0][0], vertices[0][1], colors='b')
    pp.show()


def plot_scatter_and_box(x, y, vertices):
    pp.plot(x, y, 'o')
    pp.vlines(vertices[0], vertices[1][0], vertices[1][1], colors='b')
    pp.hlines(vertices[1], vertices[0][0], vertices[0][1], colors='b')
    pp.show()
