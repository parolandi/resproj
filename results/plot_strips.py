
import matplotlib.pyplot as pp

#import results.plot as rp

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
    
    #dim_obs = len(data.measurements)
    fig = pp.figure(1)
    config.figure = fig
    #plot_data = {}
    #plot_data["figure"] = fig
    #plot_data["no_rows"] = dim_obs
    #plot_data["no_cols"] = 1
    #plot_colours = get_plot_colours(dim_obs)

    for ii in range(config.count):
        #plot_data["plot_count"] = ii+1
        #plot_data["colour"] = plot_colours[ii]      
        #plot_data["index"] = ii
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
    #assert(plot_data is not None)
    # TODO assertions
    
    fig = config.figure
    index = config.layout.index
    sp = fig.add_subplot(config.layout.no_rows, config.layout.no_cols, index+1)
    t = independent
    meas = measurements
    pred = predictions
    err = errors
    legend = []
    trace = config.multi_plots[index].trace
    colour = trace.colour
    mark = trace.mark
    sp.errorbar(t, meas, fmt = colour+mark, yerr = err)
    legend.append("m-" + str(index))
    sp.plot(t, pred, colour+'+')
    legend.append("p-" + str(index))
#    sp.legend(legend)
    sp.set_xlabel(config.multi_plots[index].x_axis.label)
    sp.set_ylabel(config.multi_plots[index].y_axis.label)