
from numpy import arange

import data.generator
import metrics.basic
import models.algebraic
import results.report
import results.plot
import solvers.least_squares

# linear regression
# print basic
def experiment3():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    initial_guess = 0.1
    estimate, cov, info, msg, err = solvers.least_squares.solve(
        metrics.basic.residual, models.algebraic.linear, initial_guess, x, measurements)

    results.report.print_least_squares_basic(estimate, info, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.linear(p, x), y)
    return

# linear regression
# print advanced
def experiment4():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    initial_guess = 0.1
    estimate, cov, info, msg, err = solvers.least_squares.solve(
        metrics.basic.residual, models.algebraic.linear, initial_guess, x, measurements)

    results.report.print_least_squares_detailed(estimate, cov, info, msg, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.linear(p, x), y)
    return

# linear regression
# analytical jacobian
# print advanced
def experiment5():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.linear(2, x)
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    initial_guess = 0.1
    estimate, cov, info, msg, err = solvers.least_squares.solve_with_jacobian(
        metrics.basic.residual, models.algebraic.linear, models.algebraic.jacobian_linear, initial_guess, x, measurements)

    results.report.print_least_squares_detailed(estimate, cov, info, msg, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.linear(p, x), y)
    return

# quadratic regression
# print advanced
def experiment6():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.quadratic(3, x)
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    initial_guess = 0.1
    estimate, cov, info, msg, err = solvers.least_squares.solve(
        metrics.basic.residual, models.algebraic.quadratic, initial_guess, x, measurements)

    results.report.print_least_squares_detailed(estimate, cov, info, msg, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.quadratic(p, x), y)
    return

# quadratic regression
# analytical jacobian
# print advanced
def experiment7():
    x = arange(0.1, 1, 0.9 / 10)
    y = models.algebraic.quadratic(3, x)
    data.generator.set_seed(117)
    measurements = y + 0.1*data.generator.normal_distribution(len(y))
    data.generator.unset_seed()
    
    initial_guess = 0.1
    estimate, cov, info, msg, err = solvers.least_squares.solve_with_jacobian(
        metrics.basic.residual, models.algebraic.quadratic, models.algebraic.jacobian_quadratic, initial_guess, x, measurements)

    results.report.print_least_squares_detailed(estimate, cov, info, msg, err)
    p = estimate[0]
    results.plot.plot_least_squares(x, measurements, models.algebraic.quadratic(p, x), y)
    return
