
from numpy import arange
from scipy.optimize import leastsq
import matplotlib.pyplot

import data.generator
import metrics.basic
import models.algebraic
import results.report
import results.plot

def experiment1():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    
    estimate, cov, info, msg, err = leastsq(metrics.basic.residual_linear, 0.1, args=(x, measurements), full_output=True)

    results.report.print_least_squares_basic(estimate, info, err)
    '''
    matplotlib.pyplot.plot(x, models.algebraic.linear(estimate[0], x), x, measurements, "o", x, y)
    matplotlib.pyplot.legend(["fit", "data", "true"])
    matplotlib.pyplot.show()
    '''

def experiment2():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))

    print(metrics.basic.residual(0.1, x, models.algebraic.linear, measurements))
    
def experiment3():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    estimate, cov, info, msg, err = leastsq(metrics.basic.residual, 0.1, args=(x, models.algebraic.linear, measurements), full_output=True)

    results.report.print_least_squares_basic(estimate, info, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.linear(p, x), y)
#    results.report.print_least_squares_detailed(estimate, cov, info, msg, err)
    '''
    matplotlib.pyplot.plot(x, models.algebraic.linear(estimate[0], x), x, measurements, "o", x, y)
    matplotlib.pyplot.legend(["fit", "data", "true"])
    matplotlib.pyplot.show()
    '''