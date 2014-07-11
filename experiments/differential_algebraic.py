
from __future__ import print_function
import numpy

import common.utilities
import data.generator
import models.differential_algebraic
import results.plot
import solvers.intial_value
import solvers.dynamic_optimisation

import models.analytical

def experiment1():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    yt, info = solvers.intial_value.solve_lsoda(models.differential_algebraic.linear, y0, t_if, [p], [u])
    y = common.utilities.sliceit(yt)
    
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()

    results.plot.plottrajectoryandobservations(t_if, measurements, y, models.analytical.exponential(p, t_if, y0, p*u))
    results.report.print_integration_basic(info)


def experiment2():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    y = solvers.intial_value.compute_trajectory([u], models.differential_algebraic.linear, y0, t_if, [p])
    t = t_if[len(t_if)-1]
    
    results.plot.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), t, y) 


def experiment3():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    y = ([u], models.differential_algebraic.linear, y0, t_if, [p])
    t = t_if[len(t_if)-1]
    
    initial_guess = 0.1
    simple_bounds = [(0,10)]
    result = solvers.dynamic_optimisation.solve_slsqp_optimise_with_bounds(
        solvers.dynamic_optimisation.maximise_it, models.differential_algebraic.linear, y0, initial_guess, t_if, [p], simple_bounds)

    results.report.print_result(result)
    u = result.x
    results.plot.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), \
        t, solvers.intial_value.compute_trajectory(u, models.differential_algebraic.linear, y0, t_if, [p]))


def experiment4():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    y = ([u], models.differential_algebraic.linear, y0, t_if, [p])
    t = t_if[len(t_if)-1]
    
    initial_guess = 0.1
    simple_bounds = [(0,10)]
    result = solvers.dynamic_optimisation.solve_slsqp_optimise_with_bounds(
        solvers.dynamic_optimisation.minimise_it, models.differential_algebraic.linear, y0, initial_guess, t_if, [p], simple_bounds)

    results.report.print_result(result)
    u = result.x
    results.plot.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), \
        t, solvers.intial_value.compute_trajectory(u, models.differential_algebraic.linear, y0, t_if, [p]))
