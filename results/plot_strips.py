
import matplotlib.pyplot as pp


def show_all():
    pp.show()


def plot_measurements_with_trajectories_with_errors( \
    data, config):
    """
    """
    # TODO: pre-conditions
    
    errors_provided = True
    if data.errors is None:
        errors_provided = False
    
    config.figure = pp.figure(1)
    for ii in range(config.count):
        config.layout.index = ii
        errors_ii = None
        if errors_provided:
            errors_ii = data.errors[ii]
        plot_measurements_with_trajectory_with_errors( \
            data.independent, data.measurements[ii], data.predictions[ii], errors_ii, \
            config)
    pp.show()


def plot_measurements_with_trajectory_with_errors( \
    independent, measurements, predictions, errors, \
    config):
    """
    errors can be None
    """
    # TODO: pre-conditions
    
    fig = config.figure
    index = config.layout.index
    single_plot = config.multi_plots[index]
    sp = fig.add_subplot(config.layout.no_rows, config.layout.no_cols, index+1)
    
    t = independent
    meas = measurements
    pred = predictions
    err = errors
    
    trace = single_plot.trace
    colour = trace.colour
    mark = trace.mark
    
    sp.errorbar(t, meas, fmt = colour+mark, yerr = err)
    sp.plot(t, pred, colour+'+')
    
#    legend = []
#    legend.append("m-" + str(index))
#    legend.append("p-" + str(index))
#    sp.legend(legend)

    sp.set_xlabel(single_plot.x_axis.label + single_plot.x_axis.eng_units)
    sp.set_ylabel(single_plot.y_axis.label + single_plot.y_axis.eng_units)
    sp.xaxis.set_ticks(single_plot.x_axis.major_ticks)
    sp.set_ylim(bottom = 0)
    
    
def plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
    data_calib, data_valid, config):
    """
    """
    # TODO: pre-conditions
    if data_valid is None:
        plot_measurements_with_trajectories_with_errors(data_calib, config)
        return
        
    errors_provided = True
    if data_calib.errors is None or data_valid.errors is None:
        assert(data_calib.errors == data_valid.errors)
        errors_provided = False
    
    config.figure = pp.figure(1)
    for ii in range(config.count):
        config.layout.index = ii
        errors_ii = None
        if errors_provided:
            errors_ii = data_calib.errors[ii]
            errors_jj = data_valid.errors[ii]
        plot_measurements_with_calibration_and_validation_trajectories_with_errors_internal( \
            data_calib.independent, data_calib.measurements[ii], data_calib.predictions[ii], errors_ii, \
            data_valid.independent, data_valid.measurements[ii], data_valid.predictions[ii], errors_jj, \
            config)
    pp.show()
    
    
def plot_measurements_with_calibration_and_validation_trajectories_with_errors_internal( \
    independent, measurements, predictions, errors, \
    independent_valid, measurements_valid, predictions_valid, errors_valid, \
    config):
    """
    errors can be None
    """
    # TODO: pre-conditions
    
    fig = config.figure
    index = config.layout.index
    single_plot = config.multi_plots[index]
    sp = fig.add_subplot(config.layout.no_rows, config.layout.no_cols, index+1)
    
    t = independent
    meas = measurements
    pred = predictions
    err = errors
    
    trace = single_plot.trace
    colour = trace.colour
    mark = trace.mark
    
    sp.errorbar(t, meas, fmt = colour+'o', yerr = err)
    sp.plot(t, pred, colour+'+')

    t = independent_valid
    meas = measurements_valid
    pred = predictions_valid
    err = errors_valid
    
    trace = single_plot.trace
    colour = trace.colour
    mark = trace.mark
    
    sp.errorbar(t, meas, fmt = colour+'s', yerr = err)
    sp.plot(t, pred, colour+'x')

#    legend = []
#    legend.append("m-" + str(index))
#    legend.append("p-" + str(index))
#    sp.legend(legend)

    sp.set_xlabel(single_plot.x_axis.label + single_plot.x_axis.eng_units)
    sp.set_ylabel(single_plot.y_axis.label + single_plot.y_axis.eng_units)
    sp.xaxis.set_ticks(single_plot.x_axis.major_ticks)
    sp.set_ylim(bottom = 0)