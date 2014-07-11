
import matplotlib.pyplot

def plotit(independent, measurements, predictions, actuals):
    x = independent
    y_model = predictions
    y_meas = measurements
    y = actuals
    matplotlib.pyplot.plot(x, y_model, x, y_meas, "o", x, y)
    matplotlib.pyplot.legend(["fit", "obs", "true"])
    matplotlib.pyplot.show()
