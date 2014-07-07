
import matplotlib.pyplot

def plot_least_squares(independent, measurements, predictions, actuals):
    x = independent
    y_model = predictions
    y_meas = measurements
    y = actuals
    matplotlib.pyplot.plot(x, y_model, x, y_meas, "o", x, y)
    matplotlib.pyplot.legend(["fit", "data", "true"])
    matplotlib.pyplot.show()
