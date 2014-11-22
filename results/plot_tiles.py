
import matplotlib.pyplot as pp


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
