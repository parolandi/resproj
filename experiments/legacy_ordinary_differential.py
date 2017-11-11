
from __future__ import print_function
import numpy

import common.utilities
import data.generator
import metrics.ordinary_differential_legacy
import models.analytical
import models.ordinary_differential
import results.plot_legacy
import solvers.initial_value_legacy
import solvers.dynamic_optimisation_legacy
import solvers.least_squares_legacy


# integrate, basic
def experiment1():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    yt, info = solvers.initial_value_legacy.solve_lsoda(models.ordinary_differential.linear, y0, t_if, [p], [u])
    y = common.utilities.sliceit_assnapshot(yt)
    
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()

    results.plot_legacy.plottrajectoryandobservations(t_if, measurements, y, models.analytical.exponential(p, t_if, y0, p*u))
    results.report.print_integration_basic(info)


# integrate, endpoint
def experiment2():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    y = solvers.initial_value_legacy.compute_endpoint([u], models.ordinary_differential.linear, y0, t_if, [p])
    t = t_if[len(t_if)-1]
    
    results.plot_legacy.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), t, y) 


# optimise, maximise
def experiment3():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u0 = 1.0
    p = 2.0 * u0
    t = t_if[len(t_if)-1]
    
    initial_guess = 0.1
    simple_bounds = [(0,10)]
    result = solvers.dynamic_optimisation_legacy.solve_slsqp_optimise_with_bounds(
        solvers.dynamic_optimisation_legacy.maximise_it, models.ordinary_differential.linear, y0, initial_guess, t_if, [p], simple_bounds)

    results.report.print_result(result)
    u = result.x
    results.plot_legacy.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), \
        t, solvers.initial_value_legacy.compute_endpoint(u, models.ordinary_differential.linear, y0, t_if, [p]))


# optimise; minimise
def experiment4():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u0 = 1.0
    p = 2.0 * u0
    t = t_if[len(t_if)-1]
    
    initial_guess = 0.1
    simple_bounds = [(0,10)]
    result = solvers.dynamic_optimisation_legacy.solve_slsqp_optimise_with_bounds(
        solvers.dynamic_optimisation_legacy.minimise_it, models.ordinary_differential.linear, y0, initial_guess, t_if, [p], simple_bounds)

    results.report.print_result(result)
    u = result.x
    results.plot_legacy.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), \
        t, solvers.initial_value_legacy.compute_endpoint(u, models.ordinary_differential.linear, y0, t_if, [p]))


# integrate, basic
def experiment5():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    t, yt = solvers.initial_value_legacy.solve_ode_lsoda(models.ordinary_differential.linear_ty, y0, t_if, [p], [u])
    y = common.utilities.sliceit_assnapshot(yt)

    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()

    results.plot_legacy.plottrajectoryandobservations(t, measurements, y, models.analytical.exponential(p, t, y0, p*u))


# integrate, trajectory
def experiment6():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    y = solvers.initial_value_legacy.compute_trajectory([p], models.ordinary_differential.linear, y0, [u], t_if)

    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    results.plot_legacy.plottrajectoryandobservations(t_if, measurements, y, models.analytical.exponential(p, t_if, y0, p*u)) 


def experiment7():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 3.0
    y = solvers.initial_value_legacy.compute_trajectory([p], models.ordinary_differential.linear, y0, [u], t_if)

    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    initial_guess = 0.1
    result = solvers.least_squares_legacy.solve_slsqp_orddiff(
        metrics.ordinary_differential_legacy.sum_squared_residuals, models.ordinary_differential.linear, \
        initial_guess, [u], measurements, y0, t_if)

    results.report.print_result(result)
    p = result.x
    results.plot_legacy.plottrajectoryandobservations(t_if, measurements, y, models.analytical.exponential(p, t_if, y0, p*u))
