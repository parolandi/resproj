
import matplotlib.pyplot as pp
from matplotlib.patches import Ellipse
import numpy

import data.nonparametrics as dnp

# TODO: rename to plot single


def get_lim_scaling_factor():
    return 1.01


def handle_plot_data(fig, plot_data):
    if plot_data is not None:
        if "window_title" in plot_data:
            fig.canvas.set_window_title(plot_data["window_title"])
        if "title" in plot_data:
            fig.suptitle(plot_data["title"])
    

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


def plot_scatter(x, y, plot_data):
    fig = pp.figure()
    handle_plot_data(fig, plot_data)
    ax = fig.add_subplot(111)
    pp.plot(x, y, 'o')
    sf = get_lim_scaling_factor()
    ax.set_xlim(min(x)/sf, max(x)*sf)
    ax.set_ylim(min(y)/sf, max(y)*sf)
    pp.show()
    
    
def plot_box(vertices, plot_data):
    fig = pp.figure()
    handle_plot_data(fig, plot_data)
    ax = fig.add_subplot(111)
    pp.vlines(vertices[0], vertices[1][0], vertices[1][1], colors='b')
    pp.hlines(vertices[1], vertices[0][0], vertices[0][1], colors='b')
    sf = get_lim_scaling_factor()
    ax.set_xlim(vertices[0][0]/sf, vertices[0][1]*sf)
    ax.set_ylim(vertices[1][0]/sf, vertices[1][1]*sf)
    pp.show()


# TODO: limits
def plot_scatter_and_box(x, y, vertices, plot_data):
    """
    x, y numpy.array
    vertices list of list
    """
    fig = pp.figure()
    handle_plot_data(fig, plot_data)
    ax = fig.add_subplot(111)
    pp.plot(x, y, 'o')
    pp.vlines(vertices[0], vertices[1][0], vertices[1][1], colors='b')
    pp.hlines(vertices[1], vertices[0][0], vertices[0][1], colors='b')

    xlb = numpy.concatenate((x, numpy.asarray([vertices[0][0]])))
    xub = numpy.concatenate((x, numpy.asarray([vertices[0][1]])))
    ylb = numpy.concatenate((y, numpy.asarray([vertices[1][0]])))
    yub = numpy.concatenate((y, numpy.asarray([vertices[1][1]])))
    sf = get_lim_scaling_factor()
    ax.set_xlim(min(xlb)/sf, max(xub)*sf)
    ax.set_ylim(min(ylb)/sf, max(yub)*sf)
    
    pp.show()


def plot_ellipse(center, covar, plot_data):
    covariance = numpy.asmatrix(covar)
    # TODO: preconditions
    # sign eigenvals
    eigenvals, eigenvecs = numpy.linalg.eig(covariance)
    lambdaa = numpy.sqrt(eigenvals)
    ell = Ellipse(xy=center, width=lambdaa[0]*2, height=lambdaa[1]*2, angle=numpy.rad2deg(numpy.arccos(eigenvecs[0,0])))
    
    fig = pp.figure()
    handle_plot_data(fig, plot_data)
    ax = fig.add_subplot(111)
    ax.add_artist(ell)
    ell.set_clip_box(ax.bbox)
    sf = get_lim_scaling_factor()
    height = numpy.sqrt(covariance[0,0]) * sf
    width = numpy.sqrt(covariance[1,1]) * sf
    ax.set_xlim(center[0]-height, center[0]+height)
    ax.set_ylim(center[1]-width, center[1]+width)
    ell.set_facecolor('none')
    pp.show()


def plot_ellipse_and_box(center, covar, vertices, plot_data):
    covariance = numpy.asmatrix(covar)
    # TODO: preconditions
    # sign eigenvals
    '''
    eigenvals, eigenvecs = numpy.linalg.eig(covariance)
    lambdaa = numpy.sqrt(eigenvals)
    ell = Ellipse(xy=center, width=lambdaa[0]*2, height=lambdaa[1]*2, angle=numpy.rad2deg(numpy.arccos(eigenvecs[0,0])))
    '''
    vals, vecs = eigsorted(covariance)
    theta = numpy.degrees(numpy.arctan2(*vecs[:,0][::-1]))
    w, h = 2 * numpy.sqrt(vals)
    ell = Ellipse(xy=center, \
                  width=w, height=h,
                  angle=theta, color='black')
    lambdaa = numpy.sqrt(vals)
    
    fig = pp.figure()
    handle_plot_data(fig, plot_data)
    ax = fig.add_subplot(111)
    ax.add_artist(ell)
    ell.set_clip_box(ax.bbox)
    height = lambdaa[1] # numpy.sqrt(covariance[0,0]) * 1.2
    width = lambdaa[0] # numpy.sqrt(covariance[1,1]) * 1.2
    ell.set_facecolor('none')

    pp.vlines(vertices[0], vertices[1][0], vertices[1][1], colors='b')
    pp.hlines(vertices[1], vertices[0][0], vertices[0][1], colors='b')

    xlb = [center[0]-width]
    xub = [center[0]+width]
    xlb.append(vertices[0][0])
    xub.append(vertices[0][1])
    ylb = [center[1]-height]
    yub = [center[1]+height]
    ylb.append(vertices[1][0])
    yub.append(vertices[1][1])
    sf = get_lim_scaling_factor()
    ax.set_xlim(min(xlb)/sf, max(xub)*sf)
    ax.set_ylim(min(ylb)/sf, max(yub)*sf)

    pp.show()


def eigsorted(cov):
    vals, vecs = numpy.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]