
from numpy import arange
from scipy.optimize import leastsq
import matplotlib.pyplot

import data.generator
import metrics.basic
import models.algebraic

def experiment1():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    
    estimate, cov_x, info, msg, err = leastsq(metrics.basic.residual_linear, 0.1, args=(x, measurements), full_output=True)

    print(estimate[0])
    print(cov_x)
    print(info)
    print(msg)
    print(err)
    matplotlib.pyplot.plot(x, models.algebraic.linear(estimate[0], x), x, measurements, "o", x, y)
    matplotlib.pyplot.legend(["fit", "data", "true"])
    matplotlib.pyplot.show()

def experiment2():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))

    print(metrics.basic.residual(0.1, x, models.algebraic.linear, measurements))
    
def experiment3():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    
    estimate, cov_x, info, msg, err = leastsq(metrics.basic.residual, 0.1, args=(x, models.algebraic.linear, measurements), full_output=True)

    print(estimate[0])
    print(cov_x)
    print(info)
    print(msg)
    print(err)
    matplotlib.pyplot.plot(x, models.algebraic.linear(estimate[0], x), x, measurements, "o", x, y)
    matplotlib.pyplot.legend(["fit", "data", "true"])
    matplotlib.pyplot.show()
