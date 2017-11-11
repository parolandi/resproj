'''
Created on 28 Jun 2014

@author: mamuts
'''

from numpy import arange
from numpy import random
from scipy.optimize import leastsq
import matplotlib.pyplot

x = arange(0.1, 1, 0.9 / 10)
y = 2 * x
measurements = y + 0.1*random.randn(len(y))

def model(p, x):
    return p * x

def delta(p, x, measured):
    error = measured - model(p, x)
    return error

estimate, cov_x, info, msg, err = leastsq(delta, 0.1, args=(x, measurements), full_output=True)
print(estimate[0])
print(cov_x)
print(info)
print(msg)
print(err)
matplotlib.pyplot.plot(x, model(estimate[0], x), x, measurements, "o", x, y)
matplotlib.pyplot.legend(["fit", "data", "true"])
matplotlib.pyplot.show()