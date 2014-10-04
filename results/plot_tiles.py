
import matplotlib.pyplot as pp


# TODO: parameterise, generalise
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
