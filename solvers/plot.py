
import matplotlib.pyplot as pyplot
import numpy

def plot_objective_function(iterations, values):
    pyplot.plot(iterations, values, 'o')
    pyplot.legend("objective function")
    pyplot.show()


def plot_objective_function_contributions(iterations, values):
    vals = numpy.transpose(values)
    for ii in range(len(vals)):
        pyplot.plot(iterations, vals[ii], 'o')
    pyplot.title("objective function contributions")
    pyplot.show()


def plot_chi_squared_test(iterations, values):
    pyplot.plot(iterations, values, 'o')
    pyplot.legend("chi-squared test")
    pyplot.show()


def plot_chi_squared_tests(iterations, values):
    vals = numpy.transpose(values)
    for ii in range(len(vals)):
        pyplot.plot(iterations, vals[ii], 'o')
    pyplot.title("chi-squared test")
    pyplot.show()
