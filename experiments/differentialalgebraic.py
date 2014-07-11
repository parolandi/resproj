
from __future__ import print_function
import numpy

import common.utilities
import data.generator
import models.differentialalgebraic
import results.plot
import solvers.differentialalgebraic

import models.analytical

def experiment1():
    t_if = numpy.arange(0.0, 1.0, 1.0 / 10)
    y0 = 0.0
    u = 1.0
    p = 2.0
    yt, info = solvers.differentialalgebraic.solve_lsoda(models.differentialalgebraic.linear, y0, t_if, [p], [u])
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
    y = solvers.differentialalgebraic.compute_trajectory([u], models.differentialalgebraic.linear, y0, t_if, [p])
    t = t_if[len(t_if)-1]
    
    results.plot.plotrajectoryandpoint(t_if, models.analytical.exponential(p, t_if, y0, p*u), t, y) 
