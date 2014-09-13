
import matplotlib.pyplot as pyplot
import numpy


plot_count = 0
no_rows = 0
no_cols = 0


def plot_scatter(values, dynamic_range):
    pyplot.plot(values[0], values[1], 'o')
    pyplot.legend("scatter")
    if len(dynamic_range) > 0:
        pyplot.xlim([-dynamic_range[0], dynamic_range[0]])
        pyplot.ylim([-dynamic_range[1], dynamic_range[1]])
    pyplot.show()


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
    global plot_count
    plot_count = 0
    return pyplot.figure()


def show_figure():
    pyplot.show()
    

def increment_plot_count():
    global plot_count
    plot_count += 1
    return plot_count


def get_plot_count():
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
    plot_count = increment_plot_count()
    sp = figure.add_subplot(no_rows, no_cols, plot_count)
    sp.plot(iterations, values, 'o')
    if get_plot_count() <= no_cols:
        sp.set_title("obj-func")
    col_rank = plot_count // no_cols
    row_rank = col_rank % no_rows
    if  row_rank == 0:
        sp.set_ylabel("full")
    if  row_rank == 1:
        sp.set_ylabel("calib")
    if  row_rank == 2:
        sp.set_ylabel("valid")
    if  row_rank == 3:
        sp.set_ylabel("calib+valid")


def get_objective_function_contributions_plot(figure, iterations, values):
    no_rows, no_cols = get_plot_rows_and_cols()
    sp = figure.add_subplot(no_rows, no_cols, increment_plot_count())
    
    vals = numpy.transpose(values)
    for ii in range(len(vals)):
        sp.plot(iterations, vals[ii], 'o')
    if get_plot_count() <= no_cols:
        sp.set_title("obj-func-contribs")


def get_confidence_intervals_plot(figure, iterations, values):
    no_rows, no_cols = get_plot_rows_and_cols()
    sp = figure.add_subplot(no_rows, no_cols, increment_plot_count())
    
    vals = numpy.transpose(values)
    for ii in range(len(vals)):
        sp.plot(iterations, vals[ii], 'o')
    if get_plot_count() <= no_cols:
        sp.set_title("conf intervs")


def get_parameter_estimates_plot(figure, iterations, values):
    no_rows, no_cols = get_plot_rows_and_cols()
    sp = figure.add_subplot(no_rows, no_cols, increment_plot_count())
    
    vals = numpy.transpose(values)
    for ii in range(len(vals)):
        sp.plot(iterations, vals[ii], 'o')
    if get_plot_count() <= no_cols:
        sp.set_title("param ests")
