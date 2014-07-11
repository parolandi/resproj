
import matplotlib.pyplot

def plotfit(independent, measurements, predictions, actuals):
    x = independent
    y_model = predictions
    y_meas = measurements
    y = actuals
    matplotlib.pyplot.plot(x, y_model, x, y_meas, "o", x, y)
    matplotlib.pyplot.legend(["fit", "obs", "true"])
    matplotlib.pyplot.show()


def plottrajectoryandobservations(independent,  measurements, numerical, analytical):
    x = independent
    y_model = numerical
    y_meas = measurements
    y = analytical
    matplotlib.pyplot.plot(x, y_model, "+", x, y_meas, "o", x, y)
    matplotlib.pyplot.legend(["num", "obs", "ana"])
    matplotlib.pyplot.show()
    

def plotrajectoryandpoint(independent, analytical, singletime, singlevalue):
    x = independent
    y = analytical
    matplotlib.pyplot.plot(x, y, [singletime], [singlevalue], "o")
    matplotlib.pyplot.legend(["ana", "num"])
    matplotlib.pyplot.show()
