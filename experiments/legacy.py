
from numpy import arange
from scipy.optimize import leastsq

import data.generator
import metrics.legacy
import models.algebraic
import results.report
import results.plot

# linear regression
# call least-squared with hard coded residual
def experiment1():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    
    estimate, cov, info, msg, err = leastsq(metrics.legacy.residual_linear, 0.1, args=(x, measurements), full_output=True)

    results.report.print_least_squares_basic(estimate, info, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.linear(p, x), y)

# compute and print residual
def experiment2():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))

    print(metrics.basic.residual(0.1, x, models.algebraic.linear, measurements))