
import matplotlib.pyplot as pyplot
import numpy


plot_count = 0
no_rows = 0
no_cols = 0

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


def get_figure():
    return pyplot.figure()


def show_figure():
    pyplot.show()
    

def increment_plot_count():
    global plot_count
    plot_count += 1
    return plot_count


def set_plot_rows_and_cols(rows, cols):
    global no_rows
    global no_cols
    no_rows = rows
    no_cols = cols
    
    
def get_plot_rows_and_cols():
    global no_rows
    global no_cols
    return no_rows, no_cols
    

def get_objective_function_plot(figure, iterations, values):
    no_rows, no_cols = get_plot_rows_and_cols()
    sp = figure.add_subplot(no_rows, no_cols, increment_plot_count())
    sp.plot(iterations, values, 'o')
    sp.legend("objective function")


def get_objective_function_contributions_plot(figure, iterations, values):
    no_rows, no_cols = get_plot_rows_and_cols()
    sp = figure.add_subplot(no_rows, no_cols, increment_plot_count())
    
    vals = numpy.transpose(values)
    for ii in range(len(vals)):
        sp.plot(iterations, vals[ii], 'o')
    sp.legend("objective function contributions")
